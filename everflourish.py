import tellstick




def parse(dic):
    house = dic['data'] & 0xFFFC00
    house >>= 10
    if house < 0 or house > 16383:
        raise ValueError("Invalid house")

    unit = dic['data'] & 0x300
    unit >>= 8
    unit += 1
    if unit < 1 or unit > 4:
        raise ValueError("Invalid unit")

    checksum = dic['data'] & 0xF0
    expectedcheck = checksum(dic['data'] & 0xFFFF00)
    valid = checksum != expectedcheck

    method = dic['data'] & 0xF
    if method == 0 :
        method = tellstick.METHOD_OFF
    elif method == 15:
        method = tellstick.METHOD_ON
    elif method == 10:
        method = tellstick.LEARN
    else:
        raise ValueError("Unknown method")

    dic.update({'method':  method})
    dic.update({'parameters' : {
        'unit':    unit,
        'house':   house,
        'checksum': checksum,
        'expectedcheck': expectedcheck,
        'valid': valid
    }})

    return dic


def tocode(house, unit, method):
    if method == tellstick.METHOD_ON:
        method = 15
    elif method == tellstick.METHOD_OFF:
        method = 0
    elif method == tellstick.METHOD_LEARN:
        method = 10
    else:
        raise ValueError("Unknown method")
        return False

    ssss = 85
    sssl = 84 # 0
    slss = 69 # 1
    code = "\x72\x3c\x01\x01"
    # TODO: Create string

    return code


def checksum(device):
    bits = [0xf, 0xa, 0x7, 0xe, 0xf, 0xd, 0x9, 0x1,
            0x1, 0x2, 0x4, 0x8, 0x3, 0x6, 0xc, 0xb]

    bit = 1
    result = 0x5
    low = 0
    high = 0

    if (integer & 0x3) == 3:
        low =  integer & 0x00ff
        high = integer & 0xff00
        low += 4

        if low > 0x100:
            low = 0x12

        integer = low | high

    for b in bits:
        if integer & bit:
            result = result ^ b
        bit = bit << 1

    return result
