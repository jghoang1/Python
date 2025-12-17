"""
You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

Write a function to compute the number of combinations that make up that amount. Assume that you have an infinite number of each kind of coin.

The result is guaranteed to fit in a 32-bit integer.

Example:
Input: amount = 5, coins = [1, 2, 5]
Output: 4
Explanation: There are four ways to make up the amount:
1. 5 = 5
2. 5 = 2 + 2 + 1
3. 5 = 2 + 1 + 1 + 1
4. 5 = 1 + 1 + 1 + 1 + 1


Constraints:

1 <= coins.length <= 500
1 <= coin[i] <= 5000
0 <= amount <= 5000
"""


def coin_count_dp(amount: int, coins: list[int]) -> int:
    N = len(coins)
    dp = [[0 for _ in range(amount + 1)] for _ in range(N + 1)]

    # Base case
    # any set of coins can make an amount of 0
    for i in range(N + 1):
        dp[i][0] = 1

    # General case
    for i in range(1, N + 1):
        coin_value = coins[i - 1]
        for j in range(amount + 1):
            # For any coin, we can either include or exclude it

            # Include coin
            # Depends on count of j-(coin_value) for same subset of coins
            count_including_coin = (
                dp[i][j - coin_value] if coin_value <= j else 0
            )

            # Exclude coin
            # Depends on count of same amount, but without that coin
            count_excluding_coin = dp[i - 1][j]

            dp[i][j] = count_including_coin + count_excluding_coin
    return dp[N][amount]


def main():
    tests = [
        {"amount": 5, "coins": [1, 2, 5], "result": 4},
        {"amount": 2, "coins": [9], "result": 0},
        {"amount": 0, "coins": [1, 2, 5], "result": 1},
        {"amount": 10, "coins": [1, 2, 5], "result": 10},
        {"amount": 10, "coins": [2, 3, 5], "result": 4},
    ]

    for test in tests:
        amount = test["amount"]
        coins = test["coins"]
        result = test["result"]
        actual = coin_count_dp(amount, coins)
        assert actual == result, (
            f"Test case: \n\tAmount : {amount} \n\tCoins: {coins} \nExpected {result}. Got {actual}"
        )


if __name__ == "__main__":
    main()
