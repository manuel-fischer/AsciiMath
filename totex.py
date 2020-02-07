def line_groups(txt):
    lines = []
    for l in txt.split("\n"):
        l = l.rstrip()
        if not l:
            if lines:
                yield lines
                lines = []
        else:
            lines.append(l)
            
    if lines:
        yield lines

# adds spaces to the end of each line, so that all lines have the same length
def str_rect_space(lines):
    cols = max(map(len, lines))
    return list(map(("{:%i}"%cols).format, lines))

### lines should have all the same length
##def str_empty_cols(lines):
##    zipped = zip(*str_rect_space(lines))
##    for i, col in enumerate(zipped):
##        if not "".join(col).strip(): yield i
    
# splits lines into blocks horizontally
# lines should have all the same length and should contain elements
def str_split_rects(lines):
    #if len(lines) == 1: return [[l] for l in lines[0].split()]
    cols = [""]*len(lines)
    # scan from left to right over the whole column at once
    for col in zip(*lines):
        if not "".join(col).strip():
            # Column consists of spaces
            if cols[0]:
                yield cols
                cols = [""]*len(lines)
        else:
            cols = [a + b for a, b in zip(cols, col)]
            
    if cols[0]:
        yield cols

def str_rm_empty_lines(lines):
    return list(filter(lambda l: bool(l.strip()), lines))

# lines should have all the same length
# all columns should contain a space anywhere
# all rows    should contain a space anywhere
def totex_block(lines):
    if len(lines) == 1: return lines[0]

    columns = list(map("".join, zip(*lines)))
    width = len(columns)

    char = columns[0].strip()
    if char != "-": raise Exception("Expected '-' in multiline")
    charpos = columns[0].find(char)
    if lines[charpos] != "-"*width: raise Exception("Expected complete '-'")
    if columns[0] != columns[-1]: raise Exception("Expected single '-' before end")
    
    num = totex_line(lines[:charpos])
    den = totex_line(lines[charpos+1:])

    return r"\frac{%s}{%s}" % (num, den)
    
        

def totex_line(lines):
    ret = ""

    # split the blocks into parts, separated by whole colums consisting
    # of spaces
    for block in str_split_rects(str_rect_space(lines)):
        ret += totex_block(str_rm_empty_lines(block)) + " "

    return ret[:-1]
            

def totex(txt):
    #return r"$f(x) = \frac{5x - 3}{7x}$"
    ret = ""
    
    for lg in line_groups(txt):
        ret += "$%s$\\\\\n\n" % totex_line(lg)
        
    return ret
        
