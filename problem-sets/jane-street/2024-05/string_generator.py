def generate_masks(n):
    def helper(current_string, length):
        if length == n:
            yield current_string
        else:
            if not current_string or current_string[-1] == "0":
                yield from helper(current_string + "1", length + 1)
            yield from helper(current_string + "0", length + 1)

    return helper("", 0)


# Test the function
for s in generate_masks(5):
    print(s)
