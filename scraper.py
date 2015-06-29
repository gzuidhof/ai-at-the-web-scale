import numpy as np
from multiprocessing import Process, Queue, JoinableQueue, Value
from threading import Thread
from context_get_pool import ContextGetPool
import itertools
import api
import models
import csv

HEADER = 'Age, Agent, Referer, ID, Language, Header, AdType, Color, Product, Price'.split(', ')

class Scraper():

    def __init__(self, n_workers = 1):
        self.n_workers = n_workers

    def _worker(self, worker_id):
        while True:
            task = self.todo.get()
            if task is None:
                print "Killing worker"+ str(worker_id)
                break #kill the worker

            self._scrape_run_id(task)
            self.results.put(task)

    def _scrape_run_id(self, run_id):
        ids = range(10000)
        getter = ContextGetPool(n_workers=1)
        model = models.RandomModel()
        context_ids = [(id, run_id) for id in ids]

        context_gen = getter.get(context_ids)

        data = []
        for (id, run_id), context in itertools.izip(context_ids, context_gen):
            action = model.propose(context)
            response = api.propose_page(id, run_id, action)
            success, reward = self._extract_reward(response, action)

            context = context['context']

            extracted = [context['Age'],context['Agent'],context['Referer'], \
                    context['ID'],context['Language']]

            d = extracted + list(action) + [success,reward]

            data.append(d)

        with open('data/' + str(run_id) + '.csv', "wb") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)
            writer.writerows(data)

    def _extract_reward(self, response, action):
		#0 or 1
		success = response['effect']['Success']

		#success * price
		reward = success * action[-1]

		return success, reward

    def go(self, run_ids):
        self.todo = Queue()

        #Put run_ids in todo
        for run_id in run_ids:
            self.todo.put(run_id)

        self.results = JoinableQueue()

        for i in xrange(self.n_workers):
            #t = Process(target=self._worker, args=(i,)).start()
            t = Thread(target=self._worker, args=(i,))
            t.daemon = True
            t.start()

        #Add poison
        for w in xrange(self.n_workers):
            self.todo.put(None)

        for i in xrange(len(run_ids)):
            task = self.results.get()
            print "run_id\"" + str(task) + "\" DONE! (n_done={0})".format(i+1)
            self.results.task_done()

        #Done
        self.results.join()
        self.todo.close()
        self.results.close()


if __name__ == '__main__':
    scraper = Scraper(100)
    scraper.go(range(5000))
