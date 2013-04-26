#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Oleg Beloglazov'

import re
from structs import *

# Patterns of elementary terms
const_match = r'[a-z]+'
var_match = r'[A-Z]+'
param_match = r'{c}|{v}'.format(c=const_match, v=var_match)

# Patterns for parsing facts
fact_pattern = r'^({v})\(({c}(, *{c})*)?\)\.'.format(c=const_match, v=var_match)
constants_pattern = r'({c}),? *'.format(c=const_match)
re_fact = re.compile(fact_pattern)
re_constants = re.compile(constants_pattern)

# Patterns for parsing rules
term_match_pattern = r'({v}\((({p})(, *({p}))*)?\))'.format(v=var_match, p=param_match)
rules_match_pattern = r'^({t} *<- *{t} *(; *{t})*\.)'.format(t=term_match_pattern)
term_pattern = r'({v})\((({p})(, *({p}))*)?\)'.format(v=var_match, p=param_match)
re_rule = re.compile(rules_match_pattern)
re_term_match = re.compile(term_match_pattern)
re_term = re.compile(term_pattern)
re_param = re.compile(param_match)

# Patterns for parsing goal
goal_param_match = param_match + r'|\?'
goal_term_pattern = r'({v})\((({p})(, *({p}))*)?\)'.format(v=var_match, p=(goal_param_match))
re_goal = re.compile(goal_term_pattern)
re_goal_param = re.compile(goal_param_match)


class ParseException(Exception): pass

def parse_kb(strings_list):
    facts = []
    rules = []
    for str in [str.rstrip() for str in strings_list]:
        if is_fact(str):
            facts.append(parse_fact(str))
        elif is_rule(str):
            rules.append(parse_rule(str))
        elif str:
            raise ParseException(str)
    return KnowledgeBase(facts, rules)



def is_fact(str):
    return bool(re_fact.match(str))

def parse_fact(str):
    fact_groups = re_fact.findall(str)[0]
    fact_name = fact_groups[0]
    fact_constants = re_constants.findall(fact_groups[1])
    fact = Fact(fact_name, fact_constants)
    return fact


def is_rule(str):
    return bool(re_rule.match(str))


def parse_rule(str):
    rules_groups = re_rule.findall(str)[0]
    terms = []
    for terms_groups in re_term_match.findall(rules_groups[0]):
        for term_groups in re_term.findall(terms_groups[0]):
            term_name = term_groups[0]
            term_params = re_param.findall(term_groups[1])
            terms.append(Term(term_name, term_params))
    rule = Rule(terms[0], terms[1:])
    return rule

def parse_goal(goal_str):
    if not re_goal.match(goal_str):
        raise ParseException(goal_str)
    goal_groups = re_goal.findall(goal_str)[0]
    term_name = goal_groups[0]
    term_params = re_goal_param.findall(goal_groups[1])
    return Term(term_name, term_params)