#!/usr/bin/env python3

import Levenshtein

from cmd import Cmd
from settings import (
    HDT_FILE, DATASET_FILE, OUTPUT_DATASET_FILE, STATS_FILE,
    PREDICATES_EXCLUDED, QUERY, RATIO)

from hdt import HDTDocument
import pandas as pd


# HDTDocument creation
document = HDTDocument(HDT_FILE)

# Se hace la consulta de los triples en funcion del sujeto/predicado/objeto
(triples, cardinality) = document.search_triples("", "", "")

print("{} objetos.".format(cardinality))


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


    def do_search(self, query):
        """
        """
        self.ret = set()
        print("cardinality of { ?s ?p ?o }: %i" % cardinality)
        for triple in triples:
            s, p, o = triple
            if o.startswith("http://dbpedia.org/ontology/"):
                obj = o.split('/')[-1]
                if o not in self.ret and Levenshtein.distance(obj, query) < self.distance:
                    print(o)
                    self.ret.add(o)

        return True

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
