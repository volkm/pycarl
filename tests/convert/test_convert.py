import pytest

import pycarl
import pycarl.cln
import pycarl.gmp
import pycarl.convert

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from package_selector import PackageSelector

@pytest.mark.parametrize("convert_package,converter", [
        (pycarl.cln,pycarl.convert.cln_converter),
        (pycarl.gmp,pycarl.convert.gmp_converter)
    ], ids=["cln_converter", "gmp_converter"])
class TestConvert(PackageSelector):

    def test_convert_integer(self, package, convert_package, converter):
        original = package.Integer(-4)
        assert isinstance(original, package.Integer)
        converted = converter.convert_integer(original)
        assert isinstance(converted, convert_package.Integer)

    def test_convert_rational(self, package, convert_package, converter):
        original = package.Rational(package.Integer(-1), package.Integer(2))
        assert isinstance(original, package.Rational)
        converted = converter.convert_rational(original)
        assert isinstance(converted, convert_package.Rational)

    def test_convert_term(self, package, convert_package, converter):
        pycarl.clear_variable_pool()
        var = pycarl.Variable("n")
        rational = package.Integer(2) / package.Integer(5)
        monomial = pycarl.create_monomial(var, 2)
        original = package.Term(rational, monomial)
        assert isinstance(original, package.Term)
        converted = converter.convert_term(original)
        assert isinstance(converted, convert_package.Term)

    def test_convert_polynomial(self, package, convert_package, converter):
        pycarl.clear_variable_pool()
        var1 = pycarl.Variable("n")
        var2 = pycarl.Variable("o")
        original = package.Polynomial(4) * var1 * var2 + var1 * var1 + package.Integer(2)
        assert isinstance(original, package.Polynomial)
        converted = converter.convert_polynomial(original)
        assert isinstance(converted, convert_package.Polynomial)
