import tellstick




def parse(dic):
    data = dic['data']
    dic.update({'checksum' : (data & 0xff)})

    humidity =  (data & 0xFF00) >> 8
    if humidity <= 100:
        dic.update({'model' : 'temperaturehumidity'})
        dic.update({'humidity' : humidity})
    elif humidity == 0xFF:
        dic.update({'model' : 'temperature'})
    else:
        raise ValueError("Unvalid humidity")
        return False

    temp = (data & 0x7FF0000) >> 16
    negative =  (data & 0x8000000) >> 27
    if negative:
        temp = -temp
    dic.update({'temperature' : float(temp)/10})

    dic.update({'id' : (data & 0xFF0000000) >> 28})


    return dic
