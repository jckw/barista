import queue
import threading


class SequentialQueue:
    def __init__(self):
        self.queue = queue.PriorityQueue()
        self.next_sequence_number = 1
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.end_marker_received = False

    def add(self, item, sequence_number):
        with self.lock:
            self.queue.put((sequence_number, item))
            self.condition.notify_all()

    def mark_end(self, sequence_number):
        self.add(None, sequence_number)

    def get_next(self):
        with self.condition:
            while True:  # Loop indefinitely until we can return an item or None
                if self.queue.empty() and self.end_marker_received:
                    # If the queue is empty and the end marker has been received, exit.
                    return None

                if not self.queue.empty():
                    sequence_number, item = self.queue.queue[
                        0
                    ]  # Peek at the item with the highest priority.
                    if sequence_number == self.next_sequence_number:
                        self.queue.get()  # Actually remove the item from the queue.
                        self.next_sequence_number += 1
                        if item is None:
                            # End marker detected, signal that no more items will be added
                            self.end_marker_received = True
                            return None
                        return item
                self.condition.wait()  # Wait until a new item is added or a notification is sent.
