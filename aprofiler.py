'''
A profiler
==========

Unlike the others python profilers, this one is dedicated to profile your
application logic. You can emit(push/pop) events, or marks with information.
When you stop, the profiler will generate a json with all the events.
You can then generate HTML graphics out of it.

'''

__all__ = ('Profiler', 'profiler')

from os import getpid
from json import dump
from time import time

class Aprofiler(object):
    '''Class for doing a profiling.
    '''
    def __init__(self, name):
        object.__init__(self)
        self.name = 'mainloop'
        self.enabled = False
        self.events = []
        self.marks = []
        self.last_start_index = 0

    def push(self, event, t=None):
        '''Add a "start" event to the events list
        '''
        if not self.enabled:
            return
        if t is None:
            t = time()
        if event == 'mainloop':
            self.last_start_index = len(self.events)
        self.events.append((t, 'start-' + event))
        return t

    def pop(self, event, t=None):
        '''Add an "end" event to the events list
        '''
        if not self.enabled:
            return
        if t is None:
            t = time()
        if event == 'mainloop':
            if self.marks and self.last_start_index:
                i = self.last_start_index
                self.events = self.events[:i] + self.marks + self.events[i:]
                self.marks = []
                self.last_start_index = 0
        self.events.append((t, 'stop-' + event))
        return t

    def mark(self, name, message):
        '''Add a "mark" to the events list
        If the mark is generated during a mainloop, it will be added before the
        start of the main loop, when the main loop is end event is emitted.
        '''
        t = time()
        self.marks.append((t, 'mark-{}'.format(name), message))

    def start(self):
        '''Start the profiler
        '''
        self.enabled = True

    def stop(self):
        '''Stop the profiler, and dump everything on the json
        '''
        self.enabled = False
        fn = 'profiler-{}.json'.format(getpid())
        with open(fn, 'w') as fd:
            dump(self.events, fd)


#: Create a default profiler
profiler = Aprofiler()

