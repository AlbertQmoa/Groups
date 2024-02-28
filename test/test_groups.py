import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from groups import Group
import calc
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
    
    def test_is_closed(self, get_groups):
        D3 = get_groups['D3']
        assert D3.is_closed(['e']) is True
        assert D3.is_closed(['e', 'r', 't']) is True
        assert D3.is_closed(['e', 'a', 'b']) is not True

    def test_move_identity_to_index_0(self, get_groups):
        D3 = get_groups['D3']
        assert D3.move_identity_to_index_0(['e', 'a', 'r']) == ['e', 'a', 'r']
        assert D3.move_identity_to_index_0(['a', 'r', 'e']) == ['e', 'a', 'r']

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

    def test_find_subgroup_generated_by_gi(self, get_groups):
        D3 = get_groups['D3']
        output = set(D3.find_subgroup_generated_by_gi('e'))
        result = {'e'}
        assert output == result
        output = set(D3.find_subgroup_generated_by_gi('a'))
        result = {'e', 'a'}
        assert output == result
        output = set(D3.find_subgroup_generated_by_gi('r'))
        result = {'e', 'r', 't'}
        assert output == result
        output = set(D3.find_subgroup_generated_by_gi('t'))
        result = {'e', 'r', 't'}
        assert output == result

        C4 = get_groups['C4']
        output = set(C4.find_subgroup_generated_by_gi('a'))
        result = set(C4.g)
        assert output == result
        output = set(C4.find_subgroup_generated_by_gi('b'))
        result = {'e', 'b'}
        assert output == result
        output = set(C4.find_subgroup_generated_by_gi('c'))
        result = {'e', 'c', 'b', 'a'}
        assert output == result

    def test_find_subgroup_being_abelian_to_gi(self, get_groups):
        for _, G in get_groups.items():
            g_set = set(G.g)
            for gi in G.g:
                a_set = set(G.find_subgroup_being_abelian_to_gi(gi))
                b_set = g_set - a_set
                assert G.is_subgroup(list(a_set)) is True
                for a in a_set: assert G.is_abelian([a, gi]) is True
                for b in b_set: assert G.is_abelian([b, gi]) is not True

    # ==================== Generator ====================
    def test_find_subset_generated_by_gi_list(self, get_groups):
        D3 = get_groups['D3']
        output = set(D3.find_subset_generated_by_gi_list(['e']))
        result = {'e'}
        assert output == result
        output = set(D3.find_subset_generated_by_gi_list(['r', 't']))
        result = {'e', 'r', 't'}
        assert output == result
        output = set(D3.find_subset_generated_by_gi_list(['b', 'c']))
        result =  {'e', 'r', 't', 'a', 'b', 'c'}
        assert output == result

    def test_find_mimal_generating_set(self, get_groups):
        C4 = get_groups['C4']
        output = C4.find_mimal_generating_set()
        results = [['e', 'a'], ['e', 'b'], ['e', 'c']]
        assert output in results

        D3 = get_groups['D3']
        output = set(D3.find_mimal_generating_set())
        results = [
            {'e', 'r', 't'}, {'e', 'r', 'a'}, {'e', 'r', 'b'}, {'e', 'r', 'c'}, 
            {'e', 't', 'a'}, {'e', 't', 'b'}, {'e', 't', 'c'},
            {'e', 'a', 'b'}, {'e', 'a', 'c'},
            {'e', 'b', 'c'},
        ]
        assert output in results

    # ==================== Left Coset and Right Coset ====================
    def test_find_giH(self, get_groups):
        D3 = get_groups['D3']
        H = ['e', 'r', 't']
        assert D3.find_giH('e', H) == H
        output = set(D3.find_giH('r', H))
        result = {'r', 't', 'e'}
        assert output == result

        H = ['e', 'b']
        output = set(D3.find_giH('r', H))
        result = {'r', 'c'}
        assert output == result

    def test_find_Hgi(self, get_groups):
        D3 = get_groups['D3']
        H = ['e', 'r', 't']
        assert D3.find_Hgi(H, 'e') == H
        output = set(D3.find_Hgi(H, 'r'))
        result = {'r', 't', 'e'}
        assert output == result

        H = ['e', 'b']
        output = set(D3.find_Hgi(H, 'r'))
        result = {'r', 'a'}
        assert output == result
    
    def test_find_gH(self, get_groups):
        D3 = get_groups['D3']
        H = ['e', 'r', 't']
        output = D3.find_gH(H)
        result = {
            'e': H,
            'a': ['a', 'c', 'b']
        }
        for key, val in output.items():
            assert key in result
            assert set(val) == set(result[key])
        
        H = ['e', 'a']
        output = D3.find_gH(H)
        result = {
            'e': ['e', 'a'],
            'r': ['r', 'b'],
            't': ['t', 'c']
        }
        for key, val in output.items():
            assert key in result
            assert set(val) == set(result[key])

    def test_find_Hg(self, get_groups):
        D3 = get_groups['D3']
        H = ['e', 'r', 't']
        output = D3.find_Hg(H)
        result = {
            'e': H,
            'a': ['a', 'c', 'b']
        }
        for key, val in output.items():
            assert key in result
            assert set(val) == set(result[key])
        
        H = ['e', 'a']
        output = D3.find_Hg(H)
        result = {
            'e': ['e', 'a'],
            'r': ['r', 'c'],
            't': ['t', 'b']
        }
        for key, val in output.items():
            assert key in result
            assert set(val) == set(result[key])

    # ========================== Conjugate and Class =====================
    def test_are_x_and_y_conjugated(self, get_groups):
        D3 = get_groups['D3']
        assert D3.are_x_and_y_conjugated('e', 'e') is True
        assert D3.are_x_and_y_conjugated('e', 'r') is not True
        assert D3.are_x_and_y_conjugated('r', 't') is True
        assert D3.are_x_and_y_conjugated('a', 'b') is True
        assert D3.are_x_and_y_conjugated('c', 'a') is True
        assert D3.are_x_and_y_conjugated('a', 'r') is not True

    def test_calc_g_x_ginv(self, get_groups):
        D3 = get_groups['D3']
        assert D3.calc_g_x_ginv('e', 'r') == 'e'
        assert D3.calc_g_x_ginv('r', 't') == 'r'
        assert D3.calc_g_x_ginv('r', 'a') == 't'

    def test_are_all_elements_conjugated_to_each_other(self, get_groups):
        D3 = get_groups['D3']
        assert D3.are_all_elements_conjugated_to_each_other([]) is not True
        assert D3.are_all_elements_conjugated_to_each_other(['r']) is True
        assert D3.are_all_elements_conjugated_to_each_other(['r', 't']) is True
        assert D3.are_all_elements_conjugated_to_each_other(['a', 'b']) is True
        assert D3.are_all_elements_conjugated_to_each_other(['r', 'b']) is not True

    def test_find_all_elemets_conjugate_to_x(self, get_groups):
        for _, G in get_groups.items():
            for x in G.g:
                output = set(G.find_all_elemets_conjugate_to_x(x))
                result = set()
                a_list = G.find_subgroup_being_abelian_to_gi(x)
                gA_dict = G.find_gH(a_list)
                for gi in gA_dict:
                    gxginv = G.mult[f'{x}*{G.inv[gi]}']
                    gxginv = G.mult[f'{gi}*{gxginv}']
                    result.add(gxginv)
                assert output == result
                    
    def test_find_all_conjugated_class(self, get_groups):
        D3 = get_groups['D3']
        Cx_list = [set(Cx) for Cx in D3.find_all_conjugated_class()]
        assert len(Cx_list) == 3
        assert {'e'} in Cx_list
        assert {'r', 't'} in Cx_list
        assert {'a', 'b', 'c'} in Cx_list

    # ========================== Normal Group ==========================
    def test_is_normal_subgroup(self, get_groups):
        D3 = get_groups['D3']
        assert D3.is_normal_subgroup(['e']) is True 
        assert D3.is_normal_subgroup(['e', 'r', 't']) is True 
        assert D3.is_normal_subgroup(['e', 'r', 't', 'a', 'b', 'c']) is True 
        assert D3.is_normal_subgroup(['e', 'a']) is not True 
        assert D3.is_normal_subgroup(['e', 'b']) is not True 
        assert D3.is_normal_subgroup(['e', 'c']) is not True 

    def test_find_normal_subgroups(self, get_groups):
        D3 = get_groups['D3']
        N_list = D3.find_normal_subgroups()
        output = [set(N) for N in N_list]
        result = [{'e'}, {'e', 'r', 't'}, {'e', 'r', 't', 'a', 'b', 'c'}]
        assert len(output) == len(result)
        for N in output: assert N in result

        C4 = get_groups['C4']
        H_list = C4.find_subgroups()
        N_list = C4.find_normal_subgroups()
        output = [set(N) for N in N_list]
        result = [set(H) for H in H_list]
        assert len(output) == len(result)
        for N in output: assert N in result

    # ========================== Quotient Group ==========================
    def test_find_cayley_table_of_quotient_group_given_normal_subgroups(self, get_groups):
        D3 = get_groups['D3']
        output = D3.find_cayley_table_of_quotient_group_given_normal_subgroups(D3.g)
        assert output == [['q0']]
        output = D3.find_cayley_table_of_quotient_group_given_normal_subgroups(['e', 'r', 't'])
        assert output == [['q0', 'q1'], ['q1', 'q0']]
        output = D3.find_cayley_table_of_quotient_group_given_normal_subgroups(['e'])
        assert output == [
            ['q0', 'q1', 'q2', 'q3', 'q4', 'q5'],
            ['q1', 'q2', 'q0', 'q4', 'q5', 'q3'],
            ['q2', 'q0', 'q1', 'q5', 'q3', 'q4'],
            ['q3', 'q5', 'q4', 'q0', 'q2', 'q1'],
            ['q4', 'q3', 'q5', 'q1', 'q0', 'q2'],
            ['q5', 'q4', 'q3', 'q2', 'q1', 'q0']
        ]
    
    def test_findfind_quotient_group_given_normal_sugroup(self, get_groups):
        D3 = get_groups['D3']
        output = D3.find_quotient_group_given_normal_sugroup(D3.g)
        assert output.cayley_table == [['q0']]
        output = D3.find_quotient_group_given_normal_sugroup(['e', 'r', 't'])
        assert output.cayley_table == [['q0', 'q1'], ['q1', 'q0']]
        output = D3.find_quotient_group_given_normal_sugroup(['e'])
        assert output.cayley_table == [
            ['q0', 'q1', 'q2', 'q3', 'q4', 'q5'],
            ['q1', 'q2', 'q0', 'q4', 'q5', 'q3'],
            ['q2', 'q0', 'q1', 'q5', 'q3', 'q4'],
            ['q3', 'q5', 'q4', 'q0', 'q2', 'q1'],
            ['q4', 'q3', 'q5', 'q1', 'q0', 'q2'],
            ['q5', 'q4', 'q3', 'q2', 'q1', 'q0']
        ]

    def test_find_quotient_groups(self, get_groups):
        D3 = get_groups['D3']
        output = D3.find_quotient_groups()
        assert output[2].cayley_table == [['q0']]
        assert output[1].cayley_table == [['q0', 'q1'], ['q1', 'q0']]
        assert output[0].cayley_table == [
            ['q0', 'q1', 'q2', 'q3', 'q4', 'q5'],
            ['q1', 'q2', 'q0', 'q4', 'q5', 'q3'],
            ['q2', 'q0', 'q1', 'q5', 'q3', 'q4'],
            ['q3', 'q5', 'q4', 'q0', 'q2', 'q1'],
            ['q4', 'q3', 'q5', 'q1', 'q0', 'q2'],
            ['q5', 'q4', 'q3', 'q2', 'q1', 'q0']
        ]