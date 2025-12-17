"""
###The Challenge: Longest Valid Parentheses**Problem Statement:**
Given a string `s` containing just the characters `'('` and `')'`, find the length of the **longest valid (well-formed) parentheses substring**.

A valid parentheses substring is one that adheres to the rules of well-formedness (e.g., matching pairs and correct order).

**Examples:**

* **Input:** `s = "(()"`
* The valid substring is `"()"`
* **Output:** `2`


* **Input:** `s = ")()())"`
* The valid substrings are `"()"` and `"()"`
* The longest is the concatenation: `"()()"`
* **Output:** `4`


* **Input:** `s = ""`
* **Output:** `0`


* **Input:** `s = "()(()"`
* The longest valid substring is `"()"`
* **Output:** `2`



---

###Your TurnHow would you approach solving this?

* **Hint:** The key is to use a Stack, but instead of pushing the bracket characters, push the **index** of the bracket. This allows you to calculate the length of a valid substring every time you find a match.
* **Initial Stack State:** It's helpful to start the stack with an index of `-1`. This acts as a placeholder for the start of the current potential valid substring.

(Take your time, draft the logic, and paste your solution here!)
"""


def longest_valid_parentheses(s: str) -> int:
    """Naive Solution O(n**2)"""
    # Naive solution: iterate through s starting from each index : O(n**2)
    longest_valid = 0
    for idx_i in range(len(s)):
        count = 0
        for idx_f in range(idx_i, len(s)):
            if s[idx_f] == "(":
                count += 1
            else:
                count -= 1
                if count < 0:
                    # Invalid, as there are now closers without preceding openers
                    break
                elif count == 0:
                    # Found valid substring; check if it's the longest so far
                    longest_valid = max(longest_valid, idx_f - idx_i + 1)
    return longest_valid


def longest_valid_parentheses_ON(s: str) -> int:
    """O(n) Solution"""
    # Stack stores the indices of characters.
    # We start with -1 as a base marker for calculating the length of the first valid substring.
    stack = [-1]
    max_length = 0

    for i in range(len(s)):
        if s[i] == "(":
            stack.append(i)
        else:
            top_idx = stack.pop()
            if stack:
                max_length = max(max_length, i - stack[-1])
            else:
                # Ran into un-matched ")". This index will be the new base marker
                stack.append(i)
    return max_length



def longest_valid_parentheses_ON_Solution(s: str) -> int:
    """"Solution"""
    # Stack stores the indices of characters.
    # We start with -1 as a base marker for calculating the length of the first valid substring.
    stack = [-1]
    max_length = 0

    for i in range(len(s)):
        if s[i] == "(":
            # If it's an opening parenthesis, push its index onto the stack.
            stack.append(i)
        else: # s[i] == ")"
            # Always pop when a closing parenthesis is encountered.
            stack.pop()

            if stack:
                # If the stack is NOT empty, we found a valid pair.
                # The length is current index minus the index of the new top element (the last unmatched '(' or the base marker -1).
                # The stack.pop() removes the corresponding '(', so stack.top() is the index
                # immediately before the valid sequence began.
                max_length = max(max_length, i - stack[-1])
            else:
                # If the stack IS empty after popping, it means this ')' is unmatched.
                # It becomes the new boundary/base marker for future valid sequences.
                stack.append(i)
    return max_length

if __name__ == "__main__":
    tests = {
        "(()": 2,
        ")()())": 4,
        "": 0,
        "()(()": 2
    }
    for input_string, expected_longest in tests.items():
        res = longest_valid_parentheses_ON(input_string)
        assert res == expected_longest, f"Expected longest valid subtring of length {expected_longest} for string {input_string}.\n\tGot {res}"