import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import calc


def test_find_factors():
    assert calc.find_factors(1) == [1]
    assert calc.find_factors(2) == [1, 2]
    assert calc.find_factors(3) == [1, 3]
    assert calc.find_factors(4) == [1, 2, 4]
    assert calc.find_factors(8) == [1, 2, 4, 8]


def test_find_subsets():
    output = calc.find_subsets(['a', 'b', 'c'], [1, 2, 3])
    assert output == [['a'], ['b'], ['c'], ['a', 'b'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']]
    output = calc.find_subsets(['a', 'b', 'c', 'd'], [2])
    assert output == [['a', 'b'], ['a', 'c'], ['a', 'd'], ['b', 'c'], ['b', 'd'], ['c', 'd']]


