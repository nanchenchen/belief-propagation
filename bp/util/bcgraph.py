from bcnode import *

class BCGraph:
    def __init__(self):
        self.var_nodes = []
        self.factor_nodes = []
        self.nodes_dict = {}


    def build_graph_from_BN(self, bn_nodes):
        for node in bn_nodes:
            bc_node = BCNode(node.name, list(node.states))
            self.var_nodes.append(bc_node)
            self.nodes_dict[node.name] = bc_node

        for node in bn_nodes:
            key_list = [self.nodes_dict[node.name]]
            for pa in node.parents:
                key_list.append(self.nodes_dict[pa.name])

            node_name = str(tuple(map(lambda x: x.name, key_list)))

            factor_node = BCFactorNode(node_name, key_list)
            self.var_nodes.append(factor_node)
            self.nodes_dict[factor_node.name] = factor_node
            for row in node.theCPD:
                row_list = list(row)
                setting = []
                for i in range(len(key_list)):
                    setting.append((key_list[i], row_list[i]))
                factor_node.table.set_row_value(setting, node.theCPD[row])






