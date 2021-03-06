import sys
import math
import heapSort

def getRatings(file):
	names = dict()
	infile = open(file, 'r')
	for line in infile:
		row = line.strip('\n').replace('"', '').split(';')
		if row[0] in names and type(names[row[0]]) == type({}):
			names[row[0]][row[1]] = float(row[2])
		else:
			names[row[0]] = {row[1]: float(row[2])}
	return names

def getBooks(file):
	names = dict()
	infile = open(file, 'r')
	for line in infile:
		row = line.replace('"', '').split(';')
		names[row[0]] = (row[1], row[2])
	return names

def distanceType(x, y, r):
	s = 0
	exist = False
	for key, val in x.items():
		if key in y:
			s += pow(abs(val - y[key]), r)
			exist = True
	#s = sum([(pow(abs(e[0] - e[1]), r) if (e[0] and e[1]) else 0) for e in zip(x, y)])
	return pow(s, 1.0 / r) if exist else float("inf")

def cosenoSimilarity(x, y):
	sXY, mX, mY = 0, 0, 0
	for key, val in x.items():
		sXY += val * y[key] if key in y else 0
		mX += pow(val, 2)
	mY = sum([pow(val, 2) for key, val in y.items()])
	#for i in range(0, len(x)):
		#sXY += x[i] * y[i] 
		#mX, mY = mX + pow(x[i], 2), mY + pow(y[i], 2)
	den = (math.sqrt(mX) * math.sqrt(mY))
	return sXY / den if den != 0 else -1.0

def pearsonCorrelation(x, y):
	sX, sY, sX2, sY2, sXY = 0, 0, 0, 0, 0
	n = 0
	for key, val in x.items():
		if key in y:
			sX, sY = sX + val, sY + y[key]
			sX2, sY2 = sX2 + pow(val, 2), sY2 + pow(y[key], 2)
			sXY += val * y[key]
			n += 1
	#for i in range(0, len(x)):
	#	if x[i] != 0 and y[i] != 0:
	#		sX, sY = sX + x[i], sY + y[i]
	#		sX2, sY2 = sX2 + pow(x[i], 2), sY2 + pow(y[i], 2)
	#		sXY += x[i] * y[i]	
	#		n += 1
	den = (math.sqrt(n * sX2 - pow(sX, 2)) * math.sqrt(n * sY2 - pow(sY, 2)))
	return (n * sXY - sX * sY) / den if den != 0 else  -1.0

def funcDistance(x, y, dis):
	if dis == 1 or dis == 2:
		return distanceType(x, y, dis)
	elif dis == 3:
		return cosenoSimilarity(x, y)
	elif dis == 4:
		return pearsonCorrelation(x, y)
	return 0

def knnDistance(ratings, code, k, dis):
	knn = []
	for key, val in ratings.items():
		if key != code:
			knn.append((funcDistance(ratings[code], val, dis), key))
	if dis == 4 or dis == 3: 
		knn = heapSort.heapSort(knn)[:k]
	else:
		knn = heapSort.heapSortAsc(knn)[:k]
	sR = sum([e[0] for e in knn])
	return [(e[0], e[0] / sR if sR != 0 else float("inf"), e[1]) for e in knn] # Solo para Pearson y Coseno

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
	return [(e[0], e[0] / sR, e[1]) for e in knn2] # Solo para Pearson y Coseno

def getMaxValueProp(v1, v2, properties, name2):
	#exist = False
	max_key = '0'
	max_val = 0
	for key, val in v2.items():
		if not(key in v1) and val >= max_val:
			max_key = key
			max_val = val
	return (properties[max_key] if max_key in properties else 'undefined', max_val, name2) if max_key != '0' else ('--', max_val, name2)
	#max_i = -1
	#max_e = 0
	#for i in range(0, len(v2)):
	#	if max_e < v2[i] and v1[i] == 0:
	#		max_i = i
	#		max_e = v2[i]
	#return (properties[max_i], max_e, name2) if max_i != -1 else ('--', max_e, name2)

def recomendations(name, knn, ratings, properties):
	recomendations = []
	for e in knn:
		recomendations.append(getMaxValueProp(ratings[name], ratings[e[2]], properties, e[2]))
	for e in recomendations:
		print e

