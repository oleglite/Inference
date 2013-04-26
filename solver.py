#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Oleg Beloglazov'

from structs import *


def make_goal_tree(goal, kb):
    solves = [fact for fact in kb.facts if fact.fits(goal)]
    solve_rules = [rule.substitute(goal) for rule in kb.rules if rule.pos_term.fits(goal)]

    rule_nodes = []
    for rule in solve_rules:
        rule_nodes.append(AndNode([make_goal_tree(term, kb) for term in rule.neg_terms], rule.pos_term))

    return OrNode([Node(value=solve) for solve in solves] + rule_nodes, goal)


def hard_union(dict1, dict2):
    """ Жесткое объединение двух словарей.
    Если в словарях для одинаковых ключей есть разные значения, возвращает None.
    Все остальные значения добавляет в результат. """

    res_dict = {}
    for key in dict1.keys() + dict2.keys():
        if key in dict1 and key in dict2:
            if dict1[key] == dict2[key]:
                res_dict[key] = dict1[key]
            else:
                return None
        elif key in dict1: res_dict[key] = dict1[key]
        elif key in dict2: res_dict[key] = dict2[key]
    return res_dict


def multi_hard_union(dicts1, dicts2):
    res = []
    for d1 in dicts1:
        for d2 in dicts2:
            united = hard_union(d1, d2)
            if united:
                res.append(united)
    return res


def solve_goal(goal, kb):
    """ Для цели goal найти решения в базе знаний kb.
    Возвращает множество решений. Решение - словарь {параметр:значение} """

    fact_solves = [dict(zip(goal.params, fact.constants)) for fact in kb.facts if fact.fits(goal)]

    rules_solves = []
    for rule in kb.rules:
        if rule.pos_term.fits(goal):
            rules_solves += [
                filter_solve(solve, rule.pos_term.params, goal.params) for solve in solve_rule(rule, kb)
            ]

    return fact_solves + rules_solves


def solve_rule(rule, kb):
    """ Получить список решений правила """

    terms_solves = [solve_goal(term, kb) for term in rule.neg_terms]

    solves = terms_solves[0]
    for term_solves in terms_solves[1:]:
        solves = multi_hard_union(solves, term_solves)
    return solves


def filter_solve(solve, initial_params, goal_params):
    """ Оставить в решении solve только параметры из списка params """

    return {goal_params[i]: solve[initial_params[i]] for i in xrange(len(goal_params))}
