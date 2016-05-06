from string import upper

__author__ = 'Akshay'

from BayesNetBuilder import BayesNetBuilder
from LikelyhoodSampling import LikelyhoodSampling
from RejectionSampling import RejectionSampling
from PriorSampling import PriorSampling
from SamplingStrategy import SamplingStrategy
from EnumerationInference import EnumerationInference

import sys
#import numpy

def get_sampling_method(method, bayes_net, number_samples, query_vars, evidence_vars):
    if method == 'r':
        sampling_method = RejectionSampling(bayes_net, number_samples, evidence_vars, query_vars)
        #print "Rejection sampling"
    elif method == 'l':
        sampling_method = LikelyhoodSampling(bayes_net, number_samples, evidence_vars, query_vars)
        #print "Likelyhood sampling"
    elif method == 'p':
        sampling_method = PriorSampling(bayes_net, number_samples, evidence_vars, query_vars)
        #print "Prior sampling"
    else:
        sampling_method = EnumerationInference(bayes_net, evidence_vars, query_vars)

    return sampling_method


def input_format_method():
        line = raw_input()
        query_vars = []
        evidence_vars = []

        inpt = line.split()
        count = len(inpt)
        if count==2:
            try:
                n, m = map(int, inpt)
            except ValueError:
                print "Input an integer value"
                return query_vars , evidence_vars

            for _ in range(m+n):
              inp = raw_input()
              evidence_inpt = inp.split()
              evidence_count = len(evidence_inpt)
              if _ < n:
                  if evidence_count==2:
                      x, y = inp.split()
                      if x=='A' or x=='B' or x=='E' or x=='J' or x=='M':
                        if y=='t' or y == 'f':
                            evidence_vars.append((x, upper(y)))
                        else:
                            print "Enter truth value as either 'T' or 'F'"
                            break

                      else:
                          print "Insert node and value properly"
                          break

                  else:
                      print "Insert exactly 2 values"
                      break
              else:
                  query_inpt = inp.split()
                  query_count = len(query_inpt)
                  if query_count==1:
                      z = inp
                      if z=='A' or z=='B' or z=='E' or z=='J' or z=='M':
                        query_vars.append((z,'T'))

                      else:
                         print "Insert node and value properly"
                         break

                  else:
                      print "Insert exactly 1 values"
                      break

        else:
            print "Insert exactly 2 values"

        return query_vars , evidence_vars


def main():
    bayes_net_builder = BayesNetBuilder()
    bayes_net = bayes_net_builder.build_network()
    
    sampling_strategy = str(sys.argv[1])
    number_of_samples = int(sys.argv[2])

    query_vars, evidence_vars = input_format_method()
    result = []
    #print query_vars
    #print evidence_vars
    #query_vars = [('B', 'T'), ('J', 'T')]
    #evidence_vars = [('A', 'F')]

    if len(query_vars) != 0 and len(evidence_vars) != 0:

        for q in query_vars:
            for i in range(0, 10):
                sampling_algorithm = get_sampling_method(sampling_strategy,
                                                     bayes_net, number_of_samples, [q], evidence_vars)
                #sampling_algorithm = get_sampling_method(SamplingStrategy.RejectionSampling, bayes_net, 10, [q], evidence_vars)
                res = sampling_algorithm.perform_query()
                result.append(res)

            avg = sum(result)/len(result)
            print q[0], avg

if __name__ == "__main__":
    main()
