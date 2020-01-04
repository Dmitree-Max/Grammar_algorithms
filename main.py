from Grammar import GrammarBuilder
from first import *
from basic_functions import *
from sigma_hatch import *
from check_if_llk import *


builder = GrammarBuilder()
builder.config_from_file("g2.txt")
g1 = builder.make_grammar()
g1.print_grammar()
print("-----------------------------------")

for k in range(1, 5):
    answer = is_grammar_llk(g1, k)
    print("Является ли грамматика ll(%i)?       " % k + answer)
