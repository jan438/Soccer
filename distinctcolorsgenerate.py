
# Source - https://stackoverflow.com/a/13781114
# Posted by Janus Troelsen, modified by community. See post 'Timeline' for change history
# Retrieved 2026-04-04, License - CC BY-SA 4.0

#!/usr/bin/env python3
from typing import Iterable, Tuple
import colorsys
import itertools
from fractions import Fraction
from pprint import pprint

def zenos_dichotomy() -> Iterable[Fraction]:
    """
    http://en.wikipedia.org/wiki/1/2_%2B_1/4_%2B_1/8_%2B_1/16_%2B_%C2%B7_%C2%B7_%C2%B7
    """
    for k in itertools.count():
        yield Fraction(1,2**k)

def fracs() -> Iterable[Fraction]:
    """
    [Fraction(0, 1), Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 8), Fraction(3, 8), Fraction(5, 8), Fraction(7, 8), Fraction(1, 16), Fraction(3, 16), ...]
    [0.0, 0.5, 0.25, 0.75, 0.125, 0.375, 0.625, 0.875, 0.0625, 0.1875, ...]
    """
    yield Fraction(0)
    for k in zenos_dichotomy():
        i = k.denominator # [1,2,4,8,16,...]
        for j in range(1,i,2):
            yield Fraction(j,i)

# can be used for the v in hsv to map linear values 0..1 to something that looks equidistant
# bias = lambda x: (math.sqrt(x/3)/Fraction(2,3)+Fraction(1,3))/Fraction(6,5)

HSVTuple = Tuple[Fraction, Fraction, Fraction]
RGBTuple = Tuple[float, float, float]

def hue_to_tones(h: Fraction) -> Iterable[HSVTuple]:
    for s in [Fraction(6,10)]: # optionally use range
        for v in [Fraction(8,10),Fraction(5,10)]: # could use range too
            yield (h, s, v) # use bias for v here if you use range

def hsv_to_rgb(x: HSVTuple) -> RGBTuple:
    return colorsys.hsv_to_rgb(*map(float, x))

flatten = itertools.chain.from_iterable

def hsvs() -> Iterable[HSVTuple]:
    return flatten(map(hue_to_tones, fracs()))

def rgbs() -> Iterable[RGBTuple]:
    return map(hsv_to_rgb, hsvs())

def rgb_to_css(x: RGBTuple) -> str:
    uint8tuple = map(lambda y: int(y*255), x)
    return "rgb({},{},{})".format(*uint8tuple)

def css_colors() -> Iterable[str]:
    return map(rgb_to_css, rgbs())
    
def rgb_to_hex(r, g, b):
    if not all(isinstance(v, int) for v in (r, g, b)):
        raise TypeError("RGB values must be integers.")
    
    # Validate range
    if not all(0 <= v <= 255 for v in (r, g, b)):
        raise ValueError("RGB values must be between 0 and 255.")
    
    # Format as HEX string
    return "#{:02X}{:02X}{:02X}".format(r, g, b)

def rgbtuple_to_hex(x: RGBTuple):
    uint8tuple = map(lambda y: int(y*255), x)
    RGBList = list(uint8tuple)
    r = RGBList[0]
    g = RGBList[1]
    b = RGBList[2]
    pprint(RGBList)
    return "hallo"
    
if __name__ == "__main__":
    # sample 48 colors in css format
    sample_colors = list(itertools.islice(css_colors(), 48))
    for i in range(48):
        print(i, sample_colors[i])
    #pprint(rgb_to_hex(36, 78, 125))
    #pprint(rgbtuple_to_hex((36, 78, 125)))

key = input("wait")
