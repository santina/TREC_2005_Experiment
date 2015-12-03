import numpy as np
import timeit
import heapq
import argparse 


def readMatrix(filename, nrow, numSV): 
	''' Read in decomposed matrices U or V 	
	'''
	matrixU = np.zeros((nrow, numSV)) 

	with open(filename, "rb") as f:
		for line in f: 
			line = line.split()
			# x[0] is index and the rest are values
			matrixU[int(line[0])] = [float(num) for num in line[1:numSV+1]] 
	return matrixU

def getSVals(filename, numSV, header=True):
	''' Read in a given number of singular values 
	'''
	singularVals = []

	with open(filename) as f:
		for index, line in enumerate(f): # 0 base for lineNum 
			if header and index == 0: 
				continue 
			elif index > numSV: # If has recorded the desired number of values
				break
			else: 
				singularVals.append(float(line))
	return singularVals

def scaleMatrix(matrix, singularVals):
	''' Scale the matrix by square root such m_ij = sqrt(s_j)*m_ij
	for later's distance calculation to be sum(s_0*(a_0-b_0)^2 + s_1*(a_1-b_1)^2,...) 
	''' 
	matrix = np.multiply(matrix, np.sqrt(singularVals))
	return matrix

def normalizeMatrix(matrix, ncols=None):
	''' Calculate normalization of a part of `matrix`. Store
	and return that as a new matrix 
	'''
	rowNum = 0
	if not ncols: # default to normalize the whole matrix
		ncols = matrix.shape[1] 
	newMatrix = np.zeros((matrix.shape[0], ncols))
	
	for row in matrix:
		norm = np.linalg.norm(row[:ncols])
		# if norm is not 0, i.e. the row isn't all zeros
		if norm: 
			newMatrix[rowNum] = [number/norm for number in row[:ncols]]
		rowNum += 1

	return newMatrix

def getMatrixSubset(matrix, ncols):
	''' Return a subset of the matrix (first `ncols`)
	'''
	newMatrix = np.zeros((matrix.shape[0], ncols))
	index = 0
	for row in matrix:
		newMatrix[index] = row[:ncols]
		index += 1
	return newMatrix 

def getCosineDistance(vectorA, vectorB):
	''' Calculate and return cosine distance of two **normalized** vectors 
	'''
	return np.dot(vectorA, vectorB)

def getEuclidenDistance(vectorA, vectorB):
	''' Calculate and return Euclidean distance of two vectors: 
	'''
	score = 0
	for i in range(0, len(vectorA)):
		score += (vectorA[i] - vectorB[i])**2 

	return score**0.5 # take the square root 

def findClosestRowsByCosine(matrix, rowNum, nNeighbors):
	''' Calculate cosine distance of the given row to all other rows in the matrix
	Use a heap invariant to maintain the top `nNeighbors` greatest cosine distances 
	'''
	heap = []  # a heapified array of tuple (distance, row_number)
	index = 0
	for row in matrix:
		dist = getCosineDistance(matrix[rowNum], row)
		
		# If we haven't found nNeighbors of closestRows 
		# or 'dist' is greater than the smallest recorded distance in `heap`
		# then we need to add `dist` to `heap` 

		if len(heap) < nNeighbors or dist > heap[0][0]:
			
			# If the heap is full,remove the smallest
			if len(heap) == nNeighbors:
				heapq.heappop(heap)

			heapq.heappush(heap, (dist, index))

		index += 1

	return heapq.nlargest(nNeighbors, heap) # return top largest distances in sorted order 


def findClosestRowsByEuclidean(matrix, rowNum, nNeighbors):
	''' Calculate Euclidean distance of the given row to all other rows in the matrix
	Use a heap invariant to maintain the order and return top `nNeighbors` smallest distances 
	'''
	heap = []  # a heapified array of tuple (distance, row_number)
	index = 0
	for row in matrix:
		dist = getEuclidenDistance(matrix[rowNum], row)
		
		heapq.heappush(heap, (dist, index))

		index += 1

	return heapq.nsmallest(nNeighbors, heap)

def writeToFile(result, out):
	''' Delimited by a space for each document ID 
	'''
	docIDs = []
	for tuple in result:
		docIDs.append(tuple[1])
	out.write(' '.join([str(i) for i in docIDs])+'\n')

def writeCosineResults(matrix, outfile):
	''' Go through the entire matrix and find closest rows to each row 
	by Cosine distance and write the result to `outfile`
	'''
	with open(outfile, 'w') as out:
		for i in range(0, matrix.shape[0]):
			result = findClosestRowsByCosine(matrix, i, 100)
			writeToFile(result, out)

def writeEuclideanResults(matrix, outfile):
	''' Go through the entire matrix and find closest rows to each row 
	by Euclidean distance and write the result to `outfile` 
	'''
	with open(outfile, 'w') as out:
		for i in range(0, matrix.shape[0]):
			result = findClosestRowsByEuclidean(matrix, i, 100)
			writeToFile(result, out)

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Find closest papers using decomposed matrix and singular values')
	parser.add_argument('--matrix', type=str, help='Path to the matrix file')
	parser.add_argument('--s', type=str, help='Path to the singular values file')
	parser.add_argument('--nsv', type=int, default=1000, help='Number of maximum singular values')
	parser.add_argument('--nrow', type=int, default=1516, help='Number of rows in the matrix')
	parser.add_argument('--out', type=str, help='Path to the folder to write the results to')
	args = parser.parse_args()

	matrix = readMatrix(args.matrix, args.nrow, args.nsv)
	svals = getSVals(args.s, args.nsv)
	matrix = scaleMatrix(matrix, svals)
	outputFile = args.out + '/{0}_{1}.neighbors'

	# try each different nsv, differ by 50 in each step 
	for nsv in range(50, args.nsv+1, 50): 
		
		t = timeit.default_timer()
		outfile = outputFile.format('euclidean', str(nsv))
		newM = getMatrixSubset(matrix, nsv)
		print "Time took to subset the matrix " + str(nsv) + ": " + str(timeit.default_timer() - t)
		t = timeit.default_timer()
		writeEuclideanResults(newM, outfile)
		print "Time took to use Euclidean on " + str(nsv) + ": " + str(timeit.default_timer() - t)

		t = timeit.default_timer()
		outfile = outputFile.format('cosine', str(nsv))
		newM = normalizeMatrix(matrix, nsv)
		writeCosineResults(newM, outfile)
		print "Time took to use cosine on " + str(nsv) + ": " + str(timeit.default_timer() - t)







