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

### splits lines into blocks horizontally
### lines should have all the same length and should contain elements
##def col_groups(lines):
##    return map(transpose_str, group(nonspace, transpose_str(lines)))



# adds spaces to the end of each line, so that all lines have the same length
def str_rect_space(lines):
    cols = max(map(len, lines))
    return map(("{:%i}"%cols).format, lines)

### removes lines only consisting of spaces
##def rm_space(lines):
##    return filter(nonspace, lines)


### returns iterable, so that e is yielded first and then the elements of i
##def push_front(e, i):  yield e;  yield from i
##

### splits itr into two
### returns tuple of lhs and rhs
### lhs where for all e: pred(e) == true, returned as list
### rhs where for first e: pred(e) == False, returned as iterable
##def peek_if(pred, itr):
##    lhs = []
##    i = iter(itr)
##    while True:
##        try:  e = next(i)
##        except StopIteration:  return (lhs, [])
##        if pred(e):  lhs.append(e)
##        else:  return (lhs, push_front(e, i))
##
##def separate_cols_at(row, cols):
##    top = []
##    btm = []
##    for col in cols:
##        top.append(col[:row])
##        btm.append(col[row+1:])
##
##    return (top, btm)

# get position of first character of s, which is not in chars
# if chars is None, the position of the first nonspace character is returned
# returns len(s), if nothing different is found
def str_find_first_not(s, chars=None):
    return len(s) - len(s.lstrip(chars)) # lstrip: chars parameter defaults to None

# strips outer colums only with spaces
# removes empty lines
def str_rect_strip(lines):
    lines = list(lines) # multiple use
    if not lines: return []
    lhs = min(len(l) - len(l.lstrip()) for l in lines)
    rhs =          max(len(l.rstrip()) for l in lines)
    return (l[lhs:rhs] for l in lines if nonspace(l))

              
### cols: colums, should have all the same length
### returns top, bottom and right as cols
##def separate_at_char(row, char, lines):
##    lines = list(lines)
##
##    epos = str_find_first_not(lines[row], char)
##
##    lhs = (l[:epos] for l in lines)
##    rhs = (l[epos:] for l in lines)
##
##    top = lhs[:row]
##    btm = lhs[row+1:]
##
##    return top, btm, rhs
        


### splits vertically if there is a char, which is in splitchars
### yields tuple of two elements
### when something is split (and the top and bottom are not just space),
### the second element of the tuple is a tuple of the top and bottom
### 
##def separate_at_row(row, lines, splitchars):
##    lines = list(lines)
##
##    epos = str_find_first_not(lines[row], char)
##
##    lhs = (l[:epos] for l in lines)
##    rhs = (l[epos:] for l in lines)
##
##    top = lhs[:row]
##    btm = lhs[row+1:]
##
##    return top, btm, rhs



# yields tuples of 2 elements
# first,  the element in grouping or None
# second, the slice, in 
def slices_group_by_chars(s, grouping):
    width = len(s)
    epos = 0
    non_beg = 0
    while epos != width:
        for i, g in enumerate(grouping):
            npos = str_find_first_not(s[epos:], g)
            if npos != 0:
                if non_beg != epos: yield (None, slice(non_beg, epos))
                yield ((i, g), slice(epos, epos+npos))
                epos += npos
                non_beg = epos
                break
        else:
            epos += 1

    if non_beg != epos: yield (None, slice(non_beg, epos))


def totex_block(lines):
    ret = ""
    
    lines = list(lines)
    if len(lines) == 1: return lines[0]

    columns = list(transpose_str(lines))
    width = len(columns)

    if width == 0: return ""

    occupied = len(columns[0].strip())
    if occupied != 1: raise Exception("Ambiguous, multiple things in first column")
    # TODO check here for large brackets, etc...
    
    main_row = str_find_first_not(columns[0], None)


    # parse single line text until space
    
    for group, slc in slices_group_by_chars(lines[main_row], ["-", None]):
        g_lines = [l[slc] for l in lines]
        top = list(str_rect_strip(g_lines[:main_row]))
        btm = list(str_rect_strip(g_lines[main_row+1:]))
        if not top and not btm:
            ret += g_lines[main_row]
        elif group != None:
            i, g = group
            topx = totex_block(top)
            btmx = totex_block(btm)
            if g == "-":
                ret += r"\frac{%s}{%s}" % (topx, btmx)
            elif g == None: # spaces
                # super/subscript
                if topx:  ret += "^{%s}" % topx
                if btmx:  ret += "_{%s}" % btmx
        else:
            raise Exception("There shouldn't be text above or below other text")
            
    return ret

        

##    for x, col in enumerate(columns):
##        if nonspace(col):
##            if col[main_row] == "-":
##                
##            elif nonspace(col[main_row]):
##                assert(len(col.strip()) == 1)
##            else:
##                # super/subscript
##        else:
##            # finish...
##            ret += " "
##
##    return ret.strip()


def totex_line(lines):
    return totex_block(str_rect_strip(str_rect_space(lines)))


### lines should have all the same length
### all columns should contain a space anywhere
### all rows    should contain a space anywhere
##def totex_block(lines):
##    lines = list(lines)
##    if len(lines) == 1: return lines[0]
##
##    columns = list(transpose_str(lines))
##    width = len(columns)
##
##    char = columns[0].strip()
##    if char != "-": raise Exception("Expected '-' in multiline")
##    charpos = columns[0].find(char)
##    if lines[charpos] != "-"*width: raise Exception("Expected complete '-'")
##    if columns[0] != columns[-1]: raise Exception("Expected single '-' before end")
##    
##    num = totex_line(lines[:charpos])
##    den = totex_line(lines[charpos+1:])
##
##    return r"\frac{%s}{%s}" % (num, den)
##    
##        
##
##def totex_line(lines):
##    # split the blocks into parts, separated by whole colums consisting
##    # of spaces
##    return " ".join(
##        totex_block(rm_space(block))
##        for block in col_groups(str_rect_space(lines))
##    )
            

STR = "\\begin{flalign*}\n%s&&\n\\end{flalign*}"

def totex(txt):
    return "\n\n".join(
        STR % totex_line(lg)
        for lg in split_line_groups(txt)
    ) + "\n" # Newline at end of file
