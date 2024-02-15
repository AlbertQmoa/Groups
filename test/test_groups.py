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
        C3 = Group(cayley_table_C3)
        C4 = Group(cayley_table_C4)
        return [C3, C4]

    def test_sort_cayley_table_by_index(self, get_groups):
        for G in get_groups:
            index = [row[0] for row in G.cayley_table]
            assert index == G.cayley_table[0]



