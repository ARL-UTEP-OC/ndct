#Taken from:
# https://stackabuse.com/python-linked-lists/

class ListNode:
    def __init__(self, data):
        "constructor class to initiate this object"

        # store data
        self.data = data
        
        # store reference (next item)
        self.next = None

        # store reference (previous item)
        self.previous = None
        return

    def has_value(self, value):
        "method to compare the value with the node data"
        if self.data == value:
            return True
        else:
            return False

class DoubleLinkedList:
    def __init__(self):
        "constructor to initiate this object"

        self.head = None
        self.tail = None
        return

    def list_length(self):
        "returns the number of list items"
        
        count = 0
        current_node = self.head

        while current_node is not None:
            # increase counter by one
            count = count + 1
            
            # jump to the linked node
            current_node = current_node.next
        
        return count

    def output_list(self):
        "outputs the list (the value of the node, actually)"
        current_node = self.head

        while current_node is not None:
            print(current_node.data)

            # jump to the linked node
            current_node = current_node.next
        
        return

    def unordered_search (self, value):
        "search the linked list for the node that has this value"

        # define current_node
        current_node = self.head

        # define position
        node_id = 1

        # define list of results
        results = []

        while current_node is not None:
            if current_node.has_value(value):
                results.append(node_id)
            
            # jump to the linked node
            current_node = current_node.next
            node_id = node_id + 1
        
        return results

    def add_list_item(self, item):
        "add an item at the end of the list"

        if isinstance(item, ListNode):
            if self.head is None:
                self.head = item
                item.previous = None
                item.next = None
                self.tail = item
            else:
                self.tail.next = item
                item.previous = self.tail
                self.tail = item
        
        return