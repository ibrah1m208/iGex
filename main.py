class Parser:
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
        left = L[0] #Combine into a nested (concat,left,right) node
        for right in L[1:]:
            left = ('concat', left, right)
        return left

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
        self.alphabet = set() # For Debug purposes

    def new_state(self): # Returns ID of new state
        self.state_counter += 1
        self.transitions[self.state_counter] = []
        return self.state_counter
    def add_transition(self, from_st, to_st, symbol=None): # If no symbol, then Epsilon Transition
        self.transitions[from_st].append((symbol, to_st))
        if symbol is not None:
            self.alphabet.add(symbol)

    def resolve_charClass(self, raw):
        chars = set()
        i,n = 0, len(raw)
        while i < n:
            if i+2 < n and raw[i+1] == '-':
                lo, hi = ord(raw[i]), ord(raw[i+2])
                if lo <= hi:
                    chars.update(chr(x) for x in range(lo, hi+1))
                i+=3
            else:
                chars.add(raw[i])
                i += 1
        return chars
    def build_nfa(self, node):
        node_type = node[0]
        if node_type == 'literal':
            s = self.new_state()
            a = self.new_state()
            self.add_transition(s, a, node[1])
            return (s, a)
        elif node_type == 'concat':
            l_node, r_node = node[1], node[2]
            s1, a1 = self.build_nfa(l_node)
            s2, a2 = self.build_nfa(r_node)
            self.add_transition(a1, s2)
            return (s1, a2)
        elif node_type == 'union':
            l_node, r_node = node[1], node[2]
            s1, a1 = self.build_nfa(l_node)
            s2, a2 = self.build_nfa(r_node)
            s = self.new_state()
            a = self.new_state()

            self.add_transition(s, s1)
            self.add_transition(s, s2)
            self.add_transition(a1, a)
            self.add_transition(a2, a)

            return (s, a)
        elif node_type == 'star':
            child = node[1]
            s1, a1 = self.build_nfa(child)
            s = self.new_state()
            a = self.new_state()

            self.add_transition(s, s1) # Start -> inside start
            self.add_transition(a1, s1) # Loop back
            self.add_transition(a1, a) # inside accept -> accept
            self.add_transition(s, a) # ignore and skip

            return (s, a)
        elif node_type == 'plus':
            # A+ ~= AA* here A is node[1]
            return self.build_nfa(('concat', node[1], ('star', node[1])))
        elif node_type == 'question':
            child = node[1]
            s1, a1 = self.build_nfa(child)
            s = self.new_state()
            a = self.new_state()

            self.add_transition(s,s1) # Path
            self.add_transition(a1, a) # Finish Path
            self.add_transition(s,a) # Skip bs and proceed
            return (s, a)
        elif node_type == 'group':
            return self.build_nfa(node[1]) # group is just an organized AST, so build NFA from ASY
        elif node_type == 'char_class':
            raw = node[1]
            chars = self.resolve_charClass(raw)
            s = self.new_state()
            a = self.new_state()
            for ele in chars:
                self.add_transition(s, a, ele)
            return (s, a)
        else:
            raise ValueError(f"Unknown type - {node_type}")

def main():
    INP_REGEX = input()
    TEXT = []
    for word in TEXT:
        # TODO
        # If Not valid, return -1 to stderr
        # If valid but reject, pass
        # If valid and accept, print(word)
        pass
    return 0
