class Node:
    """ Node for the StackLinkedList """

    def __init__(self, data):
        """ Creates a new Node """
        self.data = data
        self.next = None
        self.prev = None

    def remove(self):
        if self.next is not None:
            self.next.prev = self.prev
        if self.prev is not None:
            self.prev.next = self.next
        return (self.prev, self.next)


class StackLinkedList:
    """ Data structure needed for BarcodeFilter """

    def __init__(self):
        """ Prepare the structure for data """
        self.len = 0
        self.head = None
        self.tail = None

    def insert(self, node):
        """ Insert a node into the data structure """
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node

    def remove(self, node):
        """ Remove the given node from the StackLinkedList """
        if node is Node:
            return
        neighbors = node.remove()
        # Check if node was the head
        if neighbors[0] is None:
            self.head = neighbors[1]
        # Check if node was the tail
        if neighbors[1] is None:
            self.tail = neighbors[0]
        self.len -= 1


class Event:
    """ Event data container """

    def __init__(self, node, idx):
        self.node = node


class BarcodeFilter:
    """ Preforms the barcode preproccessing step on a set of
    birth-death pairs """

    def __init__(self, bd_pairs, k):
        """ Set the birth-death pairs to be used """
        self.bd_pairs = bd_pairs
        self.k = k
        self.sorted = False
        self.stack = StackLinkedList()
        self.filtered = []
        self.top_k = []

    def set_bd_pairs(self, bd_pairs):
        """ Set the birth-death pairs to be used """
        self.bd_pairs = bd_pairs

    def set_sorted(self, state):
        self.sorted = state

    def __handle_birth_event(self, event):
        if len(self.stack) < self.k:
            self.filtered.append(self.bd_pairs[event.idx])
            self.top_k[event.idx] = True
        self.stack.insert(event.node)

    def __handle_death_event(self, event):
        self.stack.remove(event.node)
        # If the node was apart of the top k then find the next node to add and
        # add it to the filtered output
        # TODO: Can keep track of the bottom most node so that no searching is
        # required here
        if self.top_k[event.node.idx]:
            tmp = event.node.next
            while not self.top_k[tmp.data.idx]:
                tmp = tmp.next
            # Add the new pair to the filtered output and mark it as such
            self.top_k[tmp.data.idx] = True
            self.filtered.append(self.bd_pairs[tmp.data.idx])

    def filter(self):
        """ Preforms the barcode filter function on bd_pairs """
        # Values must be sorted
        if not self.sorted:
            self.bd_pairs.sort()
        # Generate event points from bd_pairs
        events = self.__generate_events()
        # Run plane sweep and calculate the filtered bd_pairs
        for event in events:
            if event.typ == event.BIRTH:
                self.__handle_birth_event(event)
            if event.typ == event.DEATH:
                self.__handle_death_event(event)
