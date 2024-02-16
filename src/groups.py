

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
        result = "   " + "  ".join(self.g) + "\n"
        for row in self.cayley_table:
            row_str = row[0] + "  " + "  ".join(str(elem) for elem in row)
            result += row_str + "\n"
        return result

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

    def _are_rearranged_from_the_group_elements(self, a_list):
        return sorted(a_list) == sorted(self.g)
    
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
            if not self._are_rearranged_from_the_group_elements(row):
                raise ValueError(f'j direction: {row} is not rearranged from G')
        for j in range(self.order):
            row = [self.cayley_table[i][j] for i in range(self.order)]
            if not self._are_rearranged_from_the_group_elements(row):
                raise ValueError(f'i direction: {row} is not rearranged from G')
        # --- Check associative law ---
        for i in range(self.order):
            for j in range(self.order):
                for k in range(self.order):
                    ij = self.mult[f'{i}*{j}']
                    jk = self.mult[f'{j}*{k}']
                    if self.mult[f'{ij}*{k}'] != self.mult[f'{i}*{jk}']:
                        raise ValueError(f'{self.g[i]}*{self.g[j]}*{self.g[k]} violates the assicuative law')
    
    def is_abelian(self, group_list):
        size = len(group_list)
        g = group_list
        for i in range(size):
            for j in range(size):
                gigj = self.mult[f'{g[i]}*{g[j]}']
                gjgi = self.mult[f'{g[j]}*{g[i]}']
                if gigj != gjgi: return False
        return True


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