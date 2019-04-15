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
			users[row[0]][row[1]] = val
		else:
			users[row[0]] = {row[1]: val}
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

def getDeviation(pr_data1, pr_data2):
	num = 0;
	card = 0;
	for i, v in pr_data1.items():
		if i in pr_data2:
			num += v - pr_data2[i]
			card += 1
	return (num / card if card else float("inf")), card

def getRatingPronostique(pr, n_data, idx_prop):
	num, den = 0, 0
	for k, v in n_data.items():
		if pr != k:
			#dev, card = getDeviation(idx_prop[k], idx_prop[pr])
			dev, card = getDeviation(idx_prop[pr], idx_prop[k])
			if dev != float("inf"):
				#print "inf"
				#print dev, card
				num += (dev + v) * card
				den += card
	#print num, den
	return num / den if den else float("inf")

def nRecomentadions(k, n_data, idx_prop, movies):
	score = []
	for key in idx_prop:
		if not(key in n_data):
			rat = getRatingPronostique(key, n_data, idx_prop)
			if rat != float("inf"):
				score.append((rat, key))
	score = heapSort.heapSort(score)
	return [(score[i], movies[score[i][1]]) for i in range(0, k)]

def menu():
	print "1. Get deviation to products"
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
				dev, card = getDeviation(idx_prop[pr1], idx_prop[pr2])
				print "Desviacion: " + `dev` + " -> Cardinalidad: " + `card`
				print "--------------------\n"
			elif m1 == 2:
				name, pr = raw_input("Escriba el nombre, y elija el producto: ").split()
				print "\n--------------------"
				#print "Rating of " + name + " to " + `pr` + ": " + `getRatingPronostique(pr, users[name], similarity)`
				print "Rating of " + name + " to " + `movies[pr]` + ": " + `getRatingPronostique(pr, users[name], idx_prop)`
				print "--------------------\n"
			elif m1 == 3:
				name, k = raw_input("Escriba el nombre, y la cantidad de recomendaciones: ").split()
				print "\n" + `k` + " Recomendaciones--------------------\n"
				recs = nRecomentadions(int(k), users[name], idx_prop, movies)
				printM(recs)
				print "--------------------\n"
			elif m1 == 4:
				id_user = raw_input("Agregar Usuario: ")
				users[id_user] = {}
			elif m1 == 5:
				file = raw_input("Escoje Usuario, id-Producto y rating: ")
				for line in open(file, 'r'):
					row = line.strip('\n').split(',')
					val = float(row[2])
					if row[0] in users and type(users[row[0]]) == type({}):
						users[row[0]][row[1]] = val
					else:
						users[row[0]] = {row[1]: val}
					if row[1] in idx_prop and type(idx_prop[row[1]]) == type({}):
						idx_prop[row[1]][row[0]] = val
					else:
						idx_prop[row[1]] = {row[0]: val}
					#if id_movies in idx_prop and type(idx_prop[id_movies]) == type({}):
					#	idx_prop[id_movies][id_user] = float(rat)
					#else:
					#	idx_prop[id_movies] = {id_user: float(rat)}

main()

# python products/big_movies_slopeOne.py ml-latest-small/movies.csv ml-latest-small/ratings.csv