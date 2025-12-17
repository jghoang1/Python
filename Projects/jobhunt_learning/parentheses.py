"""
Here is a classic SDET coding challenge. This problem is popular because it tests your understanding of **data structures** (specifically Stacks)
and your ability to validate syntax—something you do constantly when parsing JSON responses or checking code integrity.

###The Challenge: Valid Parentheses**Problem Statement:**
Given a string `s` containing just the characters `(`, `)`, `{`, `}`, `[` and `]`, determine if the input string is valid.

An input string is valid if:

1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.

**Examples:**

* **Input:** `s = "()"` \rightarrow **Output:** `true`
* **Input:** `s = "()[]{}"` \rightarrow **Output:** `true`
* **Input:** `s = "(]"` \rightarrow **Output:** `false`
* **Input:** `s = "([)]"` \rightarrow **Output:** `false` (Must close in the correct order)
* **Input:** `s = "{[]}"` \rightarrow **Output:** `true`
"""


def is_valid(input_string: str) -> bool:
    """
    Determines if a string with the characters `(`, `)`, `{`, `}`, `[` and `]`
    is valid.
    """
    matching_opener = {
        "}": "{",
        ")": "(",
        "]": "[",
    }
    stack = []
    for char in input_string:
        if char in r"({[":
            # add to stack
            stack.append(char)
        elif char in r")}]":
            if not stack:
                # If closing bracket is first element, string is not valid
                return False
            prev_char = stack.pop()
            if matching_opener[char] != prev_char:
                return False
            # pop, and check for validity

        else:
            raise ValueError(f"{char} is not a valid character")
    return not stack


def is_valid_solution(s: str) -> bool:
    # Map closer to opener
    matching_opener = {
        "}": "{",
        ")": "(",
        "]": "[",
    }
    stack = []

    for char in s:
        # Check if it is a closer
        if char in matching_opener:
            # If stack is empty, we have a closer with no opener -> False
            if not stack:
                return False

            # Pop the top element
            top_element = stack.pop()

            # If the popped opener doesn't match the current closer -> False
            if matching_opener[char] != top_element:
                return False
        else:
            # It's an opener, push to stack
            stack.append(char)

    # CRITICAL: Return True only if stack is empty
    return not stack


if __name__ == "__main__":
    tests = {
        r"({[{}]})": True,
        r"((((()))))": True,
        r"){}": False,
        r"{([(])}": False,
        r"{{{": False,
    }

    for input_string, expected_validity in tests.items():
        assert is_valid(input_string) == expected_validity, (
            f"Expected validity to be {expected_validity} for string '{input_string}'"
        )
