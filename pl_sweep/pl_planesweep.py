""" This calculates the presistant landscapes of a set of bdpairs. The pairs
should be a list of tuples with the birth then the death value """

from heapq import heappush, heappop
import time
from shapely.geometry import LineString
from matplotlib import pyplot as plt


class PersistantMountain:
    """ A specific mountain in the generation of the PersistantLandscape """

    def __init__(self, birth, midpoint, death):
        self.__pos = -1
        self.current_slope = 1
        self.birth = birth
        self.midpoint = midpoint
        self.death = death

    def set_pos(self, pos):
        """Set the position of a PersistantMountain in the PersistantLandscape.
        This is for bookkeeping  between events. It does not affect the status
        structure in a PersistantLandscape"""
        self.__pos = pos

    def get_pos(self):
        """ Returns the current position of the PersistantMountain """
        return self.__pos

    def after_midpoint(self):
        """ Signafy that the slope has changed after the midpoint and take
        relevent actions """
        self.current_slope = -1
        return self

    def get_p1(self):
        """Returns the START of the current line segment that is intersected by
        the status line"""
        if self.current_slope == 1:
            return self.birth
        return self.midpoint

    def get_p2(self):
        """ Returns the END of the current line segment that is intersected by
        the status line"""
        if self.current_slope == 1:
            return self.midpoint
        return self.death


class Event:
    """Container for the information related to a PersistantLandscape event """
    # Defines the sorting order of different event points
    DEATH_POINT = 0
    BIRTH_POINT = 1
    MIDDL_POINT = 2
    INTER_POINT = 3

    def __init__(self, typ, point, parent_mountain, parent_mountain2=None):
        self.parent_mountain = parent_mountain
        self.parent_mountain2 = parent_mountain2
        self.typ = typ
        self.point = point

    def typ(self):  # pylint: disable=E0202
        """ Returns the type event point """
        return self.typ

    def sort_order(self):
        """Returns a tuple of the different parameters to sort on in order. The
        last value is the item itself."""
        return (self.point[0], self.point[1], self.typ, id(self), self)


