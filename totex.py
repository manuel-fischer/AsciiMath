# parameter like filter, but instead of None, use bool
# pred: funtion or `bool`
def group(pred, itr):
    group = []
    for e in itr:
        if pred(e):  group.append(e)
        elif group:  yield group;    group = []
    if group:  yield group

# returns True, when s contains characters other than whitespace
def nonspace(s : str):
    return bool(s.strip())

# transposes an array of strings
# str_lst: list of strings, they should all have the same length
def transpose_str(str_lst):
    return map("".join, zip(*str_lst))

# split a string into lines and group them into arrays of lines
def split_line_groups(txt):
    return group(nonspace, txt.split("\n"))

# splits lines into blocks horizontally
# lines should have all the same length and should contain elements
def col_groups(lines):
    return map(transpose_str, group(nonspace, transpose_str(lines)))



# adds spaces to the end of each line, so that all lines have the same length
def str_rect_space(lines):
    cols = max(map(len, lines))
    return map(("{:%i}"%cols).format, lines)

# removes lines only consisting of spaces
def rm_space(lines):
    return filter(nonspace, lines)



# lines should have all the same length
# all columns should contain a space anywhere
# all rows    should contain a space anywhere
def totex_block(lines):
    lines = list(lines)
    if len(lines) == 1: return lines[0]

    columns = list(transpose_str(lines))
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
    # split the blocks into parts, separated by whole colums consisting
    # of spaces
    return " ".join(
        totex_block(rm_space(block))
        for block in col_groups(str_rect_space(lines))
    )
            

def totex(txt):
    return "\n\n".join(
        "$%s$\\\\" % totex_line(lg)
        for lg in split_line_groups(txt)
    ) + "\n" # Newline at end of file
