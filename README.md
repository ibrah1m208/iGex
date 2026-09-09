# iGex - A regex implementation in python

A regex engine: parses a regular expression, builds an NFA (Thompson's construction),
converts it to a DFA (subset construction), and matches words from an input text block.

Made for an Automaton course exercise


## Run

Input format: first line is the regex, remaining lines are the text block (read until EOF).

```bash
python3 regexpert.py < input.txt
```

With the DFA transition matrix printed to stderr:

```bash
python3 regexpert.py --debug < input.txt
```

To separate matches (stdout) from the debug matrix (stderr) into files:

```bash
python3 regexpert.py --debug < input.txt 1>matches.txt 2>debug.csv
```

Interactive (type the regex, then the text, then Ctrl+D for EOF):

```bash
python3 regexpert.py
```

## Test

Run the provided test cases from the assignment doc:

```bash
./test.sh
```
