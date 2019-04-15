import sys
import math
import heapSort

def getRatingsTwo(file):
	names = dict()
	idx_prop = dict()
	properties = []
	infile = open(file, 'r')
	for i in infile.readline().strip('\n').split(','):
		properties.append(i)
		if i != '':
			idx_prop[i] = dict()
	for line in infile:
		prom, siz = 0, 0
		min_v, max_v = float("inf"), -1
		row = line.strip('\n').split(',')
		names[row[0]] = dict()
		for i in range(1, len(row)):
			if row[i] != '':
				val = float(row[i])
				prom, siz = prom + val, siz + 1 
				names[row[0]][properties[i]] = val
				min_v = val if val < min_v else min_v
				max_v = val if val > max_v else max_v
				idx_prop[properties[i]][row[0]] = val
		if min_v != float("inf"):
			names[row[0]]['_min'] = min_v;
		if max_v != -1:
			names[row[0]]['_max'] = max_v;
		names[row[0]]['_prom'] = prom / siz;
	return names, properties[1:], idx_prop

def getSimilarityMatrix(names, pr, idx_pr):
	similarity = dict()
	for i in range(0, len(pr) - 1):
		if not pr[i] in similarity:
			similarity[pr[i]] = dict()
		for j in range(i + 1, len(pr)):
			if not pr[j] in similarity:
				similarity[pr[j]] = dict()
			num, den_i, den_j = 0, 0, 0;
			for k, v in idx_pr[pr[i]].items():
				if k in idx_pr[pr[j]]:
					i_op = v - names[k]['_prom']
					j_op = idx_pr[pr[j]][k] - names[k]['_prom']
					num += i_op * j_op
					den_i += pow(i_op, 2)
					den_j += pow(j_op, 2)
			similarity[pr[i]][pr[j]] = num / (math.sqrt(den_i) * math.sqrt(den_j))
			similarity[pr[j]][pr[i]] = similarity[pr[i]][pr[j]]
	return similarity

def getSimilarityToProducts(users, pr_data1, pr_data2):
	num, den_i, den_j = 0, 0, 0;
	for i, v in pr_data1.items():
		if i in pr_data2:
			i_op = v - users[i]['_prom']
			j_op = pr_data2[i] - users[i]['_prom']
			num += i_op * j_op
			den_i += pow(i_op, 2)
			den_j += pow(j_op, 2)
	return num / (math.sqrt(den_i) * math.sqrt(den_j)) if den_i and den_j else -1

def normalizeRatingName(data):
	nlz = dict()
	diff = data['_max'] - data['_min']
	for k, v in data.items():
		if k != '_prom' and k != '_min' and k != '_max':
			nlz[k] = (2 * (v - data['_min']) - diff) / (diff)
	return nlz

def denormalizeScore(score, data):
	return ((score + 1) * (data['_max'] - data['_min'])) / 2 + data['_min']

def getRatingPronostique(pr, n_data, idx_prop, users):
	nlz_data = normalizeRatingName(n_data)
	print nlz_data
	num, den = 0, 0
	for k, v in nlz_data.items():
		if pr != k:
			sim = getSimilarityToProducts(users, idx_prop[pr], idx_prop[k])
			#num, den = num + v * similarity[pr][k], den + abs(similarity[pr][k])
			print `v` + ' > ' + `sim` + ' ) '
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

#def printList(listT):
#	print "\n--------------------"
#	for e in listT:
#		print e
#	print "--------------------\n"

def main():
	if len(sys.argv) != 2:
		print "Los argumentos son: small_products.py <file>"
	else:
		file = sys.argv[1]
		names, properties, idx_prop = getRatingsTwo(file)
		similarity = getSimilarityMatrix(names, properties, idx_prop)
		while True:
			m1 = menu()
			if m1 == 1:
				printProperties(properties)
				pr1, pr2 = raw_input("Elija 2 productos: ").split()
				print "\n--------------------"
				print "Similitud: " + `similarity[properties[int(pr1)]][properties[int(pr2)]]`
				print "--------------------\n"
			elif m1 == 2:
				printNames(names)
				printProperties(properties)
				name, pr = raw_input("Escriba el nombre, y elija el producto: ").split()
				print "\n--------------------"
				#print "Rating of " + name + " to " + `properties[int(pr)]` + ": " + `getRatingPronostique(properties[int(pr)], names[name], similarity)`
				print "Rating of " + name + " to " + `properties[int(pr)]` + ": " + `getRatingPronostique(properties[int(pr)], names[name], idx_prop, names)`
				print "--------------------\n"

main()	