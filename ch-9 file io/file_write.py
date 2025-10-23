s1 = "gadha kahika"
f= open("file.txt","w")
f.write(s1)
f.close
f=open("file.txt","r")
print(f.read())
f.close