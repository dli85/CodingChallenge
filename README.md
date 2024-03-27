# DAG Coding Challenge

## Implementation overview

This project implements an algorithm to search a Directed Acyclic Graph (DAG) and process edges in parallel. Every edge
in the DAG has weight which represents how long the "runner" should wait before traveling to the
corresponding node. The algorithm starts at a specified node, then traverses the DAG by following the edges. The algorithm uses
threads in order to process edges in parallel. When the algorithm
reaches a node, it will print the node along with the time it took to reach that node.

The complete algorithm is implemented in main.py. backtrack.py implements the same algorithm
with slightly modified output that also displays which node every node was reached from.

## Behavior

If two nodes are reached at the same time, either node may be printed first, but nevertheless, the times for both nodes will be accurate.

The algorithm will not repeat/reprint nodes. Every node will only be printed once at the earliest time
which it can be reached.

## Usage

The main.py function performs the DAG search on a singular JSON file. The file 
is specified at the top by changing the JSON_PATH parameter. The search prints the nodes
that it reaches in the console in realtime.

Similarly, the backtrack.py file also performs a DAG search on a singular JSON file
which is also specified at the top by changing JSON_PATH parameter. In addition to doing the search,
the backtrack.py file also prints which nodes every node was reached from.

The test.py file runs all the test cases.

## Testing

In order to test the correctness of the algorithm, it will return a list in addition to
printing each node when it is reached. The list serves as a way to store the output. Every item
in the list is a tuple, (string, name), where the first element in the tuple is the Node name
and the second element is the time it took to reach (from when the program started).

The test.py file checks correctness by comparing the output with an expected output. This is done by 
first checking that the output contains the same number of nodes as the expected output, and that the
timestamps for every node in the output is "close enough" to corresponding time stamps in the expected output (times are floats).

Due to possible inconsistencies regarding threading, the test.py file allows you to specify
how many times every test should be run.

## Parallelism vs Concurrency
