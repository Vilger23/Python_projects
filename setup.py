letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "Å", 'Ä', 'Ö']
letter_points = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 4, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10, 4, 5, 3]
points = {letter:point for letter, point in zip(letters,letter_points)}

word_list_file = open("word_list.txt")
word_list = [word[:-1] for word in word_list_file.readlines()]

word_list_file.close()

word_list = [w.upper() for w in word_list]