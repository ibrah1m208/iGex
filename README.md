# iGex - A regex implementation in python

A regex engine in python
Made for an Automaton course exercise

## Description
- **iGex** reads a regular expression and a block of text from standard input, and prints every word in the text that fully matches the expression. The expression is parsed, into an NFA using Thompson's construction, then converted to a DFA using subset construction.
- **Debug Mode** prints a DFA transition table to `stderr` in CSV format

## Run
**Usage**
```
python3 main.py [--debug] < input.txt
```
**Input format** first line is the regex, remaining lines are the text block (read until EOF).
```bash
python3 main.py < input.txt
```

Interactive (type the regex, then the text, then Ctrl+D for EOF):
```bash
python3 main.py
```
