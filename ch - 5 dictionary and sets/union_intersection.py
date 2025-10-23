s={1,2,5,8,4,5,2,3,4,7,8,95,4,5,45,1,3,454}
s1={2,5,8,9,45,65,32,32,7,45,21}
print(s.union(s1))
print(s1.intersection(s))
print({1,2}.issubset(s))
print(s-s1)
print({2,5}.issuperset(s1))
