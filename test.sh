#!/bin/bash
# Runs the test cases given in the assignment doc against regexpert.py
# and compares actual output to expected output.

pass=0
fail=0

run_case() {
    name="$1"
    input="$2"
    expected="$3"

    actual=$(printf '%s' "$input" | python3 main.py 2>/dev/null)

    if [ "$actual" == "$expected" ]; then
        echo "PASS: $name"
        pass=$((pass+1))
    else
        echo "FAIL: $name"
        echo "  expected: $(echo "$expected" | tr '\n' '|')"
        echo "  actual:   $(echo "$actual" | tr '\n' '|')"
        fail=$((fail+1))
    fi
}

# Worked example
run_case "worked example (ab*)" \
"ab*
a ab abb abbb c" \
"a
ab
abb
abbb"

# Test Case 1
run_case "[a-z]+ing" \
"[a-z]+ing
I was running while thinking about swimming laps." \
"running
thinking
swimming"

# Test Case 2
run_case "(a|b)*abb" \
"(a|b)*abb
aabb babb ab abb" \
"aabb
babb
abb"

# Test Case 3
run_case "[0-9]+(\.[0-9]+)?" \
'[0-9]+(\.[0-9]+)?
Price is 42 or 3.14 or item42' \
"42
3.14"

# Test Case 4
run_case "colou?r" \
"colou?r
I prefer color over colour, but colouur is a typo." \
"color"

# Test Case 5 (malformed regex, should produce no stdout + non-zero exit)
actual=$(printf '[\nanything' | python3 regexpert.py 2>/dev/null)
exit_code=$?
if [ -z "$actual" ] && [ "$exit_code" -ne 0 ]; then
    echo "PASS: malformed regex ([) errors correctly"
    pass=$((pass+1))
else
    echo "FAIL: malformed regex ([) did not error as expected"
    fail=$((fail+1))
fi

echo ""
echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
