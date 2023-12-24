with open("/usr/share/dict/words", "r") as f:
    words = sorted({s.strip().lower() for s in f})

def deletions(s):
    yield from (s[:i]+s[i+1:] for i in range(0,len(s)))

def is_subsequence(a,b):
    if not a:
        return True
    elif len(a) == len(b):
        return a == b
    elif len(a) > len(b):
        return False
    start = 0
    for c in a:
        try:
            start = b.index(c, start)
        except ValueError:
            return False
    return True

redundant_cache = {}
def is_redundant(w):
    if w in redundant_cache:
        return redundant_cache[w][0]
    cs = [w2 for w2 in words if is_subsequence(w, w2)]
    c = len(cs)
    assert c >= 1
    res = (c >= 2)
    redundant_cache[w] = (res, cs)
    return res

def abbrev_candidates(w):
    opts = [w]
    if is_redundant(w):
        return opts
    while opts:
        print(opts)
        last = opts
        opts = sorted({o for opt in opts for o in deletions(opt) if not is_redundant(o)})
    return last

import sys
w = sys.argv[1]
if len(sys.argv) > 2:
    to_remove = sys.argv[2].split(",")
    words = set(words)
    for word in to_remove:
        assert word in words, "{} is not present anyway".format(word)
        words.remove(word)
assert w in words, "{} is not in the dictionary".format(w)
if is_redundant(w): print("not unique:", redundant_cache[w][1])
else: print(abbrev_candidates(w))
