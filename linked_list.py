class Node:
    def __init__(self, data):
        # Stores the song data (usually a dictionary)
        self.data = data
        self.next = None
        self.prev = None


class CircularDoublyLinkedList:
    def __init__(self):
        # Head points to the first song in the playlist
        self.head = None
        self.length = 0

    # Adds a new song to the end of the playlist
    def append(self, data):
        new_node = Node(data)

        # If this is the first song, it points to itself
        if self.head is None:
            new_node.next = new_node
            new_node.prev = new_node
            self.head = new_node
        else:
            # Otherwise, connect it to the end of the list
            tail = self.head.prev

            tail.next = new_node
            new_node.prev = tail

            new_node.next = self.head
            self.head.prev = new_node

        self.length += 1
        return new_node

    # Moves one existing song to a new position in the list
    def move_after(self, node, target_node):
        # If the node is already in the target location, nothing changes
        if node is target_node:
            return

        # Disconnect the node from its current position
        node.prev.next = node.next
        node.next.prev = node.prev

        # Insert the node after the target position
        node.next = target_node.next
        node.prev = target_node

        target_node.next.prev = node
        target_node.next = node

        # If the head was moved, update the head pointer
        if self.head is node:
            self.head = node.next

    # Completely removes a song from the playlist
    def remove(self, node):
        if self.length == 0:
            return

        # If this was the only song, clear the list
        if self.length == 1:
            self.head = None
        else:
            # Reconnect the surrounding nodes
            node.prev.next = node.next
            node.next.prev = node.prev

            # If the removed node was the head, update it
            if node is self.head:
                self.head = node.next

        self.length -= 1

    # Returns the next song in the playlist
    def next_node(self, current_node):
        if current_node is None:
            return None
        return current_node.next

    # Returns the previous song in the playlist
    def prev_node(self, current_node):
        if current_node is None:
            return None
        return current_node.prev

    # Converts the playlist into a regular Python list
    # This is useful for debugging and sending data to the UI
    def to_list(self):
        items = []
        if self.length == 0:
            return items

        cur = self.head
        for _ in range(self.length):
            items.append(cur.data)
            cur = cur.next

        return items