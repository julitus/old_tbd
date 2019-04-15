import sys
import math
import heapSort

def getRatingsTwo(file):
	users = dict()
	idx_prop = dict()
	infile = open(file, 'r')
	for line in infile:
		row = line.strip('\n').split('::')
		val = float(row[2])
		if row[0] in users and type(users[row[0]]) == type({}):
			c = users[row[0]]['_size']
			users[row[0]][row[1]] = val
			users[row[0]]['_prom'] = (users[row[0]]['_prom'] * c) / (c + 1) + val / (c + 1)
			users[row[0]]['_size'] += 1
			if val < users[row[0]]['_min']:
				users[row[0]]['_min'] = val
			if val > users[row[0]]['_max']:
				users[row[0]]['_max'] = val
		else:
			users[row[0]] = {row[1]: val, '_prom': val, '_min': val, '_max': val, '_size': 1}
		if row[1] in idx_prop and type(idx_prop[row[1]]) == type({}):
			idx_prop[row[1]][row[0]] = val
		else:
			idx_prop[row[1]] = {row[0]: val}
	return users, idx_prop

def getMovies(file):
	movies = dict()
	infile = open(file, 'r')
	for line in infile:
		row = line.strip('\n').split('::')
		movies[row[0]] = (row[1], row[2])
	return movies

"""
def getSimilarityMatrix(users, idx_pr):
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
					i_op = v - users[k]['_prom']
					j_op = idx_pr[j][k] - users[k]['_prom']
					num += i_op * j_op
					den_i += pow(i_op, 2)
					den_j += pow(j_op, 2)
			similarity[i][j] = num / (math.sqrt(den_i) * math.sqrt(den_j)) if den_i and den_j else -1
			similarity[j][i] = similarity[i][j]
	return similarity
"""

def getSimilarityToProducts(users, pr_data1, pr_data2):
	num, den_i, den_j = 0, 0, 0;
	for i, v in pr_data1.items():
		if i in pr_data2:
			i_op = v - users[i]['_prom']
			j_op = pr_data2[i] - users[i]['_prom']
			num += i_op * j_op
			den_i += pow(i_op, 2)
			den_j += pow(j_op, 2)
	return num / (math.sqrt(den_i) * math.sqrt(den_j)) if den_i and den_j else float("inf")

def normalizeRatingName(data):
	nlz = dict()
	diff = data['_max'] - data['_min']
	for k, v in data.items():
		if k != '_prom' and k != '_min' and k != '_max' and k != '_size':
			nlz[k] = (2 * (v - data['_min']) - diff) / (diff)
	return nlz

def denormalizeScore(score, data):
	return ((score + 1) * (data['_max'] - data['_min'])) / 2 + data['_min']

def getRatingPronostique(pr, n_data, idx_prop, users):
	nlz_data = normalizeRatingName(n_data)
	#print nlz_data
	#print "\n--------------------"
	num, den = 0, 0
	for k, v in nlz_data.items():
		if pr != k:
			sim = getSimilarityToProducts(users, idx_prop[pr], idx_prop[k])
			if sim != float("inf"):
			#num, den = num + v * similarity[pr][k], den + abs(similarity[pr][k])
			#print `users` + ' ( ' + `v` + ' > ' + `sim` + ' ) '
				num, den = num + v * sim, den + abs(sim)
	return denormalizeScore(num / den, n_data) if den else -float("inf")

def nRecomentadions(k, n_data, idx_prop, movies, users):
	score = []
	for key in idx_prop:
		if not(key in n_data):
			score.append((getRatingPronostique(key, n_data, idx_prop, users), key))
	score = heapSort.heapSort(score)
	return [(score[i], movies[score[i][1]]) for i in range(0, k)]

def menu():
	print "1. Get similarity to products"
	print "2. Points to product"
	print "3. Recomendations"
	print "4. Agregar Usuario"
	print "5. Agregar Pelicula + Rating a Usuario"
	selectOne = input("Opcion: ")
	print ""
	return selectOne

def printM(m):
	for e in m:
		print e
	print ""

def main():
	if len(sys.argv) != 3:
		print "Los argumentos son: big_movies_products.py <movies> <ratings>"
	else:
		movies = sys.argv[1]
		rat = sys.argv[2]
		users, idx_prop = getRatingsTwo(rat)
		movies = getMovies(movies)
		#similarity = getSimilarityMatrix(users, idx_prop)
		while True:
			m1 = menu()
			if m1 == 1:
				pr1, pr2 = raw_input("Elija 2 productos: ").split()
				print "\n--------------------"
				#print "Similitud: " + `similarity[pr1][pr2]`
				print "Similitud: " + `getSimilarityToProducts(users, idx_prop[pr1], idx_prop[pr2])`
				print "--------------------\n"
			elif m1 == 2:
				name, pr = raw_input("Escriba el nombre, y elija el producto: ").split()
				print "\n--------------------"
				#print "Rating of " + name + " to " + `pr` + ": " + `getRatingPronostique(pr, users[name], similarity)`
				print "Rating of " + name + " to " + `movies[pr]` + ": " + `getRatingPronostique(pr, users[name], idx_prop, users)`
				print "--------------------\n"
			elif m1 == 3:
				name, k = raw_input("Escriba el nombre, y la cantidad de recomendaciones: ").split()
				print "\n" + `k` + " Recomendaciones--------------------\n"
				recs = nRecomentadions(int(k), users[name], idx_prop, movies, users)
				printM(recs)
				print "--------------------\n"
			elif m1 == 4:
				id_user = raw_input("Agregar Usuario: ")
				users[id_user] = dict()
			elif m1 == 5:
				file = raw_input("Escoje Usuario, id-Producto y rating: ")
				for line in open(file, 'r'):
					row = line.strip('\n').split(',')
					val = float(row[2])
					if row[0] in users and type(users[row[0]]) == type({}):
						c = users[row[0]]['_size']
						users[row[0]][row[1]] = val
						users[row[0]]['_prom'] = (users[row[0]]['_prom'] * c) / (c + 1) + val / (c + 1)
						users[row[0]]['_size'] += 1
						if val < users[row[0]]['_min']:
							users[row[0]]['_min'] = val
						if val > users[row[0]]['_max']:
							users[row[0]]['_max'] = val
					else:
						users[row[0]] = {row[1]: val, '_prom': val, '_min': val, '_max': val, '_size': 1}
					if row[1] in idx_prop and type(idx_prop[row[1]]) == type({}):
						idx_prop[row[1]][row[0]] = val
					else:
						idx_prop[row[1]] = {row[0]: val}

main()

# python products/big_movies_adjustCosin.py ml-latest-small/movies.csv ml-latest-small/ratings.csv