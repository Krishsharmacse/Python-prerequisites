n=int(input("entre the nubmer you want to check it is prime or not\n"))
for i in range(2,n):
    if n % i==0:
        print("no is not prime\n")
    else:
        print("it is prime\n")