r1 = 1
r2 = 4.7
r3 = 2.2
r4 = 4.6
r5 = 3.3
vs1 = 5
vs2 = 10

def cal(a,b):
    return a*b/(a+b)

def current_i(v,r):
    return v/r

c = cal(r4,r5)
d = r3 + c


it_vs1 = current_i( vs1, cal(r2,d) )
print("it_vs1 : ",it_vs1)

e = cal(r1,r2)
f = r3 + e
it_vs2 = current_i( vs2, cal(r4,f) )
print("it_vs2 : ", it_vs2)

print("IT = ", it_vs1-it_vs2)
