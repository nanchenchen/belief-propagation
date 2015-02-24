from bcnode import *

class BCGraph(object):
    def __init__(self):
        self.var_nodes = []
        self.factor_nodes = []
        self.nodes_dict = {}


    def build_graph_from_BN(self, bn_nodes):
        for node in bn_nodes:
            bc_node = BCVarNode(node.name, list(node.states))
            self.var_nodes.append(bc_node)
            self.nodes_dict[node.name] = bc_node

        for node in bn_nodes:
            key_list = [self.nodes_dict[node.name]]
            for pa in node.parents:
                key_list.append(self.nodes_dict[pa.name])

            node_name = str(tuple(map(lambda x: x.name, key_list)))

            factor_node = BCFactorNode(node_name, key_list)
            self.factor_nodes.append(factor_node)
            self.nodes_dict[factor_node.name] = factor_node
            for row in node.dist:
                row_list = list(row)
                setting = []
                for i in range(len(key_list)):
                    setting.append((key_list[i], row_list[i]))
                factor_node.table.set_row_value(setting, node.dist[row])

    def var_to_factor_propagate(self):
        diff_value = 0
        for factor_node in self.factor_nodes:
            diff_value += factor_node.update_incoming_messages()
        for factor_node in self.factor_nodes:
            diff_value += factor_node.update_outgoing_messages()
        return diff_value

    def factor_to_var_propagate(self):
        diff_value = 0
        for var_node in self.var_nodes:
            diff_value += var_node.update_incoming_messages()
        for var_node in self.var_nodes:
            var_node.update_table()
            diff_value += var_node.update_outgoing_messages()
        return diff_value



    def show_graph(self):
        print "vars"
        for var in self.var_nodes:
            print "Node %s" %var
            var.table.show_table()

            print "Message From Connection"
            for connection in var.connected_nodes:
                if var.message_from_connections.get(connection.name):
                    print "%s->%s" %(connection.name, var.name)
                    var.message_from_connections[connection.name].show_table()
            print "Message To Connection"
            for connection in var.connected_nodes:
                if var.message_to_connections.get(connection.name):
                    print "%s->%s" %(var.name, connection.name)
                    var.message_to_connections[connection.name].show_table()
        print "--------------------------------------------"
        print "factors"
        for factor in self.factor_nodes:
            print "Factor %s" % factor
            factor.table.show_table()
            print "Message From Connection"
            for connection in factor.connected_nodes:
                if factor.message_from_connections.get(connection.name):
                    print "%s->%s" %(connection.name, factor.name)
                    factor.message_from_connections[connection.name].show_table()
            print "Message To Connection"
            for connection in factor.connected_nodes:
                if factor.message_to_connections.get(connection.name):
                    print "%s->%s" %(factor.name, connection.name)
                    factor.message_to_connections[connection.name].show_table()

    def show_vars(self):
        print "vars"
        for var in self.var_nodes:
            print "Node %s" %var
            var.table.show_table()
