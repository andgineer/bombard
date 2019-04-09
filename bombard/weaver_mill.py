"""
Multi-thread processor abstraction.

Override method worker in descendant.

"""
from threading import Thread
from queue import Queue
from copy import deepcopy
from abc import abstractmethod


class WeaverMill:
    def __init__(self, threads_num: int=10):
        """
        :param threads_num: How many threads we will use.
        """
        self.threads_num = threads_num
        self.threads = []
        self.queue = Queue(threads_num)
        self.job_count = 0

        for thread_id in range(threads_num):
            t = Thread(target=self.thread_worker, args=[thread_id])
            t.daemon = True
            t.start()
            self.threads.append(t)

    def thread_worker(self, thread_id):
        """
        Get job from queue and pass it to abstract worker
        that should be implemented in descendant.

        Even if worker throw exception we mark the job we gave him as done.

        Job == None is a signal to stop work.
        """
        while True:
            job = deepcopy(self.queue.get())
            if job is None:
                break
            try:
                self.worker(thread_id, job)
            finally:
                self.queue.task_done()

    @abstractmethod
    def worker(self, thread_id, job):
        """
        Implement your job processor, runs in thread.

        :param thread_id: just sequential number of the thread we work into
        :param job: job from queue
        """
        pass

    def start(self):
        """ Starts all threads and lock until queue is not empty """
        self.queue.join()

    def stop(self):
        """ Stops all threads - send stop signal to queue and lock until they stop """
        for _ in range(self.threads_num):
            self.queue.put(None)
        for thread in self.threads:
            thread.join()
