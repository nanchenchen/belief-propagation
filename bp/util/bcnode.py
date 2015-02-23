import table

class BCNode:
    def __init__(self, name):
        self.name = name


        self.connected_nodes = []
        self.message_from_connections = {}
        self.message_to_connections = {}

    def get_from_message_from_by_var(self, var):
        return self.message_from_connections[var.name]
    def get_from_message_by_idx(self, idx):
        return self.get_from_message_from_by_var(self.connected_nodes[idx])

    def add_connection(self, node):
        self.connected_nodes.append(node)
        self.message_to_connections[node.name] = self.table


    def form_message_to_node(self, target_node):
        pass

    def update(self):
        for connection in self.connected_nodes:
            self.message_from_connections[connection.name] = connection.message_to_connections[self.name]

        for connection in self.connected_nodes:
            self.message_to_connections[connection.name] = self.form_message_to_node(connection)


class BCVarNode(BCNode):
    def __init__(self, name, states):
        super(BCVarNode, self).__init__(name)
        self.states = states
        self.table = table.PotentialTable()
        self.table.nodes.append(self)
        self.table.init_table(value=1.0)

    def form_message_to_node(self, target_node):
        new_message = self.get_from_message_by_idx(0)
        for i in range(1,len(self.connected_nodes)):
            if self.connected_nodes[i] == target_node:
                continue
            new_message = new_message.multiply(self.get_from_message_by_idx(i))
        return new_message

    def update_table(self):
        new_table = self.get_from_message_by_idx(0)
        for i in range(1,len(self.connected_nodes)):
            new_table = new_table.multiply(self.get_from_message_by_idx(i))
        self.table = new_table



class BCFactorNode(BCNode):
    def __init__(self, name, nodes):
        super(BCFactorNode, self).__init__(name)
        self.table = table.PotentialTable(nodes=nodes)
        self.table.init_table()
        for node in nodes:
            node.add_connection(self)
            self.add_connection(node)

    def form_message_to_node(self, target_node):
        new_message = self.table
        for connection in self.connected_nodes:
            if connection == target_node:
                continue
            new_message = new_message.multiply(self.get_from_message_by_var(connection))
        for connection in self.connected_nodes:
            if connection == target_node:
                continue
            new_message.sum_out_var_by_var(connection)
        return new_message