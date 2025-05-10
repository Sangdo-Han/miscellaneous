def longest_increasing_subsequence_dp(arr):
    n = len(arr)
    if n == 0:
        return 0

    dp = [1] * n  # dp[i]를 i번째 원소로 끝나는 LIS의 길이로 초기화

    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp) if dp else 0

# 테스트
arr1 = [10, 22, 9, 33, 21, 50, 41, 60, 80]
print(f"LIS 길이 (arr1): {longest_increasing_subsequence_dp(arr1)}")  # 출력: 6 ([10, 22, 33, 50, 60, 80] 또는 [10, 22, 33, 41, 60, 80] 등)

arr2 = [3, 10, 2, 1, 20]
print(f"LIS 길이 (arr2): {longest_increasing_subsequence_dp(arr2)}")  # 출력: 3 ([3, 10, 20] 또는 [3, 20] 또는 [2, 20] 또는 [1, 20])

arr3 = [2, 2, 2, 2, 2]
print(f"LIS 길이 (arr3): {longest_increasing_subsequence_dp(arr3)}")  # 출력: 1 ([2])

arr4 = []
print(f"LIS 길이 (arr4): {longest_increasing_subsequence_dp(arr4)}")  # 출력: 0