import re
from Grammar import GrammarBuilder
from basic_functions import *


def calc_not_terminal_table(grammar, k):
    not_terminals = grammar.not_terminals
    symbols_firsts_next = {symbol: first_for_symbol(grammar, symbol, 0, k) for symbol in not_terminals}
    symbols_firsts = []
    deep = 0
    while symbols_firsts != symbols_firsts_next:
        symbols_firsts = symbols_firsts_next
        symbols_firsts_next = {symbol: first_for_symbol(grammar, symbol, deep + 1, k) for symbol in not_terminals}
        deep += 1
    return symbols_firsts


def first(grammar, sentence, not_terminal_table, k):
    if len(not_terminal_table) == 0:
        raise Exception("Forgot to calculate not_terminal_table")
    symbols = re.findall(r'.', sentence)
    final_sets = [not_terminal_table[symbol] if symbol in grammar.not_terminals else {symbol} for symbol in symbols]
    result = concatenation(k, *final_sets)
    result.add('')
    return result


def first_for_symbol(grammar, symbol, deep, k):
    result = set()
    if symbol in grammar.terminals:
        result.add(symbol)
    elif symbol in grammar.not_terminals:
        result = first_for_not_terminal(grammar, symbol, deep=deep, k=k)
    else:
        raise Exception("Symbol not in grammars alphabets")
    return result


def first_for_not_terminal(grammar, symbol, deep, k):
    result = set()
    if deep == 0:
        for rule in grammar.rules:
            produced_string = use_rule(symbol, rule)
            if is_the_beginning_terminals(produced_string, grammar.terminals, k):
                result.add(produced_string[:k])
    else:
        for rule in grammar.rules:
            temp_string = use_rule(symbol, rule)
            if temp_string == symbol:
                continue
            symbols = re.findall(r'.', temp_string)
            symbols_firsts = [first_for_symbol(grammar, symbol, deep - 1, k) for symbol in symbols]
            # print(temp_string + str(symbols) + str(symbols_firsts) + "   " + rule)
            temp_result = concatenation(k, *symbols_firsts)
            result = result.union(temp_result)
        result = result.union(first_for_not_terminal(grammar, symbol, deep - 1, k))
    return result


def is_the_beginning_terminals(string, terminals, k):
    """
    Checks if the first k symbols are terminals.
    :param string: (string) string to check
    :param terminals: (list<char>) list of terminals
    :param k: (int) amount of symbols which should be terminals
    :return: (bool) True if k first symbols are terminals, otherwise returns False
    """
    amount = min(k, len(string))
    for i in range(amount):
        if string[i] not in terminals:
            return False
    return True


