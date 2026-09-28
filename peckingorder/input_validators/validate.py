#validate.py
#input format validator for pecking order
#reads one test input on stdin, exits 42 if it matches the spec exactly, 43 if not
#(the problemtools convention). strict on whitespace: single spaces between numbers,
#every line ends in "\n", nothing after the last line
#
#checks:
#  line 1: "N M" with 1 <= N <= 2*10^5 and 0 <= M <= 2*10^5
#  then exactly M lines "a b" with 1 <= a, b <= N and a != b
import re
import sys

MAX_N = 200000
MAX_M = 200000

#integer with no leading zeros or plus sign
INT = r"(0|[1-9][0-9]*)"
LINE = re.compile(rb"^" + INT.encode() + rb" " + INT.encode() + rb"$")


#bail out with the reject code and a reason on stderr
def reject(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(43)


#parse "x y" from one line, or reject
def two_ints(line, lineno):
    match = LINE.match(line)
    if not match:
        reject(f"line {lineno}: expected two integers separated by one space, got {line[:40]!r}")
    return int(match.group(1)), int(match.group(2))


def main():
    data = sys.stdin.buffer.read()
    if not data.endswith(b"\n"):
        reject("input must end with a newline")
    lines = data[:-1].split(b"\n")

    n, m = two_ints(lines[0], 1)
    if not 1 <= n <= MAX_N:
        reject(f"N = {n} out of range")
    if not 0 <= m <= MAX_M:
        reject(f"M = {m} out of range")
    if len(lines) != m + 1:
        reject(f"expected {m} entry lines, found {len(lines) - 1}")

    #each log entry
    for i in range(1, m + 1):
        a, b = two_ints(lines[i], i + 1)
        if not (1 <= a <= n and 1 <= b <= n):
            reject(f"line {i + 1}: swan number out of range")
        if a == b:
            reject(f"line {i + 1}: a swan cannot displace itself")

    sys.exit(42)


if __name__ == "__main__":
    main()
