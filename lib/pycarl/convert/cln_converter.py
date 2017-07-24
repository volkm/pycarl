import pycarl

def convert_integer(integer):
    if isinstance(integer, pycarl.cln.Integer):
        return integer
    elif isinstance(integer, pycarl.gmp.Integer):
        return pycarl.cln.Integer(integer)
    else:
        raise TypeError("Integer of type {} cannot be convert to cln".format(type(integer)))

def convert_rational(rational):
    if isinstance(rational, pycarl.cln.Rational):
        return rational
    elif isinstance(rational, pycarl.gmp.Rational):
        return pycarl.cln.Rational(rational)
    else:
        raise TypeError("Rational of type {} cannot be convert to cln".format(type(rational)))

def convert_term(term):
    if isinstance(term, pycarl.cln.Term):
        return term
    elif isinstance(term, pycarl.gmp.Term):
        coeff = convert_rational(term.coeff)
        return pycarl.cln.Term(coeff, term.monomial)
    else:
        raise TypeError("Term of type {} cannot be convert to cln".format(type(term)))

def convert_polynomial(polynomial):
    if isinstance(polynomial, pycarl.cln.Polynomial):
        return polynomial
    elif isinstance(polynomial, pycarl.gmp.Polynomial):
        terms = []
        for term in polynomial:
            terms.append(convert_term(term))
        return pycarl.cln.Polynomial(terms)
    else:
        raise TypeError("Polynomial of type {} cannot be convert to cln".format(type(polynomial)))

def convert_rational_function(ratfunc):
    if isinstance(ratfunc, pycarl.cln.RationalFunction):
        return ratfunc
    elif isinstance(ratfunc, pycarl.gmp.RationalFunction):
        numerator = convert_polynomial(ratfunc.numerator)
        denominator = convert_polynomial(ratfunc.denominator)
        return pycarl.cln.RationalFunction(numerator, denominator)
    else:
        raise TypeError("Rational function of type {} cannot be convert to cln".format(type(ratfunc)))

def convert_factorized_polynomial(polynomial):
    if isinstance(polynomial, pycarl.cln.FactorizedPolynomial):
        return polynomial
    elif isinstance(polynomial, pycarl.gmp.FactorizedPolynomial):
        coefficient = convert_rational(polynomial.coefficient())
        converted = pycarl.cln.FactorizedPolynomial(coefficient)
        for (factor, exponent) in polynomial.factorization():
            pol = convert_polynomial(factor.polynomial())
            factorized = pycarl.cln.create_factorized_polynomial(pol)
            converted *= factorized ** exponent
        return converted
    else:
        raise TypeError("Factorized polynomial of type {} cannot be convert to cln".format(type(polynomial)))

def convert_factorized_rational_function(ratfunc):
    if isinstance(ratfunc, pycarl.cln.FactorizedRationalFunction):
        return ratfunc
    elif isinstance(ratfunc, pycarl.gmp.FactorizedRationalFunction):
        numerator = convert_factorized_polynomial(ratfunc.numerator)
        denominator = convert_factorized_polynomial(ratfunc.denominator)
        return pycarl.cln.FactorizedRationalFunction(numerator, denominator)
    else:
        raise TypeError("Factorized rational function of type {} cannot be convert to cln".format(type(ratfunc)))

def convert(data):
    if isinstance(data, pycarl.cln.Integer) or isinstance(data, pycarl.gmp.Integer):
        return convert_integer(data)
    elif isinstance(data, pycarl.cln.Rational) or isinstance(data, pycarl.gmp.Rational):
        return convert_rational(data)
    elif isinstance(data, pycarl.cln.Term) or isinstance(data, pycarl.gmp.Term):
        return convert_term(data)
    elif isinstance(data, pycarl.cln.Polynomial) or isinstance(data, pycarl.gmp.Polynomial):
        return convert_polynomial(data)
    elif isinstance(data, pycarl.cln.RationalFunction) or isinstance(data, pycarl.gmp.RationalFunction):
        return convert_rational_function(data)
    elif isinstance(data, pycarl.cln.FactorizedPolynomial) or isinstance(data, pycarl.gmp.FactorizedPolynomial):
        return convert_factorized_polynomial(data)
    elif isinstance(data, pycarl.cln.FactorizedRationalFunction) or isinstance(data, pycarl.gmp.FactorizedRationalFunction):
        return convert_factorized_rational_function(data)
    else:
        raise TypeError("Unknown type {} for conversion to cln".format(type(data)))

