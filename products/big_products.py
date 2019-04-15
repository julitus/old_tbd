import sys
import math
import heapSort

def getRatingsTwo(file):
	names = dict()
	idx_prop = dict()
	infile = open(file, 'r')
	for line in infile:
		row = line.strip('\n').replace('"', '').split(';')
		val = float(row[2])
		if row[0] in names and type(names[row[0]]) == type({}):
			c = names[row[0]]['_size']
			names[row[0]][row[1]] = val
			names[row[0]]['_prom'] = (names[row[0]]['_prom'] * c) / (c + 1) + val / (c + 1)
			names[row[0]]['_size'] += 1
			if val < names[row[0]]['_min']:
				names[row[0]]['_min'] = val
			if val > names[row[0]]['_max']:
				names[row[0]]['_max'] = val
		else:
			names[row[0]] = {row[1]: val, '_prom': val, '_min': val, '_max': val, '_size': 1}
		if row[1] in idx_prop and type(idx_prop[row[1]]) == type({}):
			idx_prop[row[1]][row[0]] = val
		else:
			idx_prop[row[1]] = {row[0]: val}
	return names, idx_prop

def getBooks(file):
	names = dict()
	infile = open(file, 'r')
	for line in infile:
		row = line.replace('"', '').split(';')
		names[row[0]] = (row[1], row[2])
	return names

"""
def getSimilarityMatrix(names, idx_pr):
	similarity = dict()
	for i, v_i in idx_pr.items():
		if not i in similarity:
			similarity[i] = dict()
		for j, v_j in idx_pr.items():
			if not j in similarity:
				similarity[j] = dict()
			num, den_i, den_j = 0, 0, 0;
			for k, v in idx_pr[i].items():
				if k in idx_pr[j]:
					i_op = v - names[k]['_prom']
					j_op = idx_pr[j][k] - names[k]['_prom']
					num += i_op * j_op
					den_i += pow(i_op, 2)
					den_j += pow(j_op, 2)
			similarity[i][j] = num / (math.sqrt(den_i) * math.sqrt(den_j)) if den_i and den_j else -1
			similarity[j][i] = similarity[i][j]
	return similarity
"""

def getSimilarityToProducts(names, pr_data1, pr_data2):
	num, den_i, den_j = 0, 0, 0;
	for i, v in pr_data1.items():
		if i in pr_data2:
			i_op = v - names[i]['_prom']
			j_op = pr_data2[i] - names[i]['_prom']
			num += i_op * j_op
			den_i += pow(i_op, 2)
			den_j += pow(j_op, 2)
	return num / (math.sqrt(den_i) * math.sqrt(den_j)) if den_i and den_j else -1

#def getSimilarityVectorToProduct():


def normalizeRatingName(data):
	nlz = dict()
	diff = data['_max'] - data['_min']
	for k, v in data.items():
		if k != '_prom' and k != '_min' and k != '_max' and k != '_size':
			nlz[k] = (2 * (v - data['_min']) - diff) / (diff)
	return nlz

def denormalizeScore(score, data):
	return ((score + 1) * (data['_max'] - data['_min'])) / 2 + data['_min']

def getRatingPronostique(pr, n_data, idx_prop, names):
	nlz_data = normalizeRatingName(n_data)
	print nlz_data
	print "\n--------------------"
	num, den = 0, 0
	for k, v in nlz_data.items():
		if pr != k:
			sim = getSimilarityToProducts(names, idx_prop[pr], idx_prop[k])
			#num, den = num + v * similarity[pr][k], den + abs(similarity[pr][k])
			num, den = num + v * sim, den + abs(sim)
	return denormalizeScore(num / den, n_data)

def menu():
	print "1. Get similarity to products"
	print "2. Points to product"
	selectOne = input("Opcion: ")
	print ""
	return selectOne

def printNames(ratings):
	print "-- Los nombres son --"
	for k in ratings:
		print k + ",",
	print "\n"

def printProperties(properties):
	print "-- Los productos son --"
	for i in range(0, len(properties)):
		print `i` + ". " + `properties[i]` + ", ",
	print "\n"

def main():
	if len(sys.argv) != 4:
		print "Los argumentos son: distance.py <users> <books> <ratings>"
	else:
		users = sys.argv[1]
		books = sys.argv[2]
		rat = sys.argv[3]
		names, idx_prop = getRatingsTwo(rat)
		books = getBooks(books)
		#similarity = getSimilarityMatrix(names, idx_prop)
		while True:
			m1 = menu()
			if m1 == 1:
				pr1, pr2 = raw_input("Elija 2 productos: ").split()
				print "\n--------------------"
				#print "Similitud: " + `similarity[pr1][pr2]`
				print "Similitud: " + `getSimilarityToProducts(names, idx_prop[pr1], idx_prop[pr2])`
				print "--------------------\n"
			elif m1 == 2:
				name, pr = raw_input("Escriba el nombre, y elija el producto: ").split()
				print "\n--------------------"
				#print "Rating of " + name + " to " + `pr` + ": " + `getRatingPronostique(pr, names[name], similarity)`
				print "Rating of " + name + " to " + `pr` + ": " + `getRatingPronostique(pr, names[name], idx_prop, names)`
				print "--------------------\n"

main()	