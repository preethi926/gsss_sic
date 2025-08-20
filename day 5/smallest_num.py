def next_bigger_number(n):
    digits = list(str(n))
    i = len(digits) - 2

    # Step 1: Find pivot
    while i >= 0 and digits[i] >= digits[i + 1]:
        i -= 1

    if i == -1:
        return "No higher permutation possible"

    # Step 2: Find successor
    j = len(digits) - 1
    while digits[j] <= digits[i]:
        j -= 1

    # Step 3: Swap
    digits[i], digits[j] = digits[j], digits[i]

    # Step 4: Reverse suffix
    digits[i + 1:] = reversed(digits[i + 1:])

    return int(''.join(digits))

# Example usage
print(next_bigger_number(218765))  # Output: 251678