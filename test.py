import unittest
from main import run
import logging

times = 15


class TestDAGSearch(unittest.TestCase):

    # Checks if two result lists (of the DAG search) are equivalent.
    # timestamps/floats will not be exactly equivalent, so check if they are roughly equivalent to each other
    # Assumes each element in both lists are (string, number)
    # Checks for race conditions.
    def compare_results(self, l1, l2):
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
            # self.assertLessEqual(abs(time1 - time2), 0.05 * (min(time1, time2)))
            self.assertLessEqual(abs(time1 - time2), 0.05)

    # Basic DAG from problem description
    def testDAG1(self):
        for _ in range(times):
            path = 'DAGs/DAG1.json'
            expected_result = [('A', 0), ('B', 5), ('C', 7)]
            result = run(path, False)
            logging.debug(expected_result)
            self.compare_results(result, expected_result)

    # DAG with 1 node
    def testDAG2(self):
        for _ in range(times):
            path = 'DAGs/DAG2.json'
            expected_result = [('A', 0)]
            result = run(path, False)
            self.compare_results(result, expected_result)

    # DAG with 2 levels of children
    def testDAG3(self):
        for _ in range(times):
            path = 'DAGs/DAG3.json'
            expected_result = [('A', 0), ('B', 1), ('D', 2), ('E', 3), ('C', 5)]
            result = run(path, False)
            self.compare_results(result, expected_result)

    # DAG with simultaneous finishing/race conditions
    def testDAG4(self):
        for _ in range(times):
            path = 'DAGs/DAG4.json'
            expected_result = [('A', 0), ('B', 1), ('C', 1)]
            result = run(path, False)
            self.compare_results(result, expected_result)

    # Even more race conditions
    def testDAG5(self):
        for _ in range(times):
            path = 'DAGs/DAG5.json'
            expected_result = [('A', 0), ('B', 1), ('C', 1), ('D', 2), ('E', 2), ('F', 2), ('G', 2)]
            result = run(path, False)
            self.compare_results(result, expected_result)

    # Fractional edge weights
    def testDAG6(self):
        for _ in range(times):
            path = 'DAGs/DAG6.json'
            expected_result = [('A', 0), ('C', 0.4), ('D', 0.7), ('B', 0.8)]
            result = run(path, False)
            self.compare_results(result, expected_result)

    # DAG with more than 2 children
    def testDAG7(self):
        for _ in range(times):
            path = 'DAGs/DAG7.json'
            expected_result = [('A', 0), ('C', 1), ('E', 2), ('G', 3), ('D', 4), ('F', 5), ('B', 6)]
            result = run(path, False)
            self.compare_results(result, expected_result)

    # DAG with multiple paths leading to an edge
    def testDAG8(self):
        for _ in range(times):
            path = 'DAGs/DAG8.json'
            expected_result = [('A', 0), ('B', 1), ('D', 1), ('C', 3)]
            result = run(path, False)
            self.compare_results(result, expected_result)

    # Even more paths!!
    def testDAG9(self):
        for _ in range(times):
            path = 'DAGs/DAG9.json'
            expected_result = [('A', 0), ('C', 1), ('D', 3), ('B', 4), ('F', 4), ('E', 5)]
            result = run(path, False)
            self.compare_results(result, expected_result)


if __name__ == '__main__':
    unittest.main()



