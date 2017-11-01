'''
Esse programa foi desenvolvido para apresentação do segundo trabalho na diciplina de Inteligência Artifical (GBC063) do cusro de Bacharelado
em Ciências da Computação (BCC) da Universidade Federal de Uberlândia (UFU), ministrada durane o semestre 2017-2.
O deselvolvimento se baseou nos estudos do capítulo 5.2 do livro Artificial Intelligence: A Modern Approach (3rd Edition), Peter Norvig,
Stuart J. Russell.

Autores: Vinicius Gonzaga Rocha, Rafael Melo
Contato: viniciusrocha0996@gmail.com

This program was developed for the presentation of the second homework of the Artificial Intelligence course (GBC063) from the Computer
Science undergraduate course of the Federal University of Uberlândia, that took place during the semester of 2017-2.
The development was based on the chapter 5.2 of the Artificial Intelligence: A Modern Approach (3rd Edition) book, from Peter Norvig,
Stuart J. Russell.

Authors: Vinicius Gonzaga Rocha, Rafael Melo
Contact: viniciusrocha0996@gmail.com
'''

import copy as cp

class State:

    def __init__ (self):
        self.human = 'x'
        self.ai = 'o'
        self.empty = '-'	
        self.squares = []						# mantem o tabuleiro do jogo
        self.current_player = self.human		# jogador na atual rodada, o programa sempre inicia com o humano
        self.wins = [[0,1,2],[3,4,5],[6,7,8],  	# combos que resultam em vitórias
                     [0,3,6],[1,4,7],[2,5,8],
                     [0,4,8],[2,4,6]]

        for i in range(9):
            self.squares.append(self.empty)		# preenche inicialmente todos os espaços com vazio	

    def show_state (self):
        print('\n---------------------------------------\n')

        for i in range(1,10):
            print('|' + self.squares[i-1] + '|', end='')
            if i%3 == 0:
                print('')

        print('\n---------------------------------------\n')


    def check_win (self, player):
        for combo in self.wins:
            won = True
            for square in combo:
                if self.squares[square] != player:
                    won = False
            if won == True:
                return True
        return False


    def is_valid_play(self, move):
    	if self.squares[move] == self.empty:
    		return True
    	return False


    def check_tie (self):
    	
        if len([x for x in self.squares if x == self.empty]) != 0:
            return False
        return True

    def actions (self):
        available = []
        for i in range(9):
            if self.squares[i] == self.empty:
                available.append(i)
        return available


    def terminal_test (self):
        return self.check_win('x') or self.check_win('o') or self.check_tie()


    def make_play (self, move):
    	
        self.squares[move] = self.current_player

        self.current_player = self.human if self.current_player == self.ai else self.ai


    def result (self, move):
        clone = cp.deepcopy(self)
        clone.make_play(move)
        return clone

    def utility(self):
        if self.check_win(self.human):
            return -10
        elif self.check_win(self.ai):
            return 10
        elif self.check_tie():
            return 0


    def player (self):
        return self.current_player


def alpha_beta(state):
    moves = state.actions()
    best_move = moves[0]
    v = -10000
    
    for move in moves:
        clone = state.result(move)
        score = min_play(clone, -10000, 10000)
        if score > v:
            best_move = move
            v = score

    return best_move

def max_play(state, a, b):
    if state.terminal_test():
        return state.utility()

    moves = state.actions()
    v = -10000

    for move in moves:
        clone = state.result(move)
        v = max(v, min_play(clone, a,b))
        if v >= b:
            return v
        a = max(a, v)
    return v


def min_play(state, a, b):
    if state.terminal_test():
        return state.utility()

    v = 10000
    moves = state.actions()
    
    for move in moves:
        clone = state.result(move)
        v = min(v, max_play(clone, a,b))
        if v <= a:
            return v
        b = min(b, v)
    return v

def main():

	state = State()

	while (not state.terminal_test()): # enquanto o jogo nao acabar, roda o laço
		state.show_state()
	
		play = int(input('Faça uma jogada (1-9): '))

		if (play > 0 and play < 10): # verificação da entrada do usuário

			while(not state.is_valid_play(play-1)): # verificação da entrada do usuário
				print('Jogada inválida, tente novamente')
				state.show_state()
				play = int(input('Faça uma jogada (1-9): '))

			state.make_play(play-1) # caso tudo esteja certo, realiza a jogada

			if(not state.terminal_test()): # necessário para verificar apenas se o usuário empatou o jogo, uma vez que o nunca irá vencer
				state.make_play(alpha_beta(state)) # busca a melhor jogada com minimax e realiza
				state.show_state()

			# verificações do término da partida
			if(state.utility() == 10):
				state.show_state()
				print('\nVoce perdeu!\n')
			elif(state.utility() == -10): # Nao vai ocorrer, pode até ser retirado
				state.show_state()
				print('\nVoce venceu!\n')
			elif(state.utility() == 0):
				state.show_state()
				print('\nEmpate\n')

		else:
			print('Entre com um número entre 1 e 9')

	input('')

main()
