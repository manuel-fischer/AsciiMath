import totex

with open("test-input.txt", "r") as f:
    out = totex.totex(f.read())
    
print(out)

with open("test-output.tex", "w") as f:
    f.write(out)
