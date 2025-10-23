a=input("Entre Your Name ")
b=input("Entre The Date ")

Joining_Letter = """Dear <chaman>
you are Selected for corporate Majduri in TATA POWER and you assigned as an Assistant Trainee Officer 
Date<bla bla>
Appki Gand Mein Chawanprash
"""
print(Joining_Letter.replace("<chaman>",a).replace("<bla bla>",b))