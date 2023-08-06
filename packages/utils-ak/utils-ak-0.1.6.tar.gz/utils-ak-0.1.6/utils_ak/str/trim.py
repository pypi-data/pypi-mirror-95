
def trim(s, beg=None, end=None):
    if beg is not None and s.startswith(beg):
        s = s[len(beg):]
    if end is not None and s.endswith(end):
        s = s[:-len(end)]
    return s
