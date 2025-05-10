# longest common string / sequences / parent-pointer

# Findout logest common sequence between the two words


WORDS_1 = "artsocca"
WORDS_2 = "heartbeat"

N = len(WORDS_1)
M = len(WORDS_2)

lcs_memo = [[0 for j in range(M + 1)] for i in range(N + 1)]


def longest_common_sequence_length(M, N):
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            if WORDS_1[i - 1] == WORDS_2[j - 1]:
                lcs_memo[i][j] = lcs_memo[i - 1][j - 1] + 1
            else:
                lcs_memo[i][j] = max(lcs_memo[i - 1][j], lcs_memo[i][j - 1])
    return lcs_memo[N][M]


def get_lcs(i, j):
    if i == 0 or j == 0:
        return ""
    if WORDS_1[i - 1] == WORDS_2[j - 1]:
        return get_lcs(i - 1, j - 1) + WORDS_1[i - 1]
    elif lcs_memo[i - 1][j] > lcs_memo[i][j - 1]:
        return get_lcs(i - 1, j)
    else:
        return get_lcs(i, j - 1)


lcs_length = longest_common_sequence_length(M, N)
lcs_sequence = get_lcs(N, M)

print(f"Length of Longest Common Subsequence: {lcs_length}")
print(f"Longest Common Subsequence: {lcs_sequence}")