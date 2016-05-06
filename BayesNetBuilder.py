__author__ = 'Akshay'

from Node import Node


class BayesNetBuilder:
    def __init__(self):
        pass

    # Currently this network is hardcoded
    # The build network method may be changed later to read any network from a file.
    @staticmethod
    def build_network():
        burglary = Node("B")
        earthquake = Node("E")
        alarm = Node("A")
        john = Node("J")
        mary = Node("M")

        burglary.add_child(alarm)
        earthquake.add_child(alarm)
        alarm.add_child(john)
        alarm.add_child(mary)

        cpt_burglary = {'T': 0.001}
        cpt_earthquake = {'T': 0.002}
        cpt_alarm = {('T', 'T'): 0.95, ('T', 'F'): 0.94, ('F', 'T'): 0.29, ('F', 'F'): 0.0010}
        cpt_john_calls = {'T': 0.90, 'F': 0.05}
        cpt_mary_calls = {'T': 0.70, 'F': 0.01}

        burglary.conditional_probability_table = cpt_burglary
        earthquake.conditional_probability_table = cpt_earthquake
        alarm.conditional_probability_table = cpt_alarm
        john.conditional_probability_table = cpt_john_calls
        mary.conditional_probability_table = cpt_mary_calls

        bayes_net_order = [burglary, earthquake, alarm, john, mary]

        return bayes_net_order