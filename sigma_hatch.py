import re
import first
import basic_functions


def sigma_hatch_zero_level(a, b, grammar, this_result, table, k):
    """
    Functions adds into dictionary this_result note with key a + b and value as sigma hatch function value
     on zero iteration of a and b not terminals
    :param a: (char) not terminal
    :param b: (char) not terminal
    :param grammar: (Grammar) grammar to take rules from
    :param this_result: (dictionary<string, set<string>>) dictionary to write result to, can store previous result,
    because it it subsets of current result we expect
    :param table: (dictionary<string, set<string>>) table with calculated firsts for all not-terminals
    :param k: (int) characteristic of ll(k) grammars
    :return: none
    """
    result = set()
    for rule in grammar.rules:
        after_rule_string = basic_functions.use_rule(a, rule)
        if after_rule_string == a:
            continue
        # print(after_rule_string)
        all_endings = []
        while len(re.findall(b, after_rule_string)) > 0:
            after_rule_string = re.split(b, after_rule_string, 1)[1]
            all_endings.append(after_rule_string)
        # print(all_endings)
        for ending in all_endings:
            # print(First.first(grammar, ending, table, k))
            result = result.union(first.first(grammar, ending, table, k))
            # print("result: " + str(result))
    this_result[a + b] = result
    return


def sigma_hatch_next_level(a, b, grammar, previous_result, this_result, table, k):
    """
    Functions adds into dictionary this_result note with key a + b and value as sigma hatch function value
     on some iteration of a and b not terminals, bases on previous iteration result from previous_result
     parameter
    :param a: (char) not terminal
    :param b: (char) not terminal
    :param grammar: (Grammar) grammar to take rules from
    :param previous_result: (dictionary<string, set<string>>) dictionary with result from previous iteration
    :param this_result: (dictionary<string, set<string>>) dictionary to write result to, can store previous result,
    because it it subsets of current result we expect
    :param table: (dictionary<string, set<string>>) table with calculated firsts for all not-terminals
    :param k: (int) characteristic of ll(k) grammars
    :return: none
    """
    result = set()
    for rule in grammar.rules:
        after_rule_string = basic_functions.use_rule(a, rule)
        if after_rule_string == a:
            continue
        all_endings = []
        nt = find_first_not_terminal(after_rule_string, grammar.not_terminals)
        while nt != '':
            after_rule_string = re.split(nt, after_rule_string, 1)[1]
            all_endings.append([nt, after_rule_string])
            nt = find_first_not_terminal(after_rule_string, grammar.not_terminals)
        for ending in all_endings:
            l_hatch = previous_result[ending[0] + b]
            temp_result = first.first(grammar, ending[1], table, k)
            result = result.union(first.concatenation(k, l_hatch, temp_result))
    result.union(previous_result[a + b])
    this_result[a + b] = result
    return


def sigma_hatch(grammar, k):
    """
    Calculates sigma hatch function for all pairs of not terminals from the grammar and returns dictionary
    with result, which has not terminal + not terminal string as a key, and sigma hatch function of them
    as value
    :param grammar: (Grammar) grammar to take rules and all not terminals from
    :param k: (int) characteristic of ll(k) grammars
    :return: (dictionary<string, set<string>>) dictionary with result
    """
    table = first.calc_not_terminal_table(grammar, k)
    current_table = {}
    next_step_table = {}
    for a in grammar.not_terminals:
        for b in grammar.not_terminals:
            sigma_hatch_zero_level(a, b, grammar, next_step_table, table, k)
    deep = 0
    while current_table != next_step_table:
        current_table = next_step_table
        for a in grammar.not_terminals:
            for b in grammar.not_terminals:
                sigma_hatch_next_level(a, b, grammar, current_table, next_step_table, table, k)
        # print(next_step_table)
        deep += 1
        if deep == 20:
            raise Exception("Attention, 20-depth has been reached")
    return current_table


def find_first_not_terminal(string, not_terminals):
    """
    Finds and returns first not terminal from the string, if there is no not terminal in the string returns ''
    :param string: (string) String to find in
    :param not_terminals: (list<char>) list of not terminals
    :return: (char) first met not terminal in the string
    """
    for symbol in string:
        if symbol in not_terminals:
            return symbol
    return ''





