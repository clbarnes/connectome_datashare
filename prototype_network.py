import networkx as nx
import csv
from collections import defaultdict
from itertools import product
import unittest
from abc import abstractclassmethod
import pytest


DB_DUMP_PATH = 'combined.csv'
MONOAMINES = {'Dopamine', 'Serotonin', 'Tyramine', 'Octopamine'}


# dummy
class Neuron:
    def __init__(self, receptors=None, neuropeptides=None, neurotransmitters=None):
        self.receptors = receptors if receptors is not None else set()
        self.neuropeptides = neuropeptides if neuropeptides is not None else set()
        self.neurotransmitters = neurotransmitters if neurotransmitters is not None else set()


# dummy
class Evidence:
    def __init__(self, name, url):
        self.name = name
        self.url = url


# dummy
class Data:
    def __init__(self):
        self.neurons, self.ligand_mappings, self.evidence = self.setup()

    @staticmethod
    def setup():
        neurons = defaultdict(Neuron)
        ligand_mappings = defaultdict(set)
        evidence = dict()

        with open('combined.csv') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row[1] == 'Receptor':
                    neurons[row[0]].receptors.add(row[2])
                elif row[1] == 'Neurotransmitter':
                    neurons[row[0]].neurotransmitters.add(row[2])
                elif row[1] == 'Neuropeptide':
                    neurons[row[0]].neuropeptides.add(row[2])
                elif row[1] == 'Ligand':
                    ligand_mappings[row[0]].add(row[2])

                evidence[(row[0], row[2])] = Evidence(row[3], row[4])

        return neurons, ligand_mappings, evidence


DATA = Data()


def make_extrasyn_net(attr_name, data=DATA):
    """

    :param attr_name: 'neurotransmitters' if building MA net, 'neuropeptides' if building NP net
    :return: nx.MultiDiGraph
    """
    net = nx.MultiDiGraph()
    net.add_nodes_from(data.neurons)

    for (src_name, src_inst), (tgt_name, tgt_inst) in product(data.neurons.items(), repeat=2):
        for transmitter in getattr(src_inst, attr_name):  # todo: prevent it catching ACh etc. in production
            for receptor in tgt_inst.receptors & data.ligand_mappings[transmitter]:
                net.add_edge(src_name, tgt_name, transmitter=transmitter, receptor=receptor, evidence={
                    'expresses_transmitter': data.evidence[(src_name, transmitter)],
                    'expresses_receptor': data.evidence[(tgt_name, receptor)],
                    'ligand': data.evidence[(transmitter, receptor)]
                })

    return net


class ExtrasynNetTest:
    @abstractclassmethod
    def setUpClass(cls):
        cls.net = None

    @unittest.skip('Source table does not include all 302 nodes')
    def test_node_count(self):
        """
        Check that there are 302 neurons in the network
        """
        assert self.net.nodes() == 302

    def test_has_edges(self):
        """
        Check that there are edges.
        """
        assert self.net.edges()


class MANetTest(unittest.TestCase, ExtrasynNetTest):
    @classmethod
    def setUpClass(cls):
        cls.net = make_extrasyn_net('neurotransmitters')


class NPNetTest(unittest.TestCase, ExtrasynNetTest):
    @classmethod
    def setUpClass(cls):
        cls.net = make_extrasyn_net('neuropeptides')


if __name__ == '__main__':
    pytest.main()
