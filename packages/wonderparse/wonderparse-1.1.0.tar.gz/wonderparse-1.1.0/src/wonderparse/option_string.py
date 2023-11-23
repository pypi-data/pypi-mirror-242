
def by_dest_and_prefix_char(dest, prefix_char):
    dest = str(dest)
    if len(dest) < 1:
        raise ValueError
    if len(dest) == 1:
        prefix = "_"
    else:
        prefix = "__"
    ans = prefix + dest
    ans = ans.replace('_', prefix_char)
    return ans