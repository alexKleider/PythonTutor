#!/usr/bin/env python3

# File: consec0s.py

"""
Regarding a PythonTutor thread.
Provides a means of counting the longest continuous series
of a particular character in a specified string.
Default is the character '0' (hence the name.)
"""

def get_longest(s, c='0'):
    """
    <s> is a sequence of characters.
    Returned is the length of the longest
    uniterupted sequence of the character <c>
    (default value for <c> is '0'.
    """
    extra_char = '_'
    if c == extra_char: extra_char = '-'
    b = longest = 0
    for ch in s + extra_char:
        if ch == c:
            b += 1
        else:
            if b > longest:
                longest = b
            b = 0
    return longest


def test_get_longest(test_data):
    print("Result  Argument")
    print("======  ========")
    for s in test_data:
        print("{:>6}, {}".format(get_longest(s), repr(s)))


test_data = (
"10100100011110000",
"00001010010001111",
"10100100011001100",
"",
"1111111111",
"0000000000",
'1',
'0',
)


if __name__ == "__main__":
    test_get_longest(test_data)
