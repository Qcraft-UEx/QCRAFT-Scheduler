import matplotlib.pyplot as plt
import json
import math
from scipy.stats import wasserstein_distance

def hellinger(p, q):
    return math.sqrt(sum([ (math.sqrt(p_i) - math.sqrt(q_i))**2 for p_i, q_i in zip(p, q) ]) / 2)

def wasserstein(p, q):
    return wasserstein_distance(p, q)

def add_missing_keys(d1, d2):
    for key in d1.keys():
        if key not in d2:
            d2[key] = 0
    for key in d2.keys():
        if key not in d1:
            d1[key] = 0

    # Sort keys by name and return the sorted dictionaries
    d1 = dict(sorted(d1.items()))
    d2 = dict(sorted(d2.items()))
    return d1, d2

def dict_to_prob(d):
    total = sum(d.values())
    return [count / total for count in d.values()]


hellinger_results = []
composed = []
individual = []

with open('datasets/mutants-9280.json') as f:
    for line in f:
        elem = json.loads(line.strip())
        composed.append(elem)

with open('datasets/mutants9280-simulator.json') as f:
    for line in f:
        elem = json.loads(line.strip())
        individual.append(elem)

composed.sort(key=lambda x: x['circuit'])
individual.sort(key=lambda x: x['circuit'])

composed_results = [elem['value'] for elem in composed]
individual_values = [elem['value'] for elem in individual]

composed_circuits = [elem['circuit'] for elem in composed]
individual_circuits = [elem['circuit'] for elem in individual]


i = 0
for elem in composed:
    composed_elem = composed_results[i]
    individual_elem = individual_values[i]
    composed_elem_circuit = composed_circuits[i]
    individual_elem_circuit = individual_circuits[i]

    if composed_elem_circuit != individual_elem_circuit:
        print(f'Error: The circuits {composed_elem_circuit} and {individual_elem_circuit} do not match on position {i}')
        break
    
    composed_elem_1, individual_elem_1 = add_missing_keys(composed_elem, individual_elem)

    hellinger_data_1 = hellinger(dict_to_prob(composed_elem_1), dict_to_prob(individual_elem_1))
    hellinger_results.append(hellinger_data_1)

    i += 1

figsize = (25,8)
label_fontsize = 25
plt.figure(figsize=figsize)
plt.plot(hellinger_results)
plt.ylabel('Hellinger distance', fontsize=label_fontsize)
plt.xlabel('Mutant circuits of the second case of study',fontsize=label_fontsize)
plt.xlim(0,len(hellinger_results)-1)
plt.xticks(fontsize=label_fontsize)
plt.yticks(fontsize=label_fontsize)
plt.ylim(0,1)
plt.savefig('plot/mutants-9280/hellinger_results_1.png')

plt.figure(figsize=figsize)
plt.scatter(range(len(hellinger_results)), hellinger_results)
plt.ylabel('Hellinger distance',fontsize=label_fontsize)
plt.xlabel('Mutant circuits of the second case of study',fontsize=label_fontsize)
plt.savefig('plot/mutants-9280/hellinger_results_scatter_1.png')