class PersistantLandscape:
    """ Class to manage a presistant landscape and generate a presistant
    landscape from a set of bd_pairs """

    def __init__(self, bd_pairs, max_lambda):
        self.bd_pairs = bd_pairs
        self.max_lambda = max_lambda
        self.events = []
        self.landscapes = []
        self.status = []
        self.max_pos = 0
        self.debug = False

    def clear(self, bd_pairs, max_lambda):
        """ Reset the PersistantLandscape to a clean state """
        self.bd_pairs = bd_pairs
        self.max_lambda = max_lambda
        self.events = []
        self.landscapes = []
        self.status = []
        self.max_pos = 0

    def enable_debug(self, state):
        """ Enables debug mode """
        self.debug = state

    def __event_add(self, item):
        """ Adds an item to the event structure """
        heappush(self.events, item.sort_order())

    def __event_remove(self):
        """ Removes the next event from the event structure """
        tup = heappop(self.events)
        return tup[len(tup)-1]

    def __status_add(self, event):
        """ Add the PersistantMountain of the provided event to the bottom of
        the status structure. Returns the pos the PersistantMountain was
        inserted at. """
        # Position we are about to insert at
        pos = self.max_pos
        self.max_pos += 1
        # Save the position we are inserting the PersistantMountain into
        event.parent_mountain.set_pos(pos)
        # Add the PersistantMountain to the bottom of the status structure
        if len(self.status) > 0 and self.status[-1] is None:
            # Check to see if there is an open spot
            self.status[-1] = event.parent_mountain
        else:
            self.status.append(event.parent_mountain)
        return pos

    def __status_remove(self):
        """ Removes the lowest PersistantMountain from the event structure """
        self.max_pos += -1
        # self.status[self.max_pos] = None
        self.status.pop()

    def __generate_initial_event_points(self):
        """ Adds the start, midpoint and end points of for each bdpairs to the
        event structure """
        for _ in range(0, self.max_lambda):
            self.landscapes.append([])
        # Insert initial points
        for bd_pair in self.bd_pairs:
            if bd_pair[0] == float("inf") or bd_pair[1] == float("inf"):
                continue
            # Birth
            birth = float(bd_pair[0])
            # Death
            death = float(bd_pair[1])
            # Calculate midpoint
            # TODO Double check this formula
            half_dist = ((death-birth)/2)
            # Define the points of interest
            birth_point = (birth, 0)
            mid_point = (half_dist+birth, half_dist)
            death_point = (death, 0)
            # Create a PersistantMountain to share between the event points so
            # that they can share variables
            event_mountain = PersistantMountain(
                birth_point, mid_point, death_point)
            # Create Intitial event points
            birth_event = Event(Event.BIRTH_POINT, birth_point, event_mountain)
            mid_event = Event(Event.MIDDL_POINT, mid_point, event_mountain)
            death_event = Event(Event.DEATH_POINT, death_point, event_mountain)
            # Add points to event structure
            self.__event_add(birth_event)
            self.__event_add(mid_event)
            self.__event_add(death_event)

    def __intersects_with_upper_neighbor(self, mountain):
        """ Returns true if the parent PersistantMountain of the event point
        intersects with the PersistantMountain that is right above it in the
        status structure """
        # Get the neighbor PersistantMountain
        neighbor_pos = mountain.get_pos()-1
        if neighbor_pos < 0 or \
                self.status[neighbor_pos] is None:
            return None
        # print("checking " + str(neighbor_pos))
        neighbor = self.status[neighbor_pos]
        # If they have the same slope they cannot intersect
        if neighbor.current_slope == 1:
            return None
        # Result of the barcode theorem
        if mountain.death > neighbor.death:
            return neighbor
        return None

    def __intersects_with_lower_neighbor(self, mountain):
        """ Returns true if the parent PersistantMountain of the event point
        intersects with the PersistantMountain that is right below it in the
        status structure """
        # Get the neighbor PersistantMountain
        neighbor_pos = mountain.get_pos()+1
        if neighbor_pos >= len(self.status) or \
                self.status[neighbor_pos] is None:
            return None
        neighbor = self.status[neighbor_pos]
        # If they have the same slope they cannot intersect
        if neighbor.current_slope == -1:
            return None
        # Result of the barcode theorem
        if mountain.death < neighbor.death:
            return neighbor
        return None

    def __add_intersection_event(self, mountain1, mountain2):
        """ Determines the Intersection of two mountains and adds the
        intersection to the event list """
        # Define lines for the intersection
        line1 = LineString([mountain1.get_p1(), mountain1.get_p2()])
        line2 = LineString([mountain2.get_p1(), mountain2.get_p2()])
        # Find the intersection
        int_pt = line1.intersection(line2)
        # Create a new event point and add it to the event list
        int_tup = (int_pt.x, int_pt.y)
        event = Event(Event.INTER_POINT, int_tup, mountain1, mountain2)
        self.__event_add(event)

    def __handle_birth_point(self, event):
        """ Update the data structure with the knowledge of a new start point
        with values defined in event """
        pos = self.__status_add(event)
        neighbor = self.__intersects_with_upper_neighbor(event.parent_mountain)
        if neighbor is not None:
            self.__add_intersection_event(event.parent_mountain, neighbor)
        if pos < self.max_lambda:
            self.landscapes[pos].append(event.point)

    def __handle_mid_point(self, event):
        """ Update the data structure with the knowledge of a new mid point
        with values defined in event """
        # Update the PersistantMountain
        event.parent_mountain.after_midpoint()
        # Check for intersections
        neighbor = self.__intersects_with_lower_neighbor(event.parent_mountain)
        if neighbor is not None:
            self.__add_intersection_event(neighbor, event.parent_mountain)
        # Update the logging structure
        pos = event.parent_mountain.get_pos()
        if pos < self.max_lambda:
            self.landscapes[pos].append(event.point)

    def __flip_points(self, mountain1, mountain2):
        """ Flip two points """
        # Switch positions
        m1_pos = mountain1.get_pos()
        mountain1.set_pos(mountain2.get_pos())
        mountain2.set_pos(m1_pos)
        # Update status structure
        self.status[mountain1.get_pos()] = mountain1
        self.status[mountain2.get_pos()] = mountain2

    def __handle_intersection_point(self, event):
        """ Update the data structure with the knowledge of a new intersection
        point with values defined in event """
        new_top_mtn = event.parent_mountain
        new_bot_mtn = event.parent_mountain2
        # Flip the points
        self.__flip_points(new_top_mtn, new_bot_mtn)
        # Check for intersections
        upper_neighbor = self.__intersects_with_upper_neighbor(new_top_mtn)
        if upper_neighbor is not None:
            self.__add_intersection_event(new_top_mtn, upper_neighbor)
        lower_neighbor = self.__intersects_with_lower_neighbor(new_bot_mtn)
        if lower_neighbor is not None:
            self.__add_intersection_event(lower_neighbor, new_bot_mtn)
        # Update logging structure
        pos_top = new_top_mtn.get_pos()
        if pos_top < self.max_lambda:
            self.landscapes[pos_top].append(event.point)
        pos_bot = new_bot_mtn.get_pos()
        if pos_bot < self.max_lambda:
            self.landscapes[pos_bot].append(event.point)

    def __handle_end_point(self, event):
        """ Update the data structure with the knowledge of a new end point
        with values defined in event """
        pos = event.parent_mountain.get_pos()
        if pos < self.max_lambda:
            self.landscapes[pos].append(event.point)
        # Update the event structure
        self.__status_remove()

    def generate_landscapes(self):
        """Generate the presistant landscapes based off of the bd_pairs defined
        in this PersistantLandscape"""
        # Create initial event points
        self.__generate_initial_event_points()
        # Loop over every event
        # This loop adds any intersections it finds as new events and places
        # them in order of x axis then y axis
        while len(self.events) > 0:
            if self.debug:
                print("Number of events left: " + str(len(self.events)))
                print("Status" + str(self.status))
                time.sleep(.300)

            # Get the next event
            event = self.__event_remove()
            if event.typ == event.BIRTH_POINT:
                self.__handle_birth_point(event)
            elif event.typ == event.MIDDL_POINT:
                self.__handle_mid_point(event)
            elif event.typ == event.INTER_POINT:
                self.__handle_intersection_point(event)
            elif event.typ == event.DEATH_POINT:
                self.__handle_end_point(event)
        return self.landscapes

    def plot(self):
        """ Plot the PersistantLandscapes """
        # Generate landscapes if they don't exist
        if not self.landscapes:
            self.generate_landscapes()
        # Generate graph
        fig = plt.figure(1, figsize=(5, 5), dpi=90)
        ax = fig.add_subplot(111)
        ax.set_title('Persistant Landscapes')
        for landscape in self.landscapes:
            poly = LineString(landscape)
            if not poly.is_empty:
                x, y = poly.xy
                ax.plot(x, y)
        plt.show()

    def __line_int(self, a, b):
        """ Returns the area under a line segment starting at a and ending at b
        assuming they have a slope of 1 or -1"""
        bottom = b[0] - a[0]
        side = abs(b[1]-a[1]) / 2
        return  bottom * side

    def integrate(self, landscapes=None):
        """ Integrate the area under a persisnat landscape or the differnce if
        multiple
        Note: This should be done on the GPU"""
        result = []
        if landscapes is None:
            landscapes = self.landscapes
        for landscape in landscapes:
            # Calculating difference list
            partial_integration = 0
            for prev, current in zip(landscape[0::], landscape[1::]):
                partial_integration += self.__line_int(prev, current)
            result.append(partial_integration)
        return result