def recomendations2(name, knn, ratings, properties):
	recomendations = []
	rec = {}
	i = 0
	for e in knn:
		for key, val in ratings[e[2]].items():
			if not(key in ratings[name]):
				if key in rec:
					recomendations[rec[key]] = (recomendations[rec[key]][0] + val * e[1], key, properties[key] if key in properties else 'undefined')
				else:
					recomendations.append((val * e[1], key, properties[key] if key in properties else 'undefined'))
					rec[key] = i
					i += 1

	recomendations = heapSort.heapSort(recomendations) # Solo para Pearson y Coseno
	for e in recomendations:
		print e
	#recomendations = [(0, '--', 0)] * len(properties)
	#for i in range(0, len(properties)):
	#	for e in knn:
	#		recomendations[i] = (recomendations[i][0] + ratings[e[2]][i] * e[1], properties[i], i)
	#recomendations = heapSort.heapSort(recomendations, 1)
	#for e in recomendations:
	#	if ratings[name][e[2]] == 0:
	#		print e

def porcPrediccion(knn, prop, ratings):
	s = 0
	for e in knn:
		s += e[1] * (ratings[e[2]][prop] if prop in ratings[e[2]] else 0)
	#return sum([ratings[e[2]][prop] * e[1] for e in knn])
	return s

def menu():
	print "1. Distancias, Similitud, Correlacion"
	print "2. K-NN"
	print "3. % Prediccion"
	print "4. % Prediccion + RADIO"
	print "5. Recomendaciones"
	selectOne = input("Opcion: ")
	print ""
	return selectOne

def printList(listT):
	print "\n--------------------"
	for e in listT:
		print e
	print "--------------------\n"

def main():
	if len(sys.argv) != 4:
		print "Los argumentos son: distance.py <users> <books> <ratings>"
	else:
		users = sys.argv[1]
		books = sys.argv[2]
		rat = sys.argv[3]
		ratings = getRatings(rat)
		books = getBooks(books)
		while True:
			m1 = menu()
			if m1 == 1:
				cod1, cod2 = raw_input("Escriba 2 de los dos codigos de usuario: ").split()
				print "\n--------------------"
				if cod1 in ratings and cod2 in ratings:
					print "D. Manhattan: " + `distanceType(ratings[cod1], ratings[cod2], 1)`
					print "D. Euclideana: " + `distanceType(ratings[cod1], ratings[cod2], 2)`
					print "S. Coseno: " + `cosenoSimilarity(ratings[cod1], ratings[cod2])`
					print "C. Pearson: " + `pearsonCorrelation(ratings[cod1], ratings[cod2])`
				else:
					print ">> Los codigos ingresados no han calificado libros"
				print "--------------------\n"
			elif m1 == 2:
				print "-- Distancias --"
				print "1. Manhattan, 2. Euclidiana, 3. Coseno, 4. Pearson"
				code, k, dis = raw_input("Escriba el codigo de usuario, k y la distancia: ").split()
				knn = knnDistance(ratings, code, int(k), int(dis))
				printList(knn)
			elif m1 == 3:
				code, k, dis, prop = raw_input("Escriba el codigo de usuario, k, la distancia y el codigo de libro: ").split()
				knn = knnDistance(ratings, code, int(k), int(dis))
				printList(knn)
				print "--------------------"
				print "% Prediccion de " + `code` +  " para " + `prop` + " de " + `k` + " K-NN es: " + `porcPrediccion(knn, prop, ratings)`
				print "--------------------\n"
			elif m1 == 4:
				code, k, dis, prop = raw_input("Escriba el codigo de usuario, radio, la distancia y el codigo de libro: ").split()
				knn = knnDistanceRadio(ratings, code, float(k), int(dis))
				printList(knn)
				print "--------------------"
				print "% Prediccion de " + `code` +  " para " + `prop` + " de " + `k` + " K-NN RADIO es: " + `porcPrediccion(knn, prop, ratings)`
				print "--------------------\n"
			elif m1 == 5:
				print "-- Distancias --"
				print "1. Manhattan, 2. Euclidiana, 3. Coseno, 4. Pearson"
				code, k, dis = raw_input("Escriba el codigo de usuario, k y la distancia: ").split()
				knn = knnDistance(ratings, code, int(k), int(dis))
				printList(knn)
				print "--------------------"
				print "% Recomendaciones para " + `code` +  " con los puntajes " + " en " + `k` + " K-NN son: "
				#print "% Recomendaciones para " + `code` +  " con los puntajes " + " en " + `k` + " K-NN-radio son: "
				#recomendations(code, knn, ratings, books)
				recomendations2(code, knn, ratings, books)
				print "--------------------\n"

main()