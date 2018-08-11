import tellstick




def parse(dic):
    if dic['model'] == "selflearning":
        dic.update({'method':  0x01      & (dic['data'] >> 4)})
        dic.update({'parameters': {
            'unit':    0x0f      & dic['data'],
            'group':   0x01      & (dic['data'] >> 5),
            'house':   0x3FFFFFF & (dic['data'] >> 6)
            }})

        return dic

    else:
        raise ValueError("Unknown model")


def selflearningcode(house, unit, method, dimlevel=255):
    SHORT = chr(24)
    LONG  = chr(127)

    ONE = SHORT + LONG + SHORT + SHORT
    ZERO = SHORT + SHORT + SHORT + LONG

    code = SHORT + chr(255) # sync bit
    for i in range(25, -1, -1):
        if house & (1 << i):
            code += ONE
        else:
            code += ZERO
    code += ZERO # Group bit
    if method == tellstick.METHOD_ON:
        code += ONE
    elif method == tellstick.METHOD_OFF:
        code += ZERO
    elif method == tellstick.METHOD_DIM:
        code += 4*SHORT
    elif method == tellstick.METHOD_LEARN:
        code += ONE
    else:
        raise ValueError("Unsupported method")

    for i in range(3, -1, -1):
        if unit & (1 << i):
            code += ONE
        else:
            code += ZERO

    if method == tellstick.METHOD_DIM:
        level = dimlevel/16
        for i in range(3, -1, -1):
            if level & (1 << i):
                code += ONE
            else:
                code += ZERO

    code += SHORT
    return code


def tocode(dic):
    dic = parse(dic)
    if dic['model'] == "selflearning":
        return selflearningcode(dic['house'], dic['unit'], dic['method'])

    raise Exception("Unknown model")
    return False
