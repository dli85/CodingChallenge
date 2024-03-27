import unittest
from main import run
import logging


class TestDAGSearch(unittest.TestCase):

    # Checks if two result lists (of the DAG search) are equivalent.
    # timestamps/floats will not be exactly equivalent, so check if they are roughly equivalent to each other
    # Assumes each element in both lists are (string, number)
    # Assumes the two lists are not affected by race conditions.
    def compare_results(self, l1, l2):
        # if lengths are not the same, lists can't be equivalent
        self.assertEquals(len(l1), len(l2))

        # List lengths are equal, does not matter if we use l1 or l2
        for i in range(len(l1)):
            node1 = l1[i][0]
            time1 = l1[i][1]
            node2 = l2[i][0]
            time2 = l2[i][1]

            self.assertEquals(node1, node2)

            # Check that the difference between the times is less than x% of the smaller time
            self.assertLessEqual(abs(time1 - time2), 0.05 * (min(time1, time2)))

    # different compare function that assumes race conditions may affect the result
    # Doesn't care about the order of the lists, checks the timestamp of when each
    # node was printed.
    def compare_results_race_condition(self, l1, l2):
        dict1 = {}
        dict2 = {}

        l1nodes = set()
        l2nodes = set()

        for node, time in l1:
            l1nodes.add(node)
            dict1[node] = time

        for node, time in l2:
            l2nodes.add(node)
            dict2[node] = time

        # l1 and l2 should have the exact same nodes
        self.assertEquals(l1nodes, l2nodes)

        for node in l1nodes:
            time1 = dict1[node]
            time2 = dict2[node]

            # Check that the difference between the times is less than x% of the smaller time
            self.assertLessEqual(abs(time1 - time2), 0.05 * (min(time1, time2)))

    def testDAG1(self):
        path = 'DAGs/DAG1.json'
        expected_result = [('A', 0), ('B', 5), ('C', 7)]
        result = run(path, False)
        logging.debug(expected_result)
        self.compare_results(result, expected_result)

    def testDAG2(self):
        path = 'DAGs/DAG2.json'
        expected_result = [('A', 0)]
        result = run(path, False)
        self.compare_results(result, expected_result)

    def testDAG3(self):
        path = 'DAGs/DAG3.json'
        expected_result = [('A', 0), ('B', 1), ('D', 2), ('E', 3), ('C', 5)]
        result = run(path, False)
        self.compare_results(result, expected_result)

    def testDAG4(self):
        path = 'DAGs/DAG4.json'
        expected_result = [('A', 0), ('B', 1), ('C', 1)]
        result = run(path, False)
        self.compare_results_race_condition(result, expected_result)

    def testDAG5(self):
        path = 'DAGs/DAG5.json'
        expected_result = [('A', 0), ('B', 1), ('C', 1), ('D', 2), ('E', 2), ('F', 2), ('G', 2)]
        result = run(path, False)
        self.compare_results_race_condition(result, expected_result)

    def testDAG6(self):
        path = 'DAGs/DAG6.json'
        expected_result = [('A', 0), ('C', 0.4), ('D', 0.7), ('B', 0.8)]
        result = run(path, False)
        self.compare_results(result, expected_result)

    def testDAG7(self):
        path = 'DAGs/DAG7.json'
        expected_result = [('A', 0), ('C', 1), ('E', 2), ('G', 3), ('D', 4), ('F', 5), ('B', 6)]
        result = run(path, False)
        self.compare_results(result, expected_result)


if __name__ == '__main__':
    unittest.main()


