#!/usr/bin/env python3

import Levenshtein

from cmd import Cmd
from settings import (
    HDT_FILE, DATASET_FILE, OUTPUT_DATASET_FILE, STATS_FILE,
    PREDICATES_EXCLUDED, QUERY, RATIO)

import pandas as pd
from hdt import HDTDocument
from helpers import query


class HDTPrompt(Cmd):
    prompt = 'hdt> '
    intro = "Welcome! Type ? to list commands"
    distance = 3
    ret = set()

    def do_exit(self, inp):
        """exit the application. Shorthand: x q."""
        print(self.ret)
        print("Bye")
        return True


    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')


    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)

        print("Default: {}".format(inp))


    def do_search_dataset(self, query):
        """
        """
        with open('index.txt', 'r') as index:
            self.ret = []
            for k in index.readlines():
                k = k.strip()
                dist = Levenshtein.distance(k, query)
                if dist < self.distance:
                    self.ret.append((k, dist))
        for idx, k in enumerate(self.ret):
            print('{}: {} (dist: {})'.format(idx, k[0], k[1]))


    def do_select_dataset(self, idx):
        self.ds = "http://dbpedia.org/ontology/{}".format(self.ret[int(idx)][0])
        print("{} selected!".format(self.ds))
        print("Process dataset... please wait!")
        query(self.ds)
        Print('Done!')


    def do_show_set(self):
        """
        """
        print(self.ret)

    def do_set_distance(self, dist):
        """
        """
        self.distance = int(dist)


    def do_show_distance(self, s):
        """
        """
        print(self.distance)

    do_EOF = do_exit
    help_EOF = help_exit


HDTPrompt().cmdloop()
