from collections import Counter

a = int(input())  # кол-во резервуаров

b = input().split(' ')

max_value = int(max(b))
min_value = int(min(b))

difference_list = []

for i in b:
    difference_list.append(max_value - int(i))

#print(difference_list)

dictionasry_repeating = Counter(difference_list)

#print(dictionasry_repeating)
#print(len(dictionasry_repeating))
if len(dictionasry_repeating) > 2:
    print(-1)
else:
    smthn = max_value - min_value
    print(smthn)
    #print('?', smthn)
    #print(dictionasry_repeating[smthn] * smthn)


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