import re
import First
from Grammar import GrammarBuilder
import basic_functions


def sigma_hatch(a, b, grammar, deep, k):
    result = set()
    if deep == 0:
        table = First.calc_not_terminal_table(grammar, k)
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
                result = result.union(First.first(grammar, ending, table, k))
                # print("result: " + str(result))
    return result



"""
builder = GrammarBuilder()
builder.add_not_terminals(["S", "A", "B"])
builder.add_terminals(["a", "b"])
builder.add_rules(("S->aB", "S->bA", "A->a", "B->b", "A->bAA", "B->aBB", "A->aS", "B->bS"))
builder.set_start_symbol("S")


builder181 = GrammarBuilder()
builder181.add_not_terminals(["E", "R", "T", "G", "F"])
builder181.add_terminals(["a", "+", "*", "(", ")"])
builder181.add_rules(("E->TR", "R->+TR", "R->", "T->FG", "G->*FG", "G->", "F->(E)", "F->a"))
builder181.set_start_symbol("E")
g = builder181.make_grammar()
# g.print_grammar()
"""

builder184 = GrammarBuilder()
builder184.add_not_terminals(["S", "A"])
builder184.add_terminals(["a", "b"])
builder184.add_rules(("S->AS", "S->", "A->aA", "A->b"))
builder184.set_start_symbol("S")
g = builder184.make_grammar()

ttable = First.calc_not_terminal_table(g, 1)
print(First.first(g, "", ttable, 1))
res1 = sigma_hatch("S", "S", g, 0, 1)
print(res1)
res2 = sigma_hatch("S", "A", g, 0, 1)
print(res2)
res3 = sigma_hatch("A", "S", g, 0, 1)
print(res3)
res4 = sigma_hatch("A", "A", g, 0, 1)
print(res4)



