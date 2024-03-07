import leb128


def deserialize(line: bytes) -> dict:
    ans: dict = {}
    while len(line) > 1:
        len_k = line[1]
        len_v = line[3]
        k = str(line[5 : 5 + len_k]).replace("'", "")[1:]
        v = line[5 + len_k : 5 + len_k + len_v]
        if line[4] == 2:
            v = deserialize(v)
        elif line[4] == 1:
            v = leb128.i.decode(v)
        else:
            v = str(v).replace("'", "")[1:]
        ans[k] = v
        line = line[5 + len_k + len_v :]
    return ans
