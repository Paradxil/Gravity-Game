DISPLAY = [800, 640]
DEPTH = 32
TILESIZE = 20

#This makes it easier to find out if a string is a number.
def is_number(s):
    #return if True
    try:
        float(s)
        return True
    #otherwise return False
    except ValueError:
        return False