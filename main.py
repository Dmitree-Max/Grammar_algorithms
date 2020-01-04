from Grammar import GrammarBuilder
from first import *
from basic_functions import *
from sigma_hatch import *
from check_if_llk import *


builder = GrammarBuilder()
builder.config_from_file("g1.txt")
g = builder.make_grammar()
g.print_grammar()
print("-----------------------------------")

for k in range(1, 7):
    answer = is_grammar_llk(g, k)
    print("Является ли грамматика ll(%i)?       " % k + answer)
print("-----------------------------------")
# print(first.first(g, "E", k=1))
# print(first.first(g, "R", k=1))
# print(first.first(g, "T", k=1))
# print(first.first(g, "G", k=1))
# print(first.first(g, "F", k=1))
