a = float(input("ENTRE MATH MARKS OF FIRST CANDIDATE\n"))
aSCIENCE = float(input("ENTRE Science MARKS OF FIRST CANDIDATE\n"))
aSST = float(input("ENTRE SST MARKS OF FIRST CANDIDATE\n"))
b = float(input("ENTRE MATH MARKS OF SECOND CANDIDATE\n"))
bSCIENCE = float(input("ENTRE Science MARKS OF SECOND CANDIDATE\n"))
bSST = float(input("ENTRE SST MARKS OF SECOND CANDIDATE\n"))
c = float(input("ENTRE MATH MARKS OF THIRD CANDIDATE\n"))
cSCIENCE = float(input("ENTRE Science MARKS OF THIRD CANDIDATE\n"))
cSST = float(input("ENTRE SST MARKS OF THIRD CANDIDATE\n"))
d = float(input("ENTRE MATH MARKS OF FOURTH CANDIDATE\n"))
dSCIENCE = float(input("ENTRE Science MARKS OF FOURTH CANDIDATE\n"))
dSST = float(input("ENTRE SST MARKS OF FOURTH CANDIDATE\n"))
if(a<33 and aSST<33 and aSCIENCE<33):
    print("YOU ARE FAIL A IS FAIL")
else:
    print("YOU ARE A IS PASS")
if(b<33 and bSST<33 and cSCIENCE<33):
    print("YOU ARE B IS FAIL")
else:
    (print("YOU ARE B IS PASS"))
if(c<33 and cSST<33 and cSCIENCE<33):
    print("YOU ARE C IS FAIL")
else:
    (print("YOU ARE C IS PASS"))
if(d<33 and dSST<33 and dSCIENCE<33):
    print("YOU ARE D IS FAIL")
else:
    (print("YOU ARE D IS PASS"))

if((a+aSCIENCE+aSST)/300*100 > 40):
        print("YOU Are Pass", (a+aSCIENCE+aSST)/300*100 )
else:
        print("you are fail", (a+aSCIENCE+aSST)/300*100)
if((b+bSCIENCE+bSST)/300*100 > 40):
        print("YOU Are Pass", (b+bSCIENCE+bSST)/300*100)
else:
        print("you are fail", (b+bSCIENCE+bSST)/300*100)
if((c+cSCIENCE+cSST)/300*100 > 40):
        print("YOU Are Pass", (c+cSCIENCE+cSST)/300*100)
else:
        print("you are fail", (c+cSCIENCE+cSST)/300*100)
if((d+dSCIENCE+dSST)/300*100 > 40):
        print("YOU Are Pass", (d+dSCIENCE+dSST)/300*100)
else:
        print("you are fail", (d+dSCIENCE+dSST)/300*100)

