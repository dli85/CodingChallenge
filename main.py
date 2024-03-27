import json
import time
import threading

JSON_PATH = 'DAGs/DAG3.json'

'''
Adjacent matrix structure:

{
  edge1: {child1: time1, child2: time2, ...}
  edge2: {child3: time3, child4: time4, ...}
  ...
}
'''


# Searches a DAG (represented as adjacency matrix) and uses the timer.
def search_dag(start_node, adj_mat, base_time, wait_time, results, verbose):
    time.sleep(wait_time)
    if verbose:
        print(start_node, time.time() - base_time)
    results.append((start_node, time.time() - base_time))

    threads = []

    for child in adj_mat[start_node]:
        # Create new thread for the child, so it can start its timer in parallel with other children
        t = threading.Thread(target=search_dag, args=(child, adj_mat, base_time, adj_mat[start_node][child], results, verbose))

        threads.append(t)

        t.start()

        # Blocks the main thread until this/all children threads are finished, also handles resource cleanup
        # t.join()

    for thread in threads:
        thread.join()


# Parses a json loads the data into an adjacency matrix.
def parse_json(path):
    start = None

    with open(path, 'r') as file:
        data = json.load(file)

    adj_mat = {}
    for node in data:
        node_data = data[node]
        if "start" in node_data:
            start = node

        children = node_data['edges']

        adj_mat[node] = children.copy()

    # Throw an error if no start node was found
    if start is None:
        raise Exception("No starting node specified")

    return adj_mat, start


# Searches a DAG from a json file, returns the result as a list
# Verbose determines if outputs should be printed
def run(path, verbose=True):
    adj_mat, starting_node = parse_json(path)
    results = []
    search_dag(starting_node, adj_mat, time.time(), 0, results, verbose)

    if verbose:
        print(results)

    return results


if __name__ == '__main__':
    _ = run(JSON_PATH)
