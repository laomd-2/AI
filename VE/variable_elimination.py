class VariableElimination:
    @staticmethod
    def inference(factor_list, query_variables,
                  ordered_list_of_hidden_variables, evidence_list):
        for ev, v in evidence_list.items():
            for i, factor in enumerate(factor_list):
                new_f = factor.restrict(ev, v)
                if new_f is not None:
                    factor_list[i] = new_f

        for var in ordered_list_of_hidden_variables:
            new_f = None
            for i in range(len(factor_list)):
                factor = factor_list.pop(0)
                if var in factor.var_list:
                    if new_f is None:
                        new_f = factor
                    else:
                        new_f = new_f.multiply(factor)
                else:
                    factor_list.append(factor)
            if new_f is not None:
                new_f = new_f.sum_out(var)
                factor_list.append(new_f)

        res = factor_list[0]
        for factor in factor_list[1:]:
            res = res.multiply(factor)
        Util.normalize(res.cpt, query_variables)
        res.print_inf()

    @staticmethod
    def print_factors(factor_list):
        for factor in factor_list:
            factor.print_inf()


class Util:
    @staticmethod
    def to_binary(num, len):
        return format(num, '0' + str(len) + 'b')

    @staticmethod
    def normalize(cpt, query_variables):
        n = len(query_variables)
        totals = dict()
        for k, v in cpt.items():
            totals[k[n:]] = totals.get(k[n:], 0) + v
        for k in cpt:
            cpt[k] /= totals[k[n:]]

    @staticmethod
    def merge(a, b):
        return a + b

    @staticmethod
    def interaction(l1, l2):
        return list(set(l1).intersection(set(l2)))

    @staticmethod
    def _can_join(t1, t2, common):
        for i, j in common:
            if t1[i] != t2[j]:
                return False
        return True

    @staticmethod
    def join(t1, t2, common):
        if Util._can_join(t1, t2, common):
            res = ""
            tmp = [c[0] for c in common]
            for i, v in enumerate(t1):
                if i not in tmp:
                    res += v
            return res + t2
        else:
            return None


class Node:
    def __init__(self, name, var_list):
        self.name = name
        self.var_list = var_list
        self.cpt = {}

    def set_cpt(self, cpt):
        self.cpt = cpt

    def print_inf(self):
        print("Name = " + self.name)
        print(" vars " + str(self.var_list))
        for key in self.cpt:
            print("   key: " + key + " val : " + str(self.cpt[key]))
        print()

    def get_var_index(self, variable):
        return self.var_list.index(variable)

    def without(self, variable):
        var_index = self.get_var_index(variable)
        return var_index, (self.var_list[:var_index] + self.var_list[var_index + 1:])

    def multiply(self, factor):
        """function that multiplies with another factor"""
        new_cpt = dict()
        common = []
        for c in Util.interaction(self.var_list, factor.var_list):
            common.append((self.get_var_index(c), factor.get_var_index(c)))
        for t1, v1 in self.cpt.items():
            for t2, v2 in factor.cpt.items():
                k = Util.join(t1, t2, common)
                if k is not None:
                    new_cpt[k] = v1 * v2
        new_var_list = self.var_list + factor.var_list
        for i, _ in common:
            new_var_list.pop(i)
        new_node = Node('f' + str(new_var_list), new_var_list)
        new_node.set_cpt(new_cpt)
        return new_node

    def sum_out(self, variable):
        """function that sums out a variable given a factor"""
        # Your code here
        var_index, new_var_list = self.without(variable)
        new_cpt = dict()
        for k, v in self.cpt.items():
            k = k[:var_index] + k[var_index + 1:]
            new_pro = new_cpt.get(k, 0) + v
            new_cpt[k] = new_pro
        # -----------------
        new_node = Node('f' + str(new_var_list), new_var_list)
        new_node.set_cpt(new_cpt)
        return new_node

    def restrict(self, variable, value):
        """function that restricts a variable to some value
        in a given factor"""
        # Your code here
        try:
            var_index, new_var_list = self.without(variable)
            new_cpt = dict()
            for k, v in self.cpt.items():
                if k[var_index] == value:
                    k = k[:var_index] + k[var_index + 1:]
                    new_cpt[k] = v
            # -----------------
            new_node = Node('f' + str(new_var_list), new_var_list)
            new_node.set_cpt(new_cpt)
            return new_node
        except ValueError:
            return None
