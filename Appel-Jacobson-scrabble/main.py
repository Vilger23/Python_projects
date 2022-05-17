from solver import *

language = 'sv'
rack = 'vuunaäe'
solver = SolveState(basic_language(language), sample_board(), language, rack)
solver.find_all_options()
SolveState.legal_moves.sort(key = lambda x:x[0], reverse = True)
for i in range(3):
    print(SolveState.legal_moves[i][0])
    print(SolveState.legal_moves[i][1])