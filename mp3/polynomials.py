"""
## Programming with Polynomials, Lagrange Interpolation
"""
import sys
from functools import reduce
sys.path += ['elliptic-curves-finite-fields']
from finitefield.finitefield import FiniteField
from finitefield.polynomial import polynomialsOver
from finitefield.euclidean import extendedEuclideanAlgorithm
import random
import operator

"""
## Sample code: using the j2kun library for polynomials over a 
   finite field
"""
if __name__ == '__main__':
    Fp = FiniteField(p=53,m=1) # Finite field is specified with a prime p
    Poly = polynomialsOver(Fp)

    p1 = Poly([1,2,3,4,5])
    print('p1:', p1)
    # 1 + 2 t + 3 t^2 + 4 t^3 + 5 t^5

    # The library comes with a variety of tools for you to use
    # First, you can perform linear operations on the polynomials.
    p2 = Poly([3,2,4,8])
    p3 = 2 * p1 + 3 * p2
    print('p2:', p2)
    print('p3:', p3)

    # You can even multiply two polynomials together, although this
    # typically results in larger degree
    p4 = p3 * p3
    assert p4.degree() == p3.degree() * 2
    print('p4:', p4)

    
######################################
# Problem 1.1: Evaluating a polynomial [5 pts]
######################################

def eval_poly(f, x):
    # The polynomial is degree-k where k+1 == len(f.coeffs)
    # Coeffs are in order so that f(x) = sum( a[i] * x^i for i in range(k+1) )
    assert type(x) in (f.field, int)
    y = f.field(0)
    # TODO: Your code goes here
    # Hint: try to implement an efficient solution. You should use O(k) total
    # multiplications, and no pow() or **
    for (degree,coeff) in enumerate(f):
        pass
    return y


####################################
# Problem 1.2: Lagrange coefficients [5pts]
####################################

"""
Goal:
  Compute the Lagrange coefficients as polynomial p[i](x)

   p[i](x) = product[over j != i] of (x - x[j])/(x[i] - x[j])
"""

def lagrange_polynomial(Poly, xs, xi):
    assert xi in xs

    x = Poly([0,1]) # This is the polynomial f(x) = x
    ONE = Poly([1]) # This is the polynomial f(x) = 1
    one = Poly.field(1)

    # Each lagrange polynomial will be degree-k or smaller
    k = len(xs) - 1
    
    # TODO: Your code goes here
    for xj in xs:
        pass
    return Poly([1])



#####################################
# Problem 1.3: Lagrange Interpolation [5pts]
#####################################

def interpolate(Poly, points):
    k = len(points) - 1
    xs = [point[0] for point in points]
    f = Poly([0])
    # TODO: Your code goes here
    return f


########
# Tests
########

if __name__ == '__main__':
    Fp = FiniteField(p=53,m=1) # Finite field is specified with a prime p
    Poly = polynomialsOver(Fp)

    # Problem 1.1: Polynomial evaluation

    poly1 = Poly([0, 1])  # y = x
    for i in range(10):
        assert eval_poly(poly1,i) == i
    poly2 = Poly([10, 0, 1])  # y = x^2 + 10
    for i in range(10):
        assert eval_poly(poly2,i) == pow(i, 2) + 10


    # Problem 1.2: Lagrange polynomials
    
    # Check the properties of the lagrange polynomial

    k = 10
    xs = list(range(Fp.p)) # Good for small p
    random.shuffle(xs)
    xs = xs[:k+1]
    for xi in xs:
        pi = lagrange_polynomial(Poly, xs, xi)
        for xj in xs:
            if xi == xj:
                assert eval_poly(pi, Fp(xj)) == 1
            else:
                assert eval_poly(pi, Fp(xj)) == 0

    # Problem 1.3: interpolation
    # Generate a random polynomial,
    def random_poly(k):
        return Poly([random.randint(0,Fp.p-1) for _ in range(k+1)])
    # Check the interpolation, randomly test function equality
    poly3 = random_poly(k)
    ys = [eval_poly(poly3, Fp(x)) for x in xs]
    poly3_ = interpolate(Poly, list(zip(xs, ys)))
    assert poly3_.degree() <= poly3.degree()
    for _ in range(10):
        x = random.randint(0,Fp.p-1)
        assert eval_poly(poly3_,x) == eval_poly(poly3,x)

