#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Oleg Beloglazov'


class Node:
    """ Класс узла дерева """

    NODE_LINE_PATTERN = '%s'
    CONNECTION_ELEMENT = '_'

    def __init__(self, childs=[], value=None):
        self.value = value
        self.childs = childs

    def to_strings(self):
        """ Возвращает список строк текстового представления дерева """

        node_line = self.NODE_LINE_PATTERN % str(self.value)
        child_connection = ' |' + self.CONNECTION_ELEMENT * len(node_line) + ' '
        child_space = ' |' + ' ' * (len(node_line) + 1)
        lines = [node_line]
        i = 0
        while i < len(self.childs):
            lines.append(child_space)
            lines.append(child_connection)
            child_lines = self.childs[i].to_strings()
            lines[-1] += child_lines[0]
            for child_line in child_lines[1:]:
                if i + 1 != len(self.childs):
                    lines.append(child_space + child_line)
                else:
                    lines.append(' ' * len(child_space) + child_line)
            i += 1
        return lines


    def __str__(self):
        return '\n'.join(self.to_strings())


class AndNode(Node):
    NODE_LINE_PATTERN = '[%s]'


class OrNode(Node):
    NODE_LINE_PATTERN = '(%s)'


class KnowledgeBase:
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules

    def __str__(self):
        return '\n'.join([str(stmt) for stmt in (self.facts + self.rules)])


class Term:
    def __init__(self, name, params):
        self.name = name
        self.params = params

    def equivalent(self, rename_dict):
        """ Создать эквивалентный терм, т.е. такое же, но с переименованными параметрами согласно rename_dict """

        params = [rename_dict[param] if param in rename_dict else param for param in self.params]
        return Term(self.name, params)


    def fits(self, other):
        """ Проверить, являются ли термы синонимами. """

        return self.name == other.name and len(self.params) == len(other.params)


    def __str__(self):
        return '%s(%s)' % (self.name, ', '.join(self.params))

    def __repr__(self):
        return str(self)


class Fact:
    def __init__(self, name, constants):
        self.name = name
        self.constants = tuple(constants)

    def fits(self, term):
        """ Проверить подходит ли данный факт под терм. """

        if self.name != term.name or len(self.constants) != len(term.params):
            return False

        params_dict = dict.fromkeys(term.params)

        for i in xrange(len(term.params)):
            cur_param = term.params[i]
            if params_dict[cur_param] and params_dict[cur_param] != self.constants[i]:
                return False
            else:
                params_dict[cur_param] = self.constants[i]
        return True

    def __str__(self):
        return '%s(%s)' % (self.name, ', '.join(self.constants))

    def __repr__(self):
        return str(self)


class Rule:
    def __init__(self, pos_term, neg_terms):
        self.pos_term = pos_term
        self.neg_terms = neg_terms

    def equivalent(self, rename_dict):
        """ Создать эквивалентное правило, т.е. такое же, но с переименованными параметрами согласно rename_dict """

        return Rule(self.pos_term.equivalent(rename_dict), [term.equivalent(rename_dict) for term in self.neg_terms])

    def substitute(self, subst_term):
        """ Создать эквивалентную копию правила, совместимую по параметрам с subst_term """

        if self.pos_term.fits(subst_term):
            rename_dict = dict(zip(self.pos_term.params, subst_term.params))
            return self.equivalent(rename_dict)

    def __str__(self):
        return '%s <- %s.' % (self.pos_term, '; '.join([str(term) for term in self.neg_terms]))

    def __repr__(self):
        return str(self)