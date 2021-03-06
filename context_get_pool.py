import api
from multiprocessing import Process, Queue, JoinableQueue, Value
from threading import Thread


class ContextGetPool():
    """
    Multithreaded context and proposal getter using producer-consumer model.
    """
    def __init__(self, n_workers = 1):
        self.n_workers = n_workers


    def _worker(self, worker_id):
        while True:
            task = self.todo.get()
            if task is None:
                #print "Killing "+ str(worker_id)
                break #kill the worker

            response = api.get_context(task[1],task[0])
            #print 'get', task[0], task[1]
            self.results.put(response)

    def _add_todo(self, id_tuples):
        self.n_added_total += len(id_tuples)
        for i, tup in enumerate(id_tuples):
            self.todo.put(tup)

    def get(self, id_tuples): #id_tuples: (run_id,id)[]

        self.todo = Queue()
        self.results = JoinableQueue()

        self.n_added_total = 0
        self.n_consumed = 0

        self._add_todo(id_tuples)

        #Start workers
        for i in xrange(self.n_workers):
            #t = Process(target=self._worker, args=(i,)).start()
            t = Thread(target=self._worker, args=(i,))
            t.daemon = True
            t.start()

        #Add poison for the workers
        for w in xrange(self.n_workers):
            self.todo.put(None)

        #Yield the results
        while self.n_consumed < self.n_added_total:
            yield self.results.get()
            self.results.task_done()
            self.n_consumed += 1

        #All done!
        self.results.join()
        self.todo.close()
        self.results.close()


# Test
if __name__ == '__main__':
    #Run ID 0 full
    id_tuples = [(id, 0) for id in xrange(10001)]

    pool = ContextGetPool(n_workers=420)

    for i, x in enumerate(pool.get(id_tuples)):
        if i % 100 == 0:
            print i#, x

    print "Closing"
