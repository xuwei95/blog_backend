from django.test import TestCase

# Create your tests here.
# import itertools
# nums = 'hello'
# a = list(itertools.permutations(nums))
# print(a)
# a = input()
# b = input()
# li = b.split(' ')
# n = 0
# li = sorted([int(i) for i in li])
# for i in li:
#     if n >= int(a):
#         print(n)
#         break
#     else:
#         n += int(i)

def move(s, i):
    s = s[i:] + s[:i]
    return s

def get_code(code, m, d):
    s1 = 'ABCDEFGHI'
    s2 = 'JKLMNOPQR'
    s3 = 'STUVWXYZ '
    m1 = (m-1) % 3
    m2 = (d-1) % 7
    s1 = move(s1, m2)
    s2 = move(s2, m2)
    s3 = move(s3, m2)
    if m1 == 1:
        li = [s2, s3, s1]
    elif m1 == 2:
        li = [s3, s2, s1]
    else:
        li = [s1, s2, s3]
    index = ''
    for i in range(3):
        if code in li[i]:
            index = (i+1) + li[i].index(code.upper())
            break
    return str(index)
a = input()
b = input()
li = a.split(' ')
m = int(li[0])
d = int(li[1])
s = ''
for i in b:
    print(i)
    print(get_code(i, m, d))
    s += get_code(i, m, d) + ' '
print(s)





