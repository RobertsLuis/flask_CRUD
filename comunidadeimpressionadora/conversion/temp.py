def celcius(value, unit):
    units = {
        "fahrenheit": value*1.8+32,
        "kelvin": value + 273.15
    }
    try:
        return units[unit]
    except:
        return value

def fahrenheit(value, unit):
    units = {
        "celcius": (value-32)/1.8,
        "kelvin": (value-32)/1.8 + 273.15
    }
    try:
        return units[unit]
    except:
        return value


def kelvin(value, unit):
    units = {
        "celcius": value - 273.15,
        "fahrenheit": (value - 273.15)*1.8 + 32
    }
    try:
        return units[unit]
    except:
        return value
