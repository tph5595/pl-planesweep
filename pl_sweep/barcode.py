# pylint: disable=R0903
""" barcode: runs the barcode filtering algorithm on a set of bd_pairs """

from heapq import heappush, heappop

class Event:
    """ Event data container """

    # Class constant globals
    BIRTH = 0
    DEATH = 1

    def __init__(self, typ, point, node, idx):
        """ Set up the class variables """
        self.typ = typ
        self.point = point
        self.node = node
        self.idx = idx

    def sort_order(self):
        """Returns a tuple of the different parameters to sort on in order. The
        last value is the item itself."""
        return (self.point, id(self), self)


class BarcodeFilter:
    """ Preforms the barcode preproccessing step on a set of
    birth-death pairs """

    def __init__(self, bd_pairs, k):
        """ Set the birth-death pairs to be used """
        self.bd_pairs = bd_pairs
        self.k = k
        self.sorted = False
        self.stackSize = 0
        self.filtered = []
        self.top_k = {}
        self.events = []

    def set_bd_pairs(self, bd_pairs):
        """ Set the birth-death pairs to be used """
        self.bd_pairs = bd_pairs

    def __handle_birth_event(self, event):
        if self.stackSize < self.k:
            self.filtered.append(self.bd_pairs[event.idx])
            self.top_k[event.idx] = True
        self.stackSize += 1

    def __handle_death_event(self, event):
        self.stackSize -= 1
        # If the node was apart of the top k then find the next node to add and
        # add it to the filtered output
        # TODO: Can keep track of the bottom most node so that no searching is
        # required here
        if event.idx in self.top_k:
            tmp = event.node.next
            # Data is just the idx
            while tmp is not None and tmp.data in self.top_k:
                tmp = tmp.next
            # Add the new pair to the filtered output and mark it as such if
            # there is an item to add
            if tmp is not None:
                self.top_k[tmp.data] = True
                self.filtered.append(self.bd_pairs[tmp.data])

    def __generate_events(self):
        """ Generate the event points for the plane sweep filter algorithm """
        for i in range(len(self.bd_pairs)):
            if self.bd_pairs[i][0] == float("inf") or \
                    self.bd_pairs[i][1] == float("inf"):
                continue
            node = Node(i)
            self.__event_add(Event(Event.BIRTH, self.bd_pairs[i][0], node, i))
            self.__event_add(Event(Event.DEATH, self.bd_pairs[i][1], node, i))

    def __event_add(self, item):
        """ Adds an item to the event structure """
        heappush(self.events, item.sort_order())

    def __event_remove(self):
        """ Removes the next event from the event structure """
        tup = heappop(self.events)
        return tup[len(tup)-1]

    def filter(self):
        """ Preforms the barcode filter function on bd_pairs """
        # Generate event points from bd_pairs
        self.__generate_events()
        # Run plane sweep and calculate the filtered bd_pairs
        num_iter = len(self.events)
        for _ in range(num_iter):
            event = self.__event_remove()
            if event.typ == event.BIRTH:
                self.__handle_birth_event(event)
            if event.typ == event.DEATH:
                self.__handle_death_event(event)
        return self.filtered
