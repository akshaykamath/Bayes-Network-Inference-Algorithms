from copy import deepcopy


class EnumerationInference:
    initial_evidence_vars = []
    query_vars = []
    bayes_net = []
    domain_values = ['T', 'F']

    def __init__(self, bayes_net, evidence_vars, query_vars):
        self.initial_evidence_vars = evidence_vars
        self.query_vars = query_vars
        self.bayes_net = bayes_net

    @staticmethod
    def is_node_in_evidence(node, evidence_var):
        if evidence_var.__contains__((node.name, 'T')) or evidence_var.__contains__((node.name, 'F')):
            return True
        else:
            return False

    @staticmethod
    def node_value_in_evidence(node, evidence_var):
        if evidence_var.__contains__((node.name, 'T')) or evidence_var.__contains__((node.name, 'F')):
            for evidence in evidence_var:
                if evidence[0] == node.name:
                    return evidence[1]

            return -1
        else:
            return -1

    def perform_query(self):
        result_vec = {'T': 1, 'F': 1}
        bayes_network = deepcopy(self.bayes_net)

        for q in self.query_vars:
            for value in self.domain_values:
                tup = (q[0], value)
                evidence = self.get_extended_evidence(self.initial_evidence_vars, tup)
                result_vec[value] *= self.enumerate_all(bayes_network, evidence)

        final_result = self.normalize(result_vec)
        return final_result['T']

    def enumerate_all(self, bayes_network, evidence_var):
        if len(bayes_network) < 1:
            return 1

        first_node = bayes_network[0]

        # Evidence or instantiated node, no need to sum out.
        if self.is_node_in_evidence(first_node, evidence_var):
            val = self.get_probability(first_node, self.node_value_in_evidence(first_node, evidence_var), evidence_var)
            probability = val * self.enumerate_all(bayes_network[1:len(bayes_network)], evidence_var)
            return probability

        probability = 0.0

        # Instantiate non-evidence nodes to a value and sum them out.
        for truth_value in self.domain_values:
            tup = (first_node.name, truth_value)
            extended_evidence = self.get_extended_evidence(evidence_var, tup)
            probability += self.get_probability(first_node, truth_value, extended_evidence) * \
                           self.enumerate_all(bayes_network[1:len(bayes_network)], extended_evidence)

        return probability

    @staticmethod
    def get_extended_evidence(evidence, tup):
        evidence = deepcopy(evidence)
        evidence.append(tup)
        return evidence

    def get_probability(self, node, truth_value, evidence):
        parent_values = []
        for parent in node.parent_nodes:
            parent_values.append(self.node_value_in_evidence(parent, evidence))

        if len(parent_values) == 0:
            parent_tup = ('T')
        elif len(parent_values) == 1:
            parent_tup = (parent_values[0])
        else:
            parent_tup = tuple(parent_values)

        probability = node.conditional_probability_table[parent_tup]

        if truth_value == 'F':
            return 1 - probability

        return probability

    @staticmethod
    def normalize(result_vec):
        denominator = result_vec['T'] + result_vec['F']

        result_vec['T'] /= denominator
        result_vec['F'] /= denominator

        return result_vec