if all( (a if a < 10 else False for a in [1, 2, 3, 4, 5, 100, 0]*100000000) ):
	print(444)
