import sys
import heapq

from collections import defaultdict


def construct(file_path):
    vertices = defaultdict(list)

    with open(file_path) as file:
        first = file.readline().split()
        v = int(first[0])
        e = int(first[1])

        for line in file:
            item = line.split()
            vertices[int(item[1])].append((int(item[0]), int(item[2])))

    return (v, vertices)


def dijkstra_search(edge, vertices, distances, heap):
    tail = edge[1]

    for head, weight in vertices[tail]:
        if distances[head] > distances[tail] + weight:
            distances[head] = distances[tail] + weight

            if (weight, head) in heap:
                heap.remove((weight, head))
                heapq.heapify(heap)

            heapq.heappush(heap, (distances[head], head))


def dijkstra(source, v, vertices):
    distances = {}

    for i in xrange(1, v + 1):
        distances[i] = sys.maxint
    distances[source] = 0

    heap = []
    heapq.heappush(heap, (0, source))

    while len(heap) != 0:
        dijkstra_search(heapq.heappop(heap), vertices, distances, heap)

    return distances


def johnson(v, vertices, weights):
    v_weighted = defaultdict(list)

    for tail in vertices:
        for heads in vertices[tail]:
            v_weighted[tail].append((heads[0], heads[1] - weights[tail - 1] + weights[heads[0] - 1]))

    shortest = []

    for i in xrange(1, v + 1):
        distances = dijkstra(i, v, v_weighted)
        for j in xrange(1, v + 1):
            if i != j:
                shortest.append((distances[j] + weights[i - 1] - weights[j - 1], (j, i)))

    return shortest


def bellman_ford(source, v, vertices):
    A = [[0 for _ in xrange(v)] for _ in xrange(v + 1)]

    for i in xrange(v):
        if i != source - 1:
            A[0][i] = sys.maxint

    for i in xrange(1, v + 1):
        for vertex in xrange(1, v + 1):
            if vertex in vertices:
                tails            = vertices[vertex]
                min_previous     = min([(A[i - 1][tail[0] - 1] + tail[1]) for tail in tails])
                A[i][vertex - 1] = min(A[i - 1][vertex - 1], min_previous)

    for i in xrange(v):
        if A[v - 1][i] != A[v][i]:
            return None

    return A


def main(argv):
    v, vertices = construct(argv[0])

    g_prime = defaultdict(list)

    for tail in vertices:
        g_prime[tail].extend(vertices[tail])
        g_prime[tail].append((0, 0))

    A = bellman_ford(0, v + 1, g_prime)

    if A == None:
        print
        print 'Negative Weight Cycle Detected!'
        print
    else:
        d, p = min(johnson(v, vertices, A[v]))
        print
        print 'Shortest Path [%s, %s] = %s' % (p[0], p[1], d)
        print


if __name__ == "__main__":
    main(sys.argv[1:])
