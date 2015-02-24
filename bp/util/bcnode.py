import table

class BCNode(object):
    def __init__(self, name):
        self.name = name


        self.connected_nodes = []
        self.message_from_connections = {}
        self.message_to_connections = {}

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

    def get_from_message_by_var(self, var):
        return self.message_from_connections[var.name]
    def get_from_message_by_idx(self, idx):
        return self.get_from_message_by_var(self.connected_nodes[idx])

    def add_connection(self, node):
        self.connected_nodes.append(node)
        self.message_to_connections[node.name] = None
        self.message_from_connections[node.name] = None

    def form_message_to_node(self, target_node):
        pass

    def update_incoming_messages(self):
        diff_value = 0.0
        for connection in self.connected_nodes:
            if self.message_from_connections[connection.name] is not None:
                changed, value = self.message_from_connections[connection.name].diff(connection.message_to_connections[self.name])
                if changed and value != -1:
                    self.message_from_connections[connection.name] = connection.message_to_connections[self.name]
                    diff_value += value
            else:
                self.message_from_connections[connection.name] = connection.message_to_connections[self.name]
                diff_value += 1.0
        return diff_value

    def update_outgoing_messages(self):
        diff_value = 0.0
        for connection in self.connected_nodes:
            new_message = self.form_message_to_node(connection)
            if self.message_to_connections[connection.name] is not None:
                changed, value = self.message_to_connections[connection.name].diff(new_message)
                if changed and value != -1:
                    self.message_to_connections[connection.name] = new_message
                    diff_value += value
            else:
                self.message_to_connections[connection.name] = new_message
                diff_value += 1.0

        return diff_value

class BCVarNode(BCNode):
    def __init__(self, name, states):
        super(BCVarNode, self).__init__(name)
        self.states = states
        self.table = table.PotentialTable()
        self.table.nodes.append(self)
        init_value = 1.0 / len(self.states)
        self.table.init_table(value=init_value)

    """def add_connection(self, node):
        super(BCVarNode, self).add_connection(node)
        self.message_to_connections[node.name] = self.table"""

    def form_message_to_node(self, target_node):
        new_message = None
        for i in range(len(self.connected_nodes)):
            if self.connected_nodes[i] == target_node:
                continue
            if new_message is None:
                new_message = self.get_from_message_by_idx(i)
            else:
                msg = self.get_from_message_by_idx(i)
                if msg is not None:
                    new_message = new_message.multiply(msg)
        if new_message is None:
            new_message = table.PotentialTable()
            new_message.nodes.append(self)
            init_value = 1.0 / len(self.states)
            new_message.init_table(value=init_value)
        new_message.normalize()
        return new_message

    def update_table(self):
        new_table = self.get_from_message_by_idx(0)
        for i in range(1,len(self.connected_nodes)):
            new_table = new_table.multiply(self.get_from_message_by_idx(i))

        nodes = new_table.nodes
        for node in nodes:
            if node == self:
                continue
            new_table = new_table.sum_out_var_by_var(node)
        self.table = new_table
        self.table.normalize()



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
            msg = self.get_from_message_by_var(connection)
            if msg is not None:
                new_message = new_message.multiply(msg)


        for connection in self.connected_nodes:
            if connection == target_node:
                continue
            new_message = new_message.sum_out_var_by_var(connection)
        new_message.normalize()
        return new_message