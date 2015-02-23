import json
from ast import literal_eval as make_tuple

class PotentialTable:
    def __init__(self, nodes=None, table=None):
        if nodes is None:
            self.nodes = []
        if table is None:
            self.table = {}
    
    def _get_state_list(self):
        states = [];
        tmp_list = [];
        def _permutation(self, idx):
            if idx == len(self.nodes):
                states.append(tuple(tmp_list))
                return
            else:
                for s in self.nodes[idx].states:
                    tmp_list.append(s)
                    self._permutation(idx + 1)
                    tmp_list.pop()
        return states 
    
    def _init_table(self):
        states = self._get_state_list()
        for state in states:
            table[state] = 0.0
    
    def set_nodes(self, nodes):
        pass
        
    
    def set_table(self, table);
        pass

    def sum_out_var(self, var):
        pass
        
    def multiply(self, PT):
        pass
        
    def get_json(self):
        return json.dumps(dict([(str(key), val) for key, val in self.table.iteritems()]))
        
    def set_table_from_json_str(self, json_str):
        tmp_obj = json.loads(json_str)
        self.table = dict([(make_tuple(key), val) for key, val in self.table.iteritems()])