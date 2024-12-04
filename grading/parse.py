#!/usr/bin/env python3

with open('users.txt', 'rt') as f:
    user_lines = f.readlines()

arr = []
d = {}
for line in user_lines:
    l = [x for x in line.strip().split('\t') if len(x) > 0]
    try:
        d[l[1]] = l[2]
    except:
        print(l)

with open("score.txt", 'rt') as f:
    lines = f.readlines()

arr = []


for line in lines:
    l = [x for x in line.strip().split('\t') if len(x) > 0]
    if l[1] == 'blue9057':
        continue

    l.append(d[l[1]])
    arr.append(l)

def get_gp(score):
    max_score = 1141
    return ((int(score) / max_score) * 80 + 20)

def get_letter_grade(pts):
    _A = 90;
    _A_ = 85;
    _Bp = 80;
    _B = 75;
    _B_ = 70;
    _Cp = 65;
    _C = 60;
    _C_ = 55;
    _Dp = 50;
    _D = 45;
    _D_ = 40;

    real_pts = pts

    if real_pts >= _A:
        return 'A'
    if real_pts >= _A_:
        return 'A-'
    if real_pts >= _Bp:
        return 'B+'
    if real_pts >= _B:
        return 'B'
    if real_pts >= _B_:
        return 'B-'
    if real_pts >= _Cp:
        return 'C+'
    if real_pts >= _C:
        return 'C'
    if real_pts >= _C_:
        return 'C-'
    if real_pts >= _Dp:
        return 'D+'
    if real_pts >= _D:
        return 'D'
    if real_pts >= _D_:
        return 'D-'
    return 'F'



for i in arr:
    gp = get_gp(i[2])
    lg = get_letter_grade(gp)

    a = [gp, lg]
    i += a
    print(i)



