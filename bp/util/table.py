import json
from ast import literal_eval as make_tuple
from operator import attrgetter
import collections

class PotentialTable(object):

    def __init__(self, nodes=None, table=None):
        #from nose.tools import set_trace; set_trace()
        if nodes is None:
            nodes = []
        self.nodes = sorted(set(nodes), key=attrgetter('name'))

        if table is None:
            table = {}
        self.table = table

    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        output = str(tuple(self.nodes))
        for key in self.table:
            output += "%s  | %f" %( str(self.get_row_setting(key)), self.table[key]) + "\n"
        return output

    def _get_state_list(self):
        states = []
        tmp_list = []
        def _permutation(idx):
            if idx == len(self.nodes):
                states.append(tuple(tmp_list))
                return
            else:
                for s in self.nodes[idx].states:
                    tmp_list.append(s)
                    _permutation(idx + 1)
                    tmp_list.pop()
        _permutation(0)
        return states 
    
    def init_table(self, value=0.0):
        states = self._get_state_list()
        for state in states:
            self.table[state] = value
    
    def set_nodes(self, nodes):
        self.nodes = sorted(set(nodes), key=attrgetter('name'))
    
    def set_table(self, table):
        self.table = table

    def sum_out_var_by_idx(self, var_idx):

        def _pop_tuple_element(t, idx):
            l = list(t)
            l.pop(idx)
            return tuple(l)

        new_node_list = list(self.nodes)
        new_node_list.pop(var_idx)

        new_table = PotentialTable(nodes=new_node_list)
        new_table.init_table()

        #from nose.tools import set_trace; set_trace()

        for key in self.table:
            new_table.table[_pop_tuple_element(key, var_idx)] += self.table[key]

        return new_table

    def sum_out_var_by_var(self, var):
        return self.sum_out_var_by_idx(self.nodes.index(var))


    def set_row_value(self, row_setting, value):
        """
            row_setting = [(var, state), (var, state)...]
        """
        sorted_setting = sorted(row_setting, key=lambda tup: tup[0].name)
        states = []
        for var, state in sorted_setting:
            if var in self.nodes:
                states.append(state)
        self.table[tuple(states)] = value

    def get_row_value(self, row_setting):
        """
            row_setting = [(var, state), (var, state)...]
        """
        sorted_setting = sorted(row_setting, key=lambda tup: tup[0].name)
        states = []
        for var, state in sorted_setting:
            if var in self.nodes:
                states.append(state)
        return self.table[tuple(states)]

    def get_row_setting(self, key):
        setting = []
        for i in range(len(self.nodes)):
            setting.append((self.nodes[i], key[i]))
        return setting

    def multiply(self, PT):
        new_node_list = sorted(set(self.nodes).union(set(PT.nodes)), key=attrgetter('name'))
        new_table = PotentialTable(nodes=new_node_list)
        new_table.init_table()

        for key in new_table.table:
            setting = new_table.get_row_setting(key)
            new_table.table[key] = self.get_row_value(setting) * PT.get_row_value(setting)

        return new_table

    def show_table(self):
        print "Table %s" %(str(tuple(self.nodes)))
        for key in self.table:
            print "%s  | %f" %( str(self.get_row_setting(key)), self.table[key])

    def get_json(self):
        return json.dumps(dict([(str(key), val) for key, val in self.table.iteritems()]))
        
    def set_table_from_json_str(self, json_str):
        tmp_obj = json.loads(json_str)
        self.table = dict([(make_tuple(key), val) for key, val in tmp_obj.iteritems()])
        #from nose.tools import set_trace; set_trace()

    def normalize(self):
        denominator = 0
        for key in self.table:
            denominator += self.table[key]
        for key in self.table:
            self.table[key] /= denominator

    def diff(self, PT):
        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

        if not compare(self.nodes, PT.nodes):
            return True, -1

        diff_value = 0
        for key in self.table:
            diff_value += abs(self.table[key] - PT.table[key])

        if diff_value > 0:
            return True, diff_value
        else:
            return False, 0

