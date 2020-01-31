#!/usr/bin/env python

# Execute with
# $ python -m daliea

import daliea
import sys
from evolution import Evolution
from interface import Interface
from chromosome import Chromosome
from PySide2.QtWidgets import QApplication

if __package__ is None and not hasattr(sys, 'frozen'):
    # direct call of __main__.py
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))


def main(argv=None):
    if argv is None:
        argv = sys.argv
    app = QApplication(argv)
    chromosome = Chromosome()
    evolution = Evolution(chromosome)
    interface = Interface(chromosome)
    evolution.make_connection(interface)
    interface.make_connection(evolution)

    app.exec_()


if __name__ == '__main__':
    sys.exit(daliea.main())
