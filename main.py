import json
import time
import threading

JSON_PATH = 'DAGs/DAG9.json'

# https://csacademy.com/app/graph_editor/

'''
Adjacent matrix structure:

{
  edge1: {child1: time1, child2: time2, ...}
  edge2: {child3: time3, child4: time4, ...}
  ...
}
'''

lock = threading.Lock()


# Searches a DAG (represented as adjacency matrix) and uses the timer.
# Verbose determines if outputs should be printed (False for testing)
def search_dag(start_node, adj_mat, base_time, wait_time, results, seen, verbose=True):
    time.sleep(wait_time)

    # Lock the shared resources before reading/writing
    lock.acquire()
    try:
        # Check that we haven't visited this node before
        if start_node in seen:
            return

        seen.add(start_node)

        if verbose:
            print(start_node, time.time() - base_time)
        results.append((start_node, time.time() - base_time))
    finally:
        lock.release()

    threads = []

    for child in adj_mat[start_node]:
        # Create new thread for the child, so it can start its timer in parallel with other children
        t = threading.Thread(target=search_dag,
                             args=(child, adj_mat,base_time, adj_mat[start_node][child], results, seen, verbose))

        threads.append(t)

        t.start()

    # thread.join blocks the main thread until other threads are finished, also handles resource cleanup for threads
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


# main function for the algorithm:
# Searches a DAG from a json file, returns the result of the search as a list
# Verbose determines if outputs should be printed
def run(path, verbose=True):
    adj_mat, starting_node = parse_json(path)
    results = []
    search_dag(starting_node, adj_mat, time.time(), 0, results, set(), verbose)

    if verbose:
        print(results)

    return results


if __name__ == '__main__':
    # return value is only used for testing
    _ = run(JSON_PATH)
