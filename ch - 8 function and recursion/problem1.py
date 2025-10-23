def greatest_number(a,b,c):
    if(a>b and a>c):
        print("a is greatest")
    if(c>b and c>a):
        print("c is greatest")
    if(b>a and b>c):
        print("b is greatest")
a=int(input("entre an number"))
b=int(input("entre an number"))
c=int(input("entre an number"))
print(greatest_number(a,b,c))