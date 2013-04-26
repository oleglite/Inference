#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Oleg Beloglazov'

import sys
import solver
import kbparser


def print_solves(goal, solves):
    print '\t'.join(goal.params)
    print
    for solve in solves:
        print '\t'.join([solve[param] for param in goal.params])


def main():
    if len(sys.argv) != 3:
        print 'usage: ./inference.py database-source-file goal'
        sys.exit(1)

    source_lines = open(sys.argv[1], 'r').readlines()
    goal_str = sys.argv[2]
    try:
        kb = kbparser.parse_kb(source_lines)
    except kbparser.ParseException:
        print 'Syntax error in knowledge base: "%s"' % sys.exc_value
        sys.exit(1)

    try:
        goal = kbparser.parse_goal(goal_str)
    except kbparser.ParseException:
        print 'Syntax error in goal: "%s"' % sys.exc_value
        sys.exit(1)
        
    print kb
    print
    print solver.make_goal_tree(goal, kb)
    print

    print_solves(goal, solver.solve_goal(goal, kb))


if __name__ == '__main__':
    main()
