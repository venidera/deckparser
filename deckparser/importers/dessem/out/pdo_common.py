
def parseValue(v, cf):
    v = v.strip()
    if v in ['-', '']:
        return None
    if cf == 'i':
        return int(v)
    if cf == 'f':
        try:
            return float(v)
        except ValueError:
            if checkInf(v):
                return float('inf')
            else:
                raise
    if cf == 's':
        return v

def checkInf(v):
    for vc in v:
        if vc != '*':
            return False
    return True
