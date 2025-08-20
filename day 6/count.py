def is_balanced_braces(s):
    stack = []
    for char in s:
        if char == '{':
            stack.append(char)
        elif char == '}':
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0

input_str = "{{{}{}}}"
print("Balanced" if is_balanced_braces(input_str) )else "Not Balanced")


import sys

input_str = sys.argv[1]
print(f'user given input is {input_str}')
