class parser:
    def __init__(self, inp_rgx):
        self.inp_rgx = inp_rgx
        self.index = 0
    
    def parse(self): # Entry Point for parsing the expression
        AST = self.parse_union()
        if self.peek() is not None: # If finished parsing but characters left
            raise ValueError(f"Syntax Error: position {self.index} - {self.peek()}") # That means syntax error
        return AST
    
    def peek(self):
        if self.index < len(self.inp_rgx):
            return self.inp_rgx[self.index]
        return None

    def consume(self, expected_char=None): # Can have 0 arguments for normal, or 1 argument to check if valid
        char=self.peek()
        if expected_char is not None and char != expected_char: # Safety check to see if Bad Expression
            raise ValueError(f"Bad Expression: expected '{expected_char}', got '{char}'")
        self.index += 1
        return char

    def parse_union(self):
        left = self.parse_concat()
        while self.peek() == '|':
            self.consume('|')
            right = self.parse_concat()
            left = ('union', left, right)
        return left

    def parse_concat(self):
        L = [] #Keep parsing as long as we dont get | or )
        while self.peek() is not None and self.peek() not in ('|', ')'):
            L.append(self.parse_repeat())
        if not L:
            raise ValueError("Empty Expression")
        if len(L) == 1:
            return L[0]
        l = L[0] #Combine into a nested (concat,l,r) node
        for r in L[1:]:
            l = ('concat', l, r)
        return l

    def parse_repeat(self):
        literal = self.parse_literal()
        while self.peek() in ['+','*','?']: #consume operator and proceed
            op = self.consume()
            if op == '*':
                literal = ('star', literal)
            elif op == '+':
                literal = ('plus', literal)
            elif op == '?':
                literal = ('question', literal)
            if self.peek() in ('+', '*', '?'):
                raise ValueError("Parse error - Stacked Quantifiers")
        return literal

    def parse_literal(self):
        char = self.peek()
        if char is None:
            raise ValueError("Unexpected happenings happened unexpectedly")
        if char == '(':
            self.consume(char)
            node = self.parse_union()
            self.consume(')') # Expected consume the closing bracket. else raises error within
            return ('group', node)
        if char == '[': # TODO - handle classes such as [0-9] and [a-z]
            charset = []
            self.consume(char)
            while self.peek() is not None and self.peek() != ']':
                # Handle backslashes
                if self.peek() == '\\':
                    self.consume('\\')
                    charset.append(self.consume())
                else:
                    charset.append(self.consume())
            if not charset:
                raise ValueError("Empty Character Class")
            self.consume(']')
            return ('char_class', "".join(charset))
        

        if char == '\\':
            self.consume('\\')
            escaped = self.peek()
            if escaped is None:
                raise ValueError("Trailing Backslash")
            self.consume()
            return ('literal', escaped)    
        else:
            return ('literal', self.consume())



class NFACompiler:
    def __init__(self):
        self.state_counter = 0
        self.transitions = {} # epsilon transitions will be denoted by None
    
    def new_state(self): # Returns ID of new state
        self.state_counter += 1
        self.transitions[self.state_counter] = []
        return self.state_counter
    def add_transition(self, from_st, to_st, symbol, epsilon=False):
        if not epsilon:
            self.transitions[from_st].append((symbol, to_st))
        else:
            self.transitions[from_st].append((None, to_st))
    


def main():
    INP_REGEX = str(input())
    TEXT = []
    for word in TEXT:
        # TODO
        # If Not valid, return -1 to stderr
        # If valid but reject, pass
        # If valid and accept, print(word)
        pass
    return 0
