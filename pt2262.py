import tellstick


def ternaryString(n):
    if n == 0:
        return '0'
    digits = ""
    while n:
        digits += str(int(n % 3))
        n /= 3
    return digits[::-1]

def parse(dic):
    ternary = ternaryString(dic['data'])
    house = int(ternary[:8], 3)
    unit = int(ternary[8:], 3)

    dic.update({'parameters' : {
        'house': house,
        'unit': unit,
    }})

    return dic



def tocode(dic):
    dic = parse(dic)

    raise RuntimeError("Not implemented")
    return False
