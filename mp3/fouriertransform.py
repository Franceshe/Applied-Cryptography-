import random
from secretsharing import Fp, Poly


def isPowerOfTwo(n):
    # bit-arithmetic trick
    return n & (n-1) == 0


def nearestPowerOfTwo(n):
    if isPowerOfTwo(n): return n
    return 2 ** n.bit_length()


###############################################
# Problem 4.1: Roots of unity in a finite field [5pts]]
###############################################


def isNthRootOfUnity(omega, n):
    assert isPowerOfTwo(n)
    # Check that omega is an nth root of unity, omega^n == 1
    return pow(omega, n) == 1


def isPrimitiveNthRootOfUnity(omega, n):
    assert isPowerOfTwo(n)
    if not isNthRootOfUnity(omega, n): return False
    # Check that n is the *smallest* power so that omega^n == 1
    return pow(omega, n // 2) != 1 or omega == n == 1


def get_omega(Fp, n, seed=None):
    """
    Given a field, this method returns an n^th root of unity.
    If the seed is not None then this method will return the
    same n'th root of unity for every run with the same seed

    This only makes sense if n is a power of 2!
    """
    assert isPowerOfTwo(n), "n must be power of 2"
    rnd = random.Random(seed)

    # TODO: Your code goes here
    y = Fp(0)

    assert isNthRootOfUnity(y, n), "omega must be 2n'th root of unity"
    assert isPrimitiveNthRootOfUnity(y, n), "omega must be primitive 2n'th root of unity"
    return y


###################################################
# Problem 4.2: Fourier transform over finite fields [10pts]
###################################################

def evaluate_fft(f, omega, n):
    """
    Evaluates the polynomial on n powers of omega,
    such that f(omega^i) for i in 0 through n-1
    """
    assert isPowerOfTwo(n), "n must be power of two"
    assert type(omega) is Fp
    assert isPrimitiveNthRootOfUnity(omega, n), "omega must be primitive 2n'th root of unity"

    # Pad coefficients to degree-n with zeros
    coeffs = f.coefficients
    coeffs = coeffs + [Fp(0)] * (n - len(coeffs))

    # Run fft
    result = []
    # TODO: Your code goes here

    assert type(result) is list
    return result


##################################################
# Problem 4.3: Interpolate a polynomial using IFFT [5pts]
##################################################


def interpolate_fft(ys, omega):
    """
    Returns a polynoial f of given degree,
    such that f(omega^i) == ys[i]
    """
    n = len(ys)
    assert isPowerOfTwo(n), "n must be power of two"
    assert type(omega) is Fp
    assert isPrimitiveNthRootOfUnity(omega, n), "omega must be primitive 2n'th root of unity"

    coeffs = []

    # TODO: Your code goes here
    # Hint: interpolate should use *inverse* fft

    poly = Poly(coeffs)
    return poly


if __name__ == "__main__":

    # Problem 4.1: Finding roots of unity
    # Try to find the 8th root of unity
    n = 2**3
    omega = get_omega(Fp, n)        

    # Example polynomial with degree t=6
    poly = Poly([1, 5, 3, 15, 0, 3])
    
    # Problem 4.2: Evaluate the polynomial using FFT
    ys = evaluate_fft(poly, omega, n)
    assert ys == [poly(omega**i) for i in range(n)], "Problem 4.2 check"

    # Problem 4.3: Interpolate polynomial using Inverse FFT
    poly2 = interpolate_fft(ys, omega)
    print(poly2)
    print(poly)
    assert poly == poly2, "Problem 4.3 check"
