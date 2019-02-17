
def parseValue(v, field_type):
    v = v.strip()
    if v in ['-', '']:
        return None
    if field_type == 'int':
        return int(v)
    if field_type == 'real':
        try:
            return float(v)
        except ValueError:
            if checkInf(v):
                return float('inf')
            else:
                raise
    if field_type == 'string':
        return v

def checkInf(v):
    for vc in v:
        if vc != '*':
            return False
    return True
