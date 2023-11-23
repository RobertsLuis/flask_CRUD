def psi(value, unit):
    units = {
        "bar": value*0.0689,
        "kpa": value * 6.894
    }
    try:
        return units[unit]
    except:
        return value


def bar(value, unit):
    units = {
        "psi": value * 14.5,
        "kpa": value * 100
    }
    try:
        return units[unit]
    except:
        return value


def kpa(value, unit):
    units = {
        "bar": value * 0.01,
        "psi": value * 0.145
    }
    try:
        return units[unit]
    except:
        return value