import random

from Node import Node


class RejectionSampling:
    number_samples = 0
    rejection_samples = {}
    evidence_vars = []
    query_vars = []
    bayes_net = []

    def __init__(self, bayes_net, number_samples, evidence_vars, query_vars):
        self.number_samples = number_samples
        self.evidence_vars = evidence_vars
        self.query_vars = query_vars
        self.bayes_net = bayes_net
        self.rejection_sample()

    def rejection_sample(self):
        # Initialise the random samples first
        # Get 10 prior samples
        i = 0

        while True:
            self.rejection_samples[i] = {}

            reject_sample = False
            # Assumption is that the the nodes are topologically ordered,
            # Additional Note: When this program is catered to work for any bayes network,
            # a topological sort may be required.
            # Based on the random numbers
            for node in self.bayes_net:
                # print node.name
                random_number = random.uniform(0, 1)
                self.rejection_samples[i] = self.get_rejection_sample(random_number, node, self.rejection_samples[i])

                # If this node is present in the evidence and
                # the value in rejection sample is not same as evidence, reject!
                if self.needs_reject(node, self.rejection_samples[i][node.name]):
                    reject_sample = True
                    break

            if reject_sample:
                continue


                # Get the next sample
            #print self.rejection_samples[i]
            i += 1

            if i == self.number_samples:
                return

    def needs_reject(self, node, sampled_value):
        if self.evidence_vars.__contains__((node.name, 'T')) or self.evidence_vars.__contains__((node.name, 'F')):
            for evidence in self.evidence_vars:
                if evidence[0] == node.name and evidence[1] != sampled_value:
                    return True

            return False
        else:
            return False

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

    def get_rejection_sample(self, random_value, node, sample):
        assert isinstance(node, Node)
        parent_values = []
        try:
            parent_tup = self.get_parent_tup_from_sample(node, sample)
            probability = node.conditional_probability_table[parent_tup]

            if random_value >= probability:
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
            if self.rejection_samples.__len__() == 0:
                print "No samples generated yet."
                return 0.0

            sample = self.rejection_samples[1]

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
            for sample in self.rejection_samples.values():
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
                denominator = self.rejection_samples.__len__()

            probability = numerator / denominator
            return probability
        except Exception as ex:
            return 0.0

        return 0.0