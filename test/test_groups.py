import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from groups import Group
import pytest


class TestGroup:
    zero_torelance = 1e-10

    @pytest.fixture(scope='class')
    def get_groups(self):
        cayley_table_C3 = [
            ['e', 'a', 'b'], 
            ['b', 'e', 'a'], 
            ['a', 'b', 'e'],
        ]
        cayley_table_C4 = [
            ['e', 'a', 'b', 'c'], 
            ['b', 'c', 'e', 'a'], 
            ['a', 'b', 'c', 'e'],
            ['c', 'e', 'a', 'b']    
        ]
        cayley_table_D3 = [
            ['e', 'r', 't', 'a', 'b', 'c'],
            ['r', 't', 'e', 'b', 'c', 'a'],
            ['t', 'e', 'r', 'c', 'a', 'b'],
            ['a', 'c', 'b', 'e', 't', 'r'],
            ['b', 'a', 'c', 'r', 'e', 't'],
            ['c', 'b', 'a', 't', 'r', 'e']
        ]
        groups = {
            'C3': Group(cayley_table_C3),
            'C4': Group(cayley_table_C4),
            'D3': Group(cayley_table_D3),
        }
        return groups

    # ==================== Construction of a Group ====================
    def test_sort_cayley_table_by_index(self, get_groups):
        for _, G in get_groups.items():
            index = [row[0] for row in G.cayley_table]
            assert index == G.cayley_table[0]

    def test_are_rearranged_from_the_group(self, get_groups):
        C4 = get_groups['C4']
        assert C4._are_rearranged_from_the_group(['a', 'b', 'c', 'e'])
        assert not C4._are_rearranged_from_the_group(['a', 'a', 'c', 'e'])
    
    def test_get_index(self, get_groups):
        for _, G in get_groups.items():
            for i in range(G.order):
                assert G.i[G.g[i]] == i

    def test_get_inverse(self, get_groups):
        for _, G in get_groups.items():
            for i in range(G.order):
                gi = G.g[i]
                gi_inv = G.inv[G.g[i]]
                assert G.mult[f'{gi}*{gi_inv}'] == G.g[0]

    def test_create_gi_multiply_gj(self, get_groups):
        C4 = get_groups['C4']
        assert C4.mult['a*e'] == 'a' and C4.mult['e*a'] == 'a'
        assert C4.mult['a*a'] == 'b'
        assert C4.mult['a*b'] == 'c' and C4.mult['b*a'] == 'c'
        assert C4.mult['a*c'] == 'e' and C4.mult['c*a'] == 'e'
        assert C4.mult['1*0'] == '1' and C4.mult['0*1'] == '1'
        assert C4.mult['1*1'] == '2'
        assert C4.mult['1*2'] == '3' and C4.mult['2*1'] == '3'
        assert C4.mult['1*3'] == '0' and C4.mult['3*1'] == '0'

    # ==================== Properties of Subgroup ====================
    def test_is_abelian(self, get_groups):
        C4 = get_groups['C4']
        assert C4.is_abelian(C4.g) is True
        D3 = get_groups['D3']
        assert D3.is_abelian(D3.g) is not True
    
    def test_get_sub_cayley_table(self, get_groups):
        D3 = get_groups['D3']
        output = D3.get_sub_cayley_table(['e', 'r', 't', 'a', 'b', 'c'])
        assert output == D3.cayley_table
        output = D3.get_sub_cayley_table(['e'])
        assert output == [['e']]
        output = D3.get_sub_cayley_table(['e', 'a', 't', 'c'])
        result = [['e', 'a', 't', 'c'], ['a', 'e', 'b', 'r'], ['t', 'c', 'r', 'b'], ['c', 't', 'a', 'e']]
        assert output == result
    
    def test_is_subgroup(self, get_groups):
        D3 = get_groups['D3']
        assert D3.is_subgroup(['e']) is True
        assert D3.is_subgroup(['e', 'r', 't', 'a', 'b', 'c']) is True
        assert D3.is_subgroup(['e', 'r', 't']) is True
        assert D3.is_subgroup(['e', 'a']) is True
        assert D3.is_subgroup(['e', 'a', 'b', 'c']) is not True

    def test_find_subgroups(self, get_groups):
        C4 = get_groups['C4']
        assert C4.find_subgroups() == [['e'], ['e', 'b'], ['e', 'a', 'b', 'c']]
        D3 = get_groups['D3']
        output = D3.find_subgroups()
        result = [
            ['e'], 
            ['e', 'a'], ['e', 'b'], ['e', 'c'], 
            ['e', 'r', 't'], 
            ['e', 'r', 't', 'a', 'b', 'c']
        ]
        assert  output == result