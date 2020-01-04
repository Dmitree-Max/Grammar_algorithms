import re


class Grammar:
    def __init__(self, not_terminals, terminals, rules, start_symbol):
        self.not_terminals = not_terminals
        self.terminals = terminals
        self.rules = rules
        self.start_symbol = start_symbol

    def print_grammar(self):
        print(vars(self))


class GrammarBuilder:
    def __init__(self):
        self.not_terminals = []
        self.terminals = []
        self.rules = []
        self.start_symbol = ""

    def add_not_terminals(self, new_not_terminals):
        self.not_terminals.extend(new_not_terminals)

    def add_terminals(self, new_terminals):
        self.terminals.extend(new_terminals)

    def add_rules(self, new_rules):
        self.rules.extend(new_rules)

    def set_start_symbol(self, start_symbol):
        self.start_symbol = start_symbol

    def config_from_file(self, file_name):
        with open(file_name, 'r') as file:
            content = file.read()
        content = content.replace(" ", "")
        parts = re.findall(r'{(.*)}', content)
        parts_order = ['not_terminals', 'terminals', 'rules', 'start_symbol']
        for i in range(4):
            elements = re.split(r',', parts[i])
            self.__setattr__(parts_order[i], elements)
            if i == 3:
                self.__setattr__(parts_order[i], elements[0])

    def make_grammar(self):
        if self.start_symbol not in self.not_terminals:
            raise Exception('Start_symbol %c not in not_terminals ' % self.start_symbol + str(self.not_terminals))
        return Grammar(self.not_terminals, self.terminals, self.rules, self.start_symbol)



