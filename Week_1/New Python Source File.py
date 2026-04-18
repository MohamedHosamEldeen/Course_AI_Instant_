a = "ahmed anas ahmed"
print(a.count("a"))
print((lambda s: [i for i in range(len(s)) if s[i] == "a"])(a))
