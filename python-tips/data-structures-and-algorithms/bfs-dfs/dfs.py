from collections import deque

M, N = map(int, input().split())
box = []
ripe_tomatoes = deque()

for i in range(N):
    row = list(map(int, input().split()))
    box.append(row)
    for j in range(M):
        if row[j] == 1:
            ripe_tomatoes.append((i, j, 0))

dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]

max_days = 0
while ripe_tomatoes:
    x, y, days = ripe_tomatoes.popleft()
    max_days = max(max_days, days)

    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]

        if 0 <= nx < N and 0 <= ny < M and box[nx][ny] == 0:
            box[nx][ny] = 1
            ripe_tomatoes.append((nx, ny, days + 1))

all_ripe = True
for row in box:
    if 0 in row:
        all_ripe = False
        break

if all_ripe:
    print(max_days)
else:
    print(-1)