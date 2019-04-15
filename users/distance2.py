import sys
import math
import heapSort

def getRatingsTwo(file):
	names = dict()
	infile = open(file, 'r')
	properties = [i for i in infile.readline().strip('\n').split(',')]
	for line in infile:
		row = [i for i in line.strip('\n').split(',')]
		names[row[0]] = [float(i) for i in row[1:]]
	return names, properties[1:]

def getRatingsOne(file):
	names = dict()
	for line in open(file, 'r'):
		row = [i for i in line.split(',')]
		names[row[0]] = [float(i) for i in row[1:]]
	return names

def distanceType(x, y, r):
	s = sum([(pow(abs(e[0] - e[1]), r) if (e[0] and e[1]) else 0) for e in zip(x, y)])
	return pow(s, 1 / float(r))

def cosenoSimilarity(x, y):
	sXY, mX, mY = 0, 0, 0
	for i in range(0, len(x)):
		sXY += x[i] * y[i]
		mX, mY = mX + pow(x[i], 2), mY + pow(y[i], 2)
	return sXY / (math.sqrt(mX) * math.sqrt(mY))

def pearsonCorrelation(x, y):
	sX, sY, sX2, sY2, sXY = 0, 0, 0, 0, 0
	#n = len(x)
	n = 0
	for i in range(0, len(x)):
		if x[i] != 0 and y[i] != 0:
			sX, sY = sX + x[i], sY + y[i]
			sX2, sY2 = sX2 + pow(x[i], 2), sY2 + pow(y[i], 2)
			sXY += x[i] * y[i]	
			n += 1
	#print n
	den = (math.sqrt(n * sX2 - pow(sX, 2)) * math.sqrt(n * sY2 - pow(sY, 2)))
	return (n * sXY - sX * sY) / den if den != 0 else 0
	#return (sXY - (sX * sY) / n) / (math.sqrt(sX2 - (pow(sX, 2) / n)) * math.sqrt(sY2 - (pow(sY, 2) / n)))

def funcDistance(x, y, dis):
	if dis == 1 or dis == 2:
		return distanceType(x, y, dis)
	elif dis == 3:
		return cosenoSimilarity(x, y)
	elif dis == 4:
		return pearsonCorrelation(x, y)
	return 0

def knnDistance(ratings, name, k, dis):
	knn = []
	for key, val in ratings.items():
		if key != name:
			#print key + ": " + `funcDistance(ratings[name], val, int(dis))`
			knn.append((funcDistance(ratings[name], val, dis), key))
	if dis == 4 or dis == 3: 
		knn = heapSort.heapSort(knn)[:k]
	else:
		knn = heapSort.heapSortAsc(knn)[:k]
	#knn2 = [(funcDistance(ratings[name], ratings[e[1]], 4), e[1]) for e in knn]
	knn2 = knn
	sR = sum([e[0] for e in knn2])
	return [(e[0], e[0] / sR, e[1]) for e in knn2]

def knnDistanceRadio(ratings, name, radio, dis):
	knn = []
	knn2 = []
	for key, val in ratings.items():
		if key != name:
			knn.append((funcDistance(ratings[name], val, dis), key))
	if dis == 4 or dis == 3: 
		knn = heapSort.heapSort(knn)
		for e in knn:
			if e[0] > radio:
				knn2.append(e)
			else:
				break
	else:
		knn = heapSort.heapSortAsc(knn)
		for e in knn:
			if e[0] < radio:
				knn2.append(e)
			else:
				break
	sR = sum([e[0] for e in knn2])
	return [(e[0], e[0] / sR, e[1]) for e in knn2]

def porcProyecto(knn, prop, ratings):
	suma = 0
	for e in knn:
		print ratings[e[2]][prop], e[1]
		suma += ratings[e[2]][prop] * e[1]
	#return sum([ratings[e[2]][prop] * e[1] for e in knn])
	return suma

def getMaxValueProp(v1, v2, properties, name2):
	max_i = -1
	max_e = 0
	for i in range(0, len(v2)):
		if max_e < v2[i] and v1[i] == 0:
			max_i = i
			max_e = v2[i]
	return (properties[max_i], max_e, name2) if max_i != -1 else ('--', max_e, name2)

def recomendations(name, knn, ratings, properties):
	recomendations = []
	for e in knn:
		recomendations.append(getMaxValueProp(ratings[name], ratings[e[2]], properties, e[2]))
	for e in recomendations:
		print e

def recomendations2(name, knn, ratings, properties):
	recomendations = [(0, '--', 0)] * len(properties)
	for i in range(0, len(properties)):
		for e in knn:
			recomendations[i] = (recomendations[i][0] + ratings[e[2]][i] * e[1], properties[i], i)
	recomendations = heapSort.heapSort(recomendations)
	for e in recomendations:
		if ratings[name][e[2]] == 0:
			print e

def menu():
	print "1. Distancias, Similitud, Correlacion"
	print "2. K-NN"
	print "3. % Prediccion"
	print "4. % Prediccion + RADIO"
	print "5. Recomendaciones"
	selectOne = input("Opcion: ")
	print ""
	return selectOne

def printNames(ratings):
	print "-- Los nombres son --"
	for k in ratings:
		print k + ",",
	print "\n"

def printProperties(properties):
	print "-- Las propiedades son --"
	for i in range(0, len(properties)):
		print `i` + ". " + `properties[i]` + ", ",
	print "\n"

def printList(listT):
	print "\n--------------------"
	for e in listT:
		print e
	print "--------------------\n"

def main():
	if len(sys.argv) != 2:
		print "Los argumentos son: distance.py <file>"
	else:
		file = sys.argv[1]
		ratings, properties = getRatingsTwo(file)
		while True:
			m1 = menu()
			if m1 == 1:
				printNames(ratings)
				name1, name2 = raw_input("Escriba 2 nombres: ").split()
				print "\n--------------------"
				print "D. Manhattan: " + `distanceType(ratings[name1], ratings[name2], 1)`
				print "D. Euclideana: " + `distanceType(ratings[name1], ratings[name2], 2)`
				print "S. Coseno: " + `cosenoSimilarity(ratings[name1], ratings[name2])`
				print "C. Pearson: " + `pearsonCorrelation(ratings[name1], ratings[name2])`
				print "--------------------\n"
			elif m1 == 2:
				printNames(ratings)
				print "-- Distancias --"
				print "1. Manhattan, 2. Euclidiana, 3. Coseno, 4. Pearson"
				name, k, dis = raw_input("Escriba el nombre, k y la distancia: ").split()
				knn = knnDistance(ratings, name, int(k), int(dis))
				printList(knn)
			elif m1 == 3:
				#ratings = {'Amanda': [4.5], 'Eric': [5], 'Sally': [3.5]}
				#properties = ['Grey']
				printNames(ratings)
				printProperties(properties)
				name, k, prop = raw_input("Escriba el nombre, k, y la propiedad: ").split()
				knn = knnDistance(ratings, name, int(k), 4)
				#knn = [(0.8, 0.4, 'Sally'), (0.7, 0.35, 'Eric'), (0.5, 0.25, 'Amanda')]
				printList(knn)
				print "--------------------"
				print "% Prediccion de " + `name` +  " para " + `properties[int(prop)]` + " de " + `k` + " K-NN es: " + `porcProyecto(knn, int(prop), ratings)`
				print "--------------------\n"
			elif m1 == 4:
				#ratings = {'Amanda': [4.5], 'Eric': [5], 'Sally': [3.5]}
				#properties = ['Grey']
				printNames(ratings)
				printProperties(properties)
				name, k, prop = raw_input("Escriba el nombre, radio, y la propiedad: ").split()
				knn = knnDistanceRadio(ratings, name, float(k), 4)
				#knn = [(0.8, 0.4, 'Sally'), (0.7, 0.35, 'Eric'), (0.5, 0.25, 'Amanda')]
				printList(knn)
				print "--------------------"
				print "% Prediccion de " + `name` +  " para " + `properties[int(prop)]` + " de " + `k` + " K-NN es: " + `porcProyecto(knn, int(prop), ratings)`
				print "--------------------\n"
			elif m1 == 5:
				printNames(ratings)
				print "-- Distancias --"
				print "1. Manhattan, 2. Euclidiana, 3. Coseno, 4. Pearson"
				name, k, dis = raw_input("Escriba el nombre, k y la distancia: ").split()
				knn = knnDistance(ratings, name, int(k), int(dis))
				#name, k, dis = raw_input("Escriba el nombre, radio y la distancia: ").split()
				#knn = knnDistance(ratings, name, float(k), 4)
				printList(knn)
				print "--------------------"
				print "% Recomendaciones para " + `name` +  " con los puntajes " + " en " + `k` + " K-NN son: "
				#print "% Recomendaciones para " + `name` +  " con los puntajes " + " en " + `k` + " K-NN-radio son: "
				recomendations2(name, knn, ratings, properties)
				print "--------------------\n"

main()	