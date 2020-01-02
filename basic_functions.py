import re


def use_rule(sentence, rule):
    """
    If the rule is applicable to the sentence, apply rule for the first occurrence of left side of the rule,
    if not returns the same string
    :param sentence: (string) String we wan't use rule to
    :param rule: (string) Rule we wan't to use in format x -> y, where x, y any string
    :return: (string) String after the application of the rule
    """
    left_side, right_side = re.split(r'->', rule)
    result = re.sub(left_side, right_side, sentence, 1)
    return result


def concatenation(k, *string_sets):
    """
    Function returns k-length strings, made as concatenation of all combination of strings from string_sets taken
    in same order as parameters
    :param k: (int) max length of returned string
    :param string_sets: (set<string>) sets of string to take parts of string from(order is important)
    :return: (set<string>)set of k-length strings
    """
    result = set()
    for string_set in string_sets:
        if len(string_set) == 0:
            return result
    for current_set in string_sets:
        if len(result) == 0:
            result = {string[:k] for string in current_set}
        else:
            temp_set = set()
            for src_string in result:
                for string_for_append in current_set:
                    temp_set.add((src_string + string_for_append)[:k])
            result = temp_set
    return result





