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
        groups = {
            'C3': Group(cayley_table_C3),
            'C4': Group(cayley_table_C4)
        }
        return groups

    def test_sort_cayley_table_by_index(self, get_groups):
        for _, G in get_groups.items():
            index = [row[0] for row in G.cayley_table]
            assert index == G.cayley_table[0]

    def test_are_rearranged_from_the_group_elements(self, get_groups):
        C4 = get_groups['C4']
        assert C4.are_rearranged_from_the_group_elements(['a', 'b', 'c', 'e'])
        assert not C4.are_rearranged_from_the_group_elements(['a', 'a', 'c', 'e'])
    
    def test_get_index_of_gi(self, get_groups):
        for _, G in get_groups.items():
            for i in range(G.order):
                assert G.get_index_of_gi(G.g[i]) == i

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


