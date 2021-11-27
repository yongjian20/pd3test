
def PositiveDollar(text):
    try:
        text = eval(text)
        if type(text) == float or type(text) == int:
            if text >= 0:
                return text
    except:
        print("Numeric input failed")
        return None
    return None

def PositiveNumber(text, maxLength=0):
    try:
        text = eval(text)
        if type(text) == int:
            if text >= 0:
                if maxLength == 0:
                    return text
                elif len(str(text)) <= maxLength:
                    return text
    except:
        print("Numbers input failed")
        return None
    return None

def MobileNumber(text):
    try:
        text = eval(text)
        if type(text) == int:
            if text >= 0:
                if len(str(text)) == 8:
                    return text
    except:
        print("Mobile Number input failed")
        return None
    return None