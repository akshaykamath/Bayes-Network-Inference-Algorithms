import random
from BayesNetBuilder import BayesNetBuilder
from Node import Node


class PriorSampling:
    number_samples = 0
    evidence_vars = []
    query_vars = []
    bayes_net = []
    prior_samples = {}

    def __init__(self, bayes_net, number_samples, evidence_vars, query_vars):
        self.number_samples = number_samples
        self.evidence_vars = evidence_vars
        self.query_vars = query_vars
        self.bayes_net = bayes_net
        self.prior_sample()

    def prior_sample(self):
        # Initialise the random samples first
        # Get 10 prior samples
        for i in range(1, self.number_samples):
            self.prior_samples[i] = {}

            # Assumption is that the the nodes are topologically ordered,
            # Additional Note: When this program is catered to work for any bayes network,
            # a topological sort may be required.
            # Based on the random numbers
            for node in self.bayes_net:
                # print node.name
                random_number = random.uniform(0, 1)
                self.prior_samples[i] = self.get_prior_sample(random_number, node, self.prior_samples[i])

            #print self.prior_samples[i]

    def get_prior_sample(self, random_value, node, sample):
        assert isinstance(node, Node)
        parent_values = []
        try:
            # If there are no values, this node has no parents in the network
            parent_tup = ()
            if node.parent_nodes.__len__() == 0:
                parent_tup = ('T')
            elif node.parent_nodes.__len__() == 1:
                parent_tup = (sample[node.parent_nodes[0].name])
            else:
                for parent_node in node.parent_nodes:
                    parent_sample_value = sample[parent_node.name]
                    parent_values.extend(parent_sample_value)

                parent_tup = tuple(parent_values)

            probability = node.conditional_probability_table[parent_tup]

            if random_value > probability:
                sample[node.name] = 'F'
            else:
                sample[node.name] = 'T'
        except Exception as inst:
            print sample
            print inst

        return sample

    def perform_query(self):
        try:
            # Sanity checks - verify that samples are generated.
            if self.prior_samples.__len__() == 0:
                print "No samples generated yet."
                return 0.0

            sample = self.prior_samples[1]

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

            if self.evidence_vars.__len__() > 0:
                self.query_vars.extend(self.evidence_vars)

            # count the numerator and denominator
            for sample in self.prior_samples.values():
                is_numerator_acceptable = True
                is_denominator_acceptable = True

                for q in self.query_vars:
                    if sample[q[0]] != q[1]:
                        is_numerator_acceptable = False
                        break
                if is_numerator_acceptable:
                    numerator += 1

                for e in self.evidence_vars:
                    if sample[e[0]] != e[1]:
                        is_denominator_acceptable = False
                        break

                if is_denominator_acceptable:
                    denominator += 1

            if self.evidence_vars.__len__() < 1:
                denominator = self.prior_samples.__len__()

            probability = numerator / denominator
            return probability
        except Exception as ex:
            return 0.0