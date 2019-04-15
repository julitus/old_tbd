from heapq import heappush, heappop

def swap(a, b):
	return b, a

def parent(i):
	return (i - 1) / 2

def left(i):
	return 2 * i + 1

def right(i):
	return 2 * i + 2

def maxHeapify(A, i):
	l = left(i)
	r = right(i)
	largest = l if l < len(A) and A[l] > A[i] else i
	if r < len(A) and A[r] > A[largest]:
		largest = r
	if largest != i:
		A[i], A[largest] = swap(A[i], A[largest])
		maxHeapify(A, largest)

def buildMaxHeap(A):
	for i in range(len(A) / 2 - 1, -1, -1):
		maxHeapify(A, i)

def heapSort(A):
	buildMaxHeap(A)
	S = []
	for i in range(len(A) - 1, -1, -1):
		A[0], A[i] = swap(A[0], A[i])
		S.append(A[i])
		A = A[:i]
		maxHeapify(A, 0)
	return S


""" Ordena de manera ascendente """
def heapSortAsc(iterable):
	h = []
	for value in iterable:
		heappush(h, value)
	return [heappop(h) for i in range(len(h))]