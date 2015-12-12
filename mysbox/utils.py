from queue import Queue


class IndexableQueue(Queue):
    def __getitem__(self, index):
        with self.mutex:
            return self.queue[index]
