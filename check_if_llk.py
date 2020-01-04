import re
import first
import basic_functions
import sigma_hatch
import time

def split_rules_by_not_terminals(grammar):
    """
    Returns dictionary with not terminals which has at least two alternatives as a key, and set of
    these alternatives as a value
    :param grammar: (Grammar) grammar to inspect
    :return: (dictionary<char, set<string>>) not terminals and alternatives
    """
    result = {}
    for nt in grammar.not_terminals:
        result[nt] = set()
    for rule in grammar.rules:
        left_side, right_side = re.split(r'->', rule)
        if left_side in grammar.not_terminals:
            result[left_side].add(right_side)
        else:
            raise Exception("Left side of rule is not not-terminal")
    for nt in grammar.not_terminals:
        if(len(result[nt])) < 2:
            result.pop(nt)
    return result


def is_grammar_llk(grammar, k):
    nt_with_alternatives = split_rules_by_not_terminals(grammar)
    # time1 = time.time()
    sigmas = sigma_hatch.sigma_hatch(grammar, k)
    # time2 = time.time()
    table = first.calc_not_terminal_table(grammar, k)
    # time3 = time.time()
    # print("sigmas:  " + str(time2 - time1) + '   firsts:   ' + str(time3 - time2))
    for nt in nt_with_alternatives.keys():
        current_sigma = sigmas[grammar.start_symbol + nt]
        for x in nt_with_alternatives[nt]:
            for y in nt_with_alternatives[nt]:
                if x == y:
                    continue
                for l_element in current_sigma:
                    first_part = basic_functions.concatenation(k, first.first(grammar, x, table, k), l_element)
                    second_part = basic_functions.concatenation(k, first.first(grammar, y, table, k), l_element)
                    intersect = first_part.intersection(second_part)
                    if len(intersect) > 0:
                        return "Нет"
    return "Да"


