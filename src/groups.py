import sys
import random
import calc


class Group:
    def __init__(self, cayley_table):
        # cayley_table is a list of list, where cayley_table[0] was assumed to be {e, ...}
        self.cayley_table = self._sort_cayley_table_by_index(cayley_table)
        self.order = len(cayley_table[0])
        self.g = cayley_table[0]
        self.i = self._get_index()
        self.inv = self._get_inverse()
        self.mult = self._create_gi_multiply_gj(cayley_table)
        self._check_validation_of_cayley_table()

    def __str__(self):
        result = "    " + "  ".join(self.g) + "\n"
        result += '-' * (self.order * 3 + 2) + "\n"
        for row in self.cayley_table:
            row_str = row[0] + " | " + "  ".join(str(elem) for elem in row)
            result += row_str + "\n"
        return result

    # ==================== Construction of a Group ====================
    def _sort_cayley_table_by_index(self, cayley_table):
        sorted_caley_table = list()
        for g in cayley_table[0]:
            find_g = False
            for row in cayley_table:
                if row[0] == g:
                    find_g = True
                    sorted_caley_table.append(row)
                    break
            if not find_g:
                raise ValueError(f'Cannot find {g} in the index of cayley_table.')
        return sorted_caley_table

    def _are_rearranged_from_the_group(self, elements):
        return sorted(elements) == sorted(self.g)
    
    def _get_index(self):
        output = dict()
        for i in range(self.order):
            output[self.g[i]] = i
        return output

    def _get_inverse(self):
        output = dict()
        for j in range(self.order):
            for i in range(self.order):
                if self.cayley_table[i][j] == self.g[0]:
                    output[self.g[j]] = self.cayley_table[i][0]
        return output

    def _create_gi_multiply_gj(self, cayley_table):
        mult = dict()
        order = len(cayley_table[0])
        for i in range(order):
            for j in range(order):
                gi = cayley_table[i][0]
                gj = cayley_table[0][j]
                gigj = f'{gi}*{gj}'
                mult[gigj] = cayley_table[i][j]
                idx = self.i[gi]
                mult[f'{idx}*{j}'] = str(self.i[mult[gigj]])
        return mult

    def _check_validation_of_cayley_table(self):
        # --- Check the order ---
        if len(self.cayley_table) != self.order:
            raise ValueError('cayley_table is not n * n')
        # --- Check rearrangement ---
        for row in self.cayley_table:
            if not self._are_rearranged_from_the_group(row):
                raise ValueError(f'j direction: {row} is not rearranged from G')
        for j in range(self.order):
            row = [self.cayley_table[i][j] for i in range(self.order)]
            if not self._are_rearranged_from_the_group(row):
                raise ValueError(f'i direction: {row} is not rearranged from G')
        # --- Check associative law ---
        for i in range(self.order):
            for j in range(self.order):
                for k in range(self.order):
                    ij = self.mult[f'{i}*{j}']
                    jk = self.mult[f'{j}*{k}']
                    if self.mult[f'{ij}*{k}'] != self.mult[f'{i}*{jk}']:
                        raise ValueError(f'{self.g[i]}*{self.g[j]}*{self.g[k]} violates the assicuative law')

    def _check_if_x_in_the_group(self, x):
        if x not in self.g: raise ValueError(f'{x} is not in the group {self.g}')

    # ==================== Properties of Subgroup ====================
    def is_abelian(self, elements):
        size = len(elements)
        g = elements
        for i in range(size):
            for j in range(size):
                gigj = self.mult[f'{g[i]}*{g[j]}']
                gjgi = self.mult[f'{g[j]}*{g[i]}']
                if gigj != gjgi: return False
        return True

    def is_closed(self, elements):
        sub_table = self.get_sub_cayley_table(elements)
        for row in sub_table:
            if set(row) != set(elements):
                return False
        return True

    def move_identity_to_index_0(self, elements):
        output = elements[:]
        if self.g[0] not in output: raise ValueError('There is no identity in the elements')
        if output[0] == self.g[0]: return output
        output.remove(self.g[0])
        output.insert(0, self.g[0])
        return output

    def get_sub_cayley_table(self, elements):
        list_ = self.move_identity_to_index_0(elements)
        idx_list = [self.i[g] for g in list_]
        output = list()
        for i in idx_list:
            output.append([self.cayley_table[i][j] for j in idx_list])
        return output

    def print_sub_cayley_table(self, elements):
        table = self.get_sub_cayley_table(elements)
        for row in table: print(row)

    def _are_two_lists_rearranged(self, list1, list2):
        return sorted(list1) == sorted(list2)

    def is_subgroup(self, elements):
        if len(elements) < 1 or elements is None: return False
        table = self.get_sub_cayley_table(elements)
        for row in table:
            if not self._are_two_lists_rearranged(row, elements): return False
        size = len(elements)
        for j in range(size):
            row = [table[i][j] for i in range(size)]
            if not self._are_two_lists_rearranged(row, elements): return False
        return True

    def find_subgroups(self):
        factors = calc.find_factors(self.order)
        elemets_without_g0 = self.g[1:]
        size_list = [n - 1 for n in factors]
        temp_list = calc.find_subsets(elemets_without_g0, size_list)
        subsets = [[self.g[0]] + tmp for tmp in temp_list]
        output = [elements for elements in subsets if self.is_subgroup(elements)]
        return output

    def find_subgroup_generated_by_gi(self, gi):
        if gi not in self.g: raise ValueError(f'{gi} is not in the group G')
        output = {self.g[0], gi}
        gi_n = gi
        while gi_n != self.g[0]:
            gi_n = self.mult[f'{gi_n}*{gi}']
            output.add(gi_n)
        return list(output)

    def find_subgroup_being_abelian_to_gi(self, gi):
        output = list()
        for gj in self.g:
            if self.is_abelian([gj, gi]):
                output.append(gj)
        return output

    # ==================== Generator ====================
    def find_subset_generated_by_gi_list(self, elements):
        set_ = set(elements)
        if self.g[0] not in elements: set_.add(self.g[0])
        output = list(set_)
        while not self.is_closed(output):
            sub_table = self.get_sub_cayley_table(output)
            for row in sub_table:
                set_.update(row)
            output = list(set_)
        return output

    def find_a_generating_set(self):
        G_set, A_set, output = set(self.g), {self.g[0]}, [self.g[0]]
        S_set = G_set - A_set
        while len(S_set) > 0:
            list_ = list(S_set)
            s0 = list_.pop(random.randint(0, len(list_)-1))
            output.append(s0)
            A_set = set(self.find_subset_generated_by_gi_list(output))
            S_set = G_set - A_set
        output = self.move_identity_to_index_0(output)
        return output

    def find_mimal_generating_set(self):
        num_iter = 10000
        size_min = sys.maxsize
        count = 0
        while count < num_iter:
            temp = self.find_a_generating_set()
            size = len(temp)
            if size < size_min:
                output = temp
                size_min = size
            count += 1
        return output

    # ==================== Left Coset and Right Coset ====================
    def find_giH(self, gi, H):
        if not self.is_subgroup(H): raise ValueError(f'H is not a subgroup')
        return [self.mult[f'{gi}*{hj}'] for hj in H]

    def find_Hgi(self, H, gi):
        if not self.is_subgroup(H): raise ValueError(f'H is not a subgroup')
        return [self.mult[f'{hj}*{gi}'] for hj in H]

    def find_gH(self, H):
        if not self.is_subgroup(H): raise ValueError(f'H is not a subgroup')
        output = dict()
        giH_list = list()
        for gi in self.g:
            giH = set(self.find_giH(gi, H))
            if giH not in giH_list:
                giH_list.append(giH) 
                output[gi] = list(giH)
        assert self.order % len(giH_list) == 0
        return output

    def find_Hg(self, H):
        if not self.is_subgroup(H): raise ValueError(f'H is not a subgroup')
        output = dict()
        Hgi_list = list()
        for gi in self.g:
            Hgi = set(self.find_Hgi(H, gi))
            if Hgi not in Hgi_list:
                Hgi_list.append(Hgi) 
                output[gi] = list(Hgi)
        assert self.order % len(Hgi_list) == 0
        return output

    # ========================== Conjugate and Class =====================
    def are_x_and_y_conjugated(self, x, y):
        if x == y: return True
        if x == self.g[0] or y == self.g[0]: return False
        for gi in self.g:
            if self.mult[f'{x}*{gi}'] == self.mult[f'{gi}*{y}']:
                return True
        return False

    def calc_g_x_ginv(self, x, g):
        x_ginv = self.mult[f'{x}*{self.inv[g]}']
        gxginv = self.mult[f'{g}*{x_ginv}']
        return gxginv

    def are_all_elements_conjugated_to_each_other(self, elements):
        for gi in elements: self._check_if_x_in_the_group(gi)
        size = len(elements)
        if size == 0: return False
        if size == 1: return True
        for i in range(size):
            for j in range(i+1, size):
                if not self.are_x_and_y_conjugated(elements[i], elements[j]):
                    return False
        return True
    
    def find_all_elemets_conjugate_to_x(self, x):
        self._check_if_x_in_the_group(x)
        if x == self.g[0]: return [self.g[0]]
        output = list()
        for gi in self.g:
            if self.are_x_and_y_conjugated(gi, x):
                output.append(gi)
        return output

    def find_all_conjugated_class(self):
        output = list()
        for x in self.g:
            Cx = set(self.find_all_elemets_conjugate_to_x(x))
            if Cx not in output: output.append(Cx)
        return [set(Cx) for Cx in output]

    # ========================== Normal Group ==========================
    def is_normal_subgroup(self, elements):
        if not self.is_subgroup(elements): raise ValueError(f'{elements} is not a subgroup')
        for x in elements:
            for g in self.g:
                if self.calc_g_x_ginv(x, g) not in elements: return False
        return True

    def find_normal_subgroups(self):
        subgroup_list = self.find_subgroups()
        output = list()
        for elements in subgroup_list:
            if self.is_normal_subgroup(elements):
                output.append(elements)
        return output

    # ========================== Quotient Group ==========================
    def find_cayley_table_of_quotient_group_given_normal_subgroups(self, elements):
        if not self.is_normal_subgroup(elements): raise ValueError(f'{elements} is not a normal subgroup')
        
        # ------ cosets = {g0N, giN, gjN, gkN, ...}
        cosets = self.find_gH(elements)

        # ------ worker = [(g0, g0N), (gi, giN), (gj, gjN), (gk, gkN) ...] ------
        worker = [(self.g[0], cosets[self.g[0]])]
        for gi, giN in cosets.items():
            if gi != self.g[0]:
                worker.append((gi, giN))
        
        # ------ create cayley_table of the quotient_group: Qk = Qi * Qj ------
        # [Q0, Q1, Q2, Q3, ...] and [g0N, giN, gjN, gkN, ...] are one to one
        size = len(worker)
        table = list()
        for i in range(size):
            row = list()
            for j in range(size):
                # to find k for Qk = Qi * Qj
                gigj =  self.mult[f'{worker[i][0]}*{worker[j][0]}']
                for k in range(size):
                    if gigj in worker[k][1]:
                        row.append(f'q{k}')
                        break
            table.append(row)
        
        # ------ do some basic check ------
        for row in table: assert self._are_two_lists_rearranged(row, table[0])
        return table

    def find_quotient_group_given_normal_sugroup(self, elements):
        table = self.find_cayley_table_of_quotient_group_given_normal_subgroups(elements)
        Q = Group(table)
        assert Q.is_subgroup(Q.g)
        return Q

    def find_quotient_groups(self):
        normal_subgroups = self.find_normal_subgroups()
        Q_list = list()
        for elements in normal_subgroups:
            Q = self.find_quotient_group_given_normal_sugroup(elements)
            Q_list.append(Q)
        return Q_list


if __name__ == '__main__':
    cayley = [
        ['e', 'a', 'b', 'c'], 
        ['b', 'c', 'e', 'a'], 
        ['a', 'b', 'c', 'e'],
        ['c', 'e', 'a', 'b']    
    ]
    C4 = Group(cayley)
    print(C4)
    print(C4.mult)
    C4.print_sub_cayley_table(['e', 'a', 'c'])
    print(C4.find_subgroups())
