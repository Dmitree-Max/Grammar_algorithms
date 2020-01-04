from basic_functions import *


def calc_not_terminal_table(grammar, k):
    """
    Calculates and returns dictionary with not-terminals as keys, and their firsts as value
    :param grammar: (Grammar) grammar we work with
    :param k: (int) characteristic of grammar
    :return: (dictionary<char, set<string>>) calculated dictionary with firsts
    """
    current_result = {}
    next_step_result = {}
    for symbol in grammar.not_terminals:
        calculate_first_for_not_terminal_zero_iteration(grammar, symbol, next_step_result, k)
    deep = 0
    while current_result != next_step_result:
        current_result = next_step_result.copy()
        for symbol in grammar.not_terminals:
            calculate_first_for_not_terminal_next(grammar, symbol, current_result, next_step_result, k)
        deep += 1
        if deep > 20:
            raise Exception("Attention! 20-depth recursion is reached")
    return current_result


def first(grammar, sentence, not_terminal_table={}, k=1):
    """
    Calculates and returns first for current sentence. To work need calculated not-terminal table
    :param grammar: (Grammar) grammar we work with
    :param sentence: (string) string to calculate first to
    :param not_terminal_table: (dictionary<char, set<string>>) basically produced by calc_not_terminal_table
    :param k: (int) characteristic of grammar
    :return: (set<string>) first value for sentence
    """
    if len(sentence) == 0:
        result = set()
        result.add('')
        return result
    if len(not_terminal_table) == 0:
        not_terminal_table = calc_not_terminal_table(grammar, k)
    symbols = re.findall(r'.', sentence)
    final_sets = [first_for_symbol(grammar, symbol, not_terminal_table) for symbol in symbols]
    result = concatenation(k, *final_sets)
    return result


def first_for_symbol(grammar, symbol, not_terminal_table):
    """
    Calculates and returns first for current symbol. To work need calculated not-terminal table
    :param grammar: (Grammar) grammar we work with
    :param symbol: (char) symbol to calculate first to
    :param not_terminal_table: (dictionary<char, set<string>>) basically produced by calc_not_terminal_table
    :return: (set<string>) first value for symbol
    """
    result = set()
    if symbol in grammar.terminals:
        result.add(symbol)
    elif symbol in grammar.not_terminals:
        result = not_terminal_table[symbol]
    else:
        raise Exception("Symbol %c not in grammars alphabets" % symbol)
    return result


def calculate_first_for_not_terminal_zero_iteration(grammar, symbol, this_result, k):
    """
    Calculates and writes into this_result zero iteration first of not terminal symbol
    :param grammar: (Grammar) grammar we work with
    :param symbol: (char) not-terminal to calculate first to
    :param this_result: (dictionary) dictionary to write result to, can store previous result,
    because it it subsets of current result we expect
    :param k: (int) characteristic of grammar
    :return: none
    """
    result = set()
    for rule in grammar.rules:
        produced_string = use_rule(symbol, rule)
        if is_the_beginning_terminals(produced_string, grammar.terminals, k):
            result.add(produced_string[:k])
    this_result[symbol] = result
    return


def calculate_first_for_not_terminal_next(grammar, symbol, previous_result, this_result, k):
    """
    Calculates and writes into this_result some iteration first of not terminal symbol. Bases on result of
    previous iteration "previous result"
    :param grammar: (Grammar) grammar we work with
    :param symbol: (char) not-terminal to calculate first to
    :param previous_result: (dictionary<char, set<string>>) result of previous iteration in same format
    :param this_result: (dictionary) dictionary to write result to, can store previous result,
    because it it subsets of current result we expect
    :param k: (int) characteristic of grammar
    :return: none
    """
    result = set()
    for rule in grammar.rules:
        temp_string = use_rule(symbol, rule)
        if temp_string == symbol:
            continue
        symbols = re.findall(r'.', temp_string)
        symbols_firsts = [first_for_symbol(grammar, symbol, previous_result) for symbol in symbols]
        temp_result = concatenation(k, *symbols_firsts)
        result = result.union(temp_result)
    result = result.union(previous_result[symbol])
    this_result[symbol] = result


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


