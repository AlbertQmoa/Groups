

class Group:
    def __init__(self, cayley_table):
        # cayley_table is a list of list, where cayley_table[0] was assumed to be {e, ...}
        self.cayley_table = self._sort_cayley_table_by_index(cayley_table)
        self.g = cayley_table[0]
        self._col = cayley_table[0]

    def __str__(self):
        result = "   " + "  ".join(self._col) + "\n"
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

    def are_rearranged_from_the_group_elements(self, array):
        pass


    def _is_cayley_table_validated(self):
        # Check the validation of the cayley table
        return True
    
    def find_inverse(self, element):
        # 查找并返回给定元素的逆元
        pass

    def multiply(self, a, b):
        # 返回元素a和b的乘积
        return self.table[a][b]
    
    def is_abelian(self):
        # 检查群是否为阿贝尔群的实现代码
        pass


if __name__ == '__main__':
    cayley = [
        ['e', 'a', 'b', 'c'], 
        ['b', 'c', 'e', 'a'], 
        ['a', 'b', 'c', 'e'],
        ['c', 'e', 'a', 'b']    
    ]
    C4 = Group(cayley)
    print(C4)