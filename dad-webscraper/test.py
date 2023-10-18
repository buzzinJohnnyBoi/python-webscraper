s = "Ford Fiesta SE"
index = s.find("20")

if index != -1 and index + 2 < len(s):
    if int(s[index + 2:index + 4]) > 10:
        print(True)
    else:
        print(False)
else:
    if "19" in s:
        print(False)
    else:
        print(True)
        