n = int(input())  # 1 <= n <= 100 000 | Amount of tanks
Volumes = list(map(int, input().split()))  # Volume of each tank
answer = 0
maximal = Volumes[0]
for i in range(len(Volumes)):
    maximal = max(Volumes[i], maximal)
    if Volumes[i] < maximal:
        answer = -1
        break
print(max(Volumes) - min(Volumes) if answer == 0 else answer)
#
# n = int(input())  # 1 <= n <= 100 000 | Amount of tanks
# Volumes = list(map(int, input().split()))  # Volume of each tank
# answer = 0
# maximal = Volumes[0]
# print("maximal: ", maximal)
# print("________________________________________________________________")
# for i in range(len(Volumes)):
#     maximal = max(Volumes[i], maximal)
#     print("maximal: ", maximal)
#     if Volumes[i] < maximal:
#         print("maximal: ", Volumes[i])
#         answer = -1
#         break
# print(max(Volumes) - min(Volumes) if answer == 0 else answer)
