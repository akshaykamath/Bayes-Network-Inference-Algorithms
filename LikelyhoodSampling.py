import random

from Node import Node


class LikelyhoodSampling:
    number_samples = 0
    likelyhood_samples = {}
    evidence_vars = []
    query_vars = []
    sample_weights = [1] * 20000
    bayes_net = []

    def __init__(self, bayes_net, number_samples, evidence_vars, query_vars):
        self.number_samples = number_samples
        self.evidence_vars = evidence_vars
        self.query_vars = query_vars
        self.bayes_net = bayes_net
        self.likelyhood_sample()

    def likelyhood_sample(self):
        i = 0

        while True:
            self.likelyhood_samples[i] = {}
            self.sample_weights[i] = 1
            # Assumption is that the the nodes are topologically ordered,
            # Additional Note: When this program is catered to work for any bayes network,
            # a topological sort may be required.
            # Based on the random numbers
            for node in self.bayes_net:
                random_number = random.uniform(0, 1)

                self.likelyhood_samples[i], sample_weight = self.get_likelyhood_samples(random_number, node,
                                                                                        self.likelyhood_samples[i])
                self.sample_weights[i] *= sample_weight

            # print self.likelyhood_samples[i], self.sample_weights[i]


            i += 1

            if i == self.number_samples - 1:
                return

    def is_node_in_evidence(self, node):
        if self.evidence_vars.__contains__((node.name, 'T')) or self.evidence_vars.__contains__((node.name, 'F')):
            return True
        else:
            return False

    def node_value_in_evidence(self, node):
        if self.evidence_vars.__contains__((node.name, 'T')) or self.evidence_vars.__contains__((node.name, 'F')):
            for evidence in self.evidence_vars:
                if evidence[0] == node.name:
                    return evidence[1]

            return -1
        else:
            return -1

    def get_parent_tup_from_sample(self, node, sample):
        parent_values = []
        parent_tup = ()
        # If there are no values, this node has no parents in the network
        if node.parent_nodes.__len__() == 0:
            parent_tup = ('T')
        elif node.parent_nodes.__len__() == 1:
            parent_tup = (sample[node.parent_nodes[0].name])
        else:
            for parent_node in node.parent_nodes:
                parent_sample_value = sample[parent_node.name]
                parent_values.extend(parent_sample_value)

            parent_tup = tuple(parent_values)

        return parent_tup

    def get_likelyhood_samples(self, random_value, node, sample):
        assert isinstance(node, Node)

        try:
            parent_tup = self.get_parent_tup_from_sample(node, sample)
            probability = node.conditional_probability_table[parent_tup]

            # Node is an evidence variable. Fix the sample value as per the evidence
            # and return the sample and the weight of the evidence.
            if self.is_node_in_evidence(node):
                sample[node.name] = self.node_value_in_evidence(node)
                if sample[node.name] == 'F':
                    probability = 1 - probability

                return sample, probability

            if random_value >= probability:
                sample[node.name] = 'F'
            else:
                sample[node.name] = 'T'

        except Exception as inst:
            print sample
            print inst

        return sample, 1

    def perform_query(self):
        try:
            # Sanity check - verify that samples are generated.
            if self.likelyhood_samples.__len__() == 0:
                print "No samples generated yet."
                return 0.0

            sample = self.likelyhood_samples[1]

            # Sanity check - check if the query variables are present in our samples.
            for q in self.query_vars:
                # the first value of the tuple contains the query variable name,
                # second parameter of the tuple contains the T/F value.
                if q[0].upper() not in sample:
                    print "Invalid query parameter."
                    return 0.0

            # Sanity check - check if the evidence variables are present in our samples.
            for e in self.evidence_vars:
                if e[0].upper() not in sample:
                    print "Invalid evidence parameter."
                    return 0.0

            denominator = 0.0
            numerator = 0.0
            ncnt = 0
            # count the numerator and denominator
            # for sample in likely-hood samples.values():

            for i in range(0, self.likelyhood_samples.__len__()):
                sample = self.likelyhood_samples[i]

                sample_weight = self.sample_weights[i]
                is_numerator_acceptable = True

                for q in self.query_vars:
                    if sample[q[0]] != q[1]:
                        is_numerator_acceptable = False
                        break
                if is_numerator_acceptable:
                    numerator += sample_weight
                    ncnt +=1

                denominator += sample_weight

            probability = numerator / denominator

            #aprint 'num', numerator
            #aprint 'den', denominator

            #aprint 'total', self.likelyhood_samples.__len__()
            #aprint 'num_tot', ncnt
            #aprint 'w', self.sample_weights[1]
            return probability
        except Exception as ex:
            return 0.0