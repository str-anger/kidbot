#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime


class Item:
    def __init__(self, text):
        self.text = text
        words = text.split('\t')
        self.ts = int(words[0])
        self.time = datetime.datetime.fromtimestamp(self.ts)
        self.action = words[1]
        self.args = words[2:]
        
    def time_to(self, event):
        if event:
            return event.ts - self.ts
        else:
            return 0

    def days_from(self, date):
        return (self.ts - date.timestamp()) / 3600 / 24.0

    def get_weight(self):
        return int(self.args[0])
		
    def __str__(self):
        return "@{0} случилось {1} с аргументами {2}".format(self.time, self.action, self.args)

    def __repr__(self):
        return self.__str__()
    
    @classmethod
    def get_all(cls, events, action):
        return [event for event in events if event.action==action]
		
    @classmethod
    def consequense_in_range(cls, events, action_open, action_close, time_hours=10, single=True):
        time_sec = time_hours * 3600
        opens = cls.get_all(events, action_open)
        closes = cls.get_all(events, action_close)
        pairs = []
        for op in opens:
            pair = [op, None]
            subr = filter(lambda e: e.ts > op.ts and e.ts <= op.ts + time_sec, closes)
            if single:
                pair[1] = next(subr, None)
            else:
                pair[1] = list(subr)
            pairs.append((*pair,))
        return pairs
