import re
from decimal import * 
def pi():
    """Compute Pi to the current precision.

    >>> print pi()
    3.141592653589793238462643383

    """
    getcontext().prec += 2  # extra digits for intermediate steps
    three = Decimal(3)      # substitute "three=3.0" for regular floats
    lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
    while s != lasts:
        lasts = s
        n, na = n+na, na+8
        d, da = d+da, da+32
        t = (t * n) / d
        s += t
    getcontext().prec -= 2
    return +s               # unary plus applies the new precision

def exp(x):
    """Return e raised to the power of x.  Result type matches input type.

    >>> print exp(Decimal(1))
    2.718281828459045235360287471
    >>> print exp(Decimal(2))
    7.389056098930650227230427461
    >>> print exp(2.0)
    7.38905609893
    >>> print exp(2+0j)
    (7.38905609893+0j)

    """
    getcontext().prec += 2
    i, lasts, s, fact, num = 0, 0, 1, 1, 1
    while s != lasts:
        lasts = s
        i += 1
        fact *= i
        num *= x
        s += num / fact
    getcontext().prec -= 2
    return +s

def ln(x):
    """Return a=ln(x), such that e^a=x.

    >>> print ln(Decimal(2))
    0.69314718056

    """
    getcontext().prec += 2
    e = exp(Decimal(1))
    i_part = Decimal(0)
    if x<0:
        raise ValueError, "ln of negative number"
    # we want x in the range 1<x<e
    while x<1: i_part -= 1; x *= e
    while x>e: i_part += 1; x /= e
    
    n = Decimal("0.5")
    x = x**2
    f_part = Decimal(0)
    last_f_part = Decimal(1)
    while last_f_part != f_part:
        if x >= e:
            last_f_part = f_part
            f_part += n 
            x /= e
        n /= 2
        x = x**2
    log = i_part+f_part 
    getcontext().prec -= 2
    return +log

 

def cos(x):
    """Return the cosine of x as measured in radians.

    >>> print cos(Decimal('0.5'))
    0.8775825618903727161162815826
    >>> print cos(0.5)
    0.87758256189
    >>> print cos(0.5+0j)
    (0.87758256189+0j)

    """
    getcontext().prec += 2
    i, lasts, s, fact, num, sign = 0, 0, 1, 1, 1, 1
    while s != lasts:
        lasts = s
        i += 2
        fact *= i * (i-1)
        num *= x * x
        sign *= -1
        s += num / fact * sign
    getcontext().prec -= 2
    return +s

def sin(x):
    """Return the sine of x as measured in radians.

    >>> print sin(Decimal('0.5'))
    0.4794255386042030002732879352
    >>> print sin(0.5)
    0.479425538604
    >>> print sin(0.5+0j)
    (0.479425538604+0j)

    """
    getcontext().prec += 2
    i, lasts, s, fact, num, sign = 1, 0, x, 1, x, 1
    while s != lasts:
        lasts = s
        i += 2
        fact *= i * (i-1)
        num *= x * x
        sign *= -1
        s += num / fact * sign
    getcontext().prec -= 2
    return +s

def pow(x,y):
    """Return x^y with full generality.

    Won't be needed in Python 2.6+
    """
    return exp(y*ln(x))

def looks_like_a_number(s):
    """Match a decimal constructor string.

    Using the definition in *BNF form in the Decimal class documentation
    sign           ::=  '+' | '-'
    digit          ::=  '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
    indicator      ::=  'e' | 'E'
    digits         ::=  digit [digit]...
    decimal-part   ::=  digits '.' [digits] | ['.'] digits
    exponent-part  ::=  indicator [sign] digits
    infinity       ::=  'Infinity' | 'Inf'
    nan            ::=  'NaN' [digits] | 'sNaN' [digits]
    numeric-value  ::=  decimal-part [exponent-part] | infinity
    numeric-string ::=  [sign] numeric-value | [sign] nan

    but ignoring the bits about 'Infinity' or 'NaN', we constrct a suitable
    regular express and return true if our single string argument matches.
    """    
    return re.match(r'\A[-+]?(\d+\.\d*|\.?\d+)([eE][-+]?\d+)?\Z',s)


if __name__ == "__main__":
    a = Decimal(2)
    b = Decimal(3)
    c = Decimal("0.5")
    print ln(a)
    print exp(ln(a))
    print pow(a*10,c)
    print a.sqrt()
    print (pow(a*10,c)/a.sqrt())**2

