import random
import copy
import numpy as np

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        count_b, count_r = 0, 0
        for r in state:
            for c in r:
                if c == 'b': count_b += 1
                elif c == 'r': count_r += 1
        drop_phase = False if (count_b >= 4 and count_r >= 4) else True # TODO: detect drop phase

        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!

            move = []
            val, next_state = self.max_value(state, 0)
            arr1 = np.array(state) == np.array(next_state)
            arr2 = np.where(arr1 == False) # find differing spots
            if state[arr2[0][0]][arr2[1][0]] == " ":
                orig_row = arr2[0][1]
                orig_col = arr2[1][1]
                new_row = arr2[0][0]
                new_col = arr2[1][0]
            else:
                orig_row = arr2[0][0]
                orig_col = arr2[1][0]
                new_row = arr2[0][1]
                new_col = arr2[1][1]

            move.insert(0, (new_row.item(), new_col.item()))
            move.insert(1, (orig_row.item(), orig_col.item()))
            return move

        # implement a minimax algorithm to play better
        move = []
        value, next_state = self.max_value(state,0)
        arr1 = np.array(state) == np.array(next_state)
        arr2 = np.where(arr1 == False)
        new_row = arr2[0][0]
        new_col = arr2[1][0]
        while not state[new_row][new_col] == " ":
            new_row = arr2[0][0]
            new_col = arr2[1][0]

        move.insert(0, (new_row.item(), new_col.item()))
        return move

    def succ(self, state, curr_player):
        """
        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.
        Return:
            successors (list): a list of the legal successors
        """
        successors = []
        count_b = 0
        count_r = 0
        for r in state:
            for c in r:
                if c == 'b': count_b += 1
                elif c == 'r': count_r += 1
        drop_phase = False if (count_b >= 4 and count_r >= 4) else True #detect drop phase

        #Code for drop phase
        if drop_phase:          
            for row in range(len(state)):
                for cell in range(len(state[row])):
                    if state[row][cell] == " ":
                        successor = copy.deepcopy(state)
                        successor[row][cell] = curr_player
                        successors.append(successor)

        #Code for continued gameplay
        else:           
            moves = [[1,0], [-1,0], [0,1], [0,-1], [1,1], [1,-1], [-1,-1], [-1,1]]
            for move in moves:
                for row in range(len(state)):
                    for col in range(len(state[row])):                 
                        if row + move[0] < 0 or row + move[0] > 4 \
                            or col + move[1] < 0 or col + move[1] > 4: continue

                        if state[row][col] == curr_player and state[row + move[0]][col + move[1]] == " ":
                            successor = copy.deepcopy(state)
                            successor[row + move[0]][col + move[1]] = curr_player
                            successor[row][col] = " "
                            successors.append(successor)

        return successors

    def heuristic_game_value(self, state):

        #you should call the game_value method from this function to determine whether 
        #the state is a terminal state before you start evaluating it heuristically


        self_cnt, temp1 = 0, 0
        opp_cnt, temp2 = 0, 0

        #Horizontal score
        for r in range(4):
            temp1 = 0
            for c in range(4):
                if state[r][c] == self.my_piece:
                    temp1 += 1
            if temp1 > self_cnt:
                self_cnt = temp1

        r, c = 0,0
        for r in range(4):
            temp2 = 0
            for c in range(4):
                if state[r][c] == self.opp:
                    temp2 += 1
            if temp2 > opp_cnt:
                opp_cnt = temp2


        #Vertical score
        r,c = 0,0
        for c in range(4):
            temp1 = 0
            for r in range(4):
                if state[r][c] == self.my_piece:
                    temp1 += 1
            if temp1 > self_cnt:
                self_cnt = temp1

        r,c = 0,0
        for c in range(4):
            temp2 = 0
            for r in range(4):
                if state[r][c] == self.opp:
                    temp2 += 1
            if temp2 > self_cnt:
                opp_cnt = temp2

        
        #Diagonal / Score
        r,c = 0,0
        temp1 = 0
        for r in range(3, 5):        
            for c in range(2):
                if state[r][c] == self.my_piece:
                    temp1 += 1
                if state[r - 1][c + 1] == self.my_piece:
                    temp1 += 1
                if state[r - 2][c + 2] == self.my_piece:
                    temp1 += 1
                if state[r - 3][c + 3] == self.my_piece:
                    temp1 += 1

                if temp1 > self_cnt:
                    self_cnt = temp1
                temp1 = 0

        r,c = 0,0
        temp2 = 0
        for r in range(3, 5):
            temp2 = 0
            for c in range(2):
                if state[r][c] == self.opp:
                    temp2 += 1
                if state[r - 1][c + 1] == self.opp:
                    temp2 += 1
                if state[r - 2][c + 2] == self.opp:
                    temp2 += 1
                if state[r - 3][c + 3] == self.opp:
                    temp2 += 1
                if temp2 > opp_cnt:
                    oppmax = temp2
                temp2 = 0

        # Diagonal \ Score
        r,c = 0,0
        temp1 = 0
        for r in range(2):
            for c in range(2):
                if state[r][c] == self.my_piece:
                    temp1 += 1
                if state[r + 1][c + 1] == self.my_piece:
                    temp1 += 1
                if state[r + 2][c + 2] == self.my_piece:
                    temp1 += 1
                if state[r + 3][c + 3] == self.my_piece:
                    temp1 += 1
                if temp1 > self_cnt:
                    self_cnt = temp1
                temp1 = 0

        r,c = 0,0
        temp2 = 0
        for r in range(2):
            for c in range(2):
                if state[r][c] == self.opp:
                    temp2 += 1
                if state[r + 1][c + 1] == self.opp:
                    temp2 += 1
                if state[r + 2][c + 2] == self.opp:
                    temp2 += 1
                if state[r + 3][c + 3] == self.opp:
                    temp2 += 1
                if temp2 > opp_cnt:
                    opp_cnt = temp2
                temp2 = 0

        # 2X2 Score
        r,c = 0,0
        temp1 = 0
        for r in range(4):        
            for c in range(4):
                if state[r][c] == self.my_piece:
                    temp1 += 1
                if state[r][c + 1] == self.my_piece:
                    temp1 += 1
                if state[r + 1][c] == self.my_piece:
                    temp1 += 1
                if state[r + 1][c + 1]== self.my_piece:
                    temp1 += 1
                if temp1 > self_cnt:
                    self_cnt = temp1
                temp1 = 0

        r,c = 0,0
        temp2 = 0
        for r in range(4):
            for c in range(4):
                if state[r][c] == self.opp:
                    temp2 += 1
                if state[r][c + 1] == self.opp:
                    temp2 += 1
                if state[r + 1][c] == self.opp:
                    temp2 += 1
                if state[r + 1][c + 1]== self.opp:
                    temp2 += 1
                if temp2 > opp_cnt:
                    opp_cnt = temp2
                temp2 = 0
        

        if self_cnt >= opp_cnt:
            return self_cnt / 6
        elif self_cnt < opp_cnt:
            return (opp_cnt / 6) * (-1)
        else:
            return 0

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def max_value(self, state, depth):
        """
        Args:
        state (list of lists): current state in game, Max about to play
        depth (int): 

        Returns:
            int: best-score (for Max) available from state
        """
        cp_state = state

        # if state is a terminal state, return terminal value of state
        state_val = self.game_value(state)
        if state_val != 0:
            return state_val, cp_state
        
        if depth >= 3:
            return self.heuristic_game_value(state), cp_state
        
        else:
            alpha = float('-Inf')
            successors = self.succ(state, self.my_piece)
            for s in successors:
                temp = self.min_value(s, depth+1)
                if temp[0] > alpha:
                    alpha = temp[0]
                    cp_state = s
          
            return alpha, cp_state

    def min_value(self, state, depth):
        """
        Args:
        state (list of lists): current state in game, Min about to play
        depth (int): 

        Returns:
            int: best-score (for Min) available from state
        """
        cp_state = state

        # if state is a terminal state, return terminal value of state
        state_val = self.game_value(state)
        if state_val != 0:
            return state_val, cp_state
        
        if depth >= 3:
            return self.heuristic_game_value(state), cp_state
        
        else:
            beta = float('Inf')
            successors = self.succ(state, self.opp)
            for s in successors:
                temp = self.max_value(s, depth+1)
                if temp[0] < beta:
                    beta = temp[0]
                    cp_state = s
                    
            return beta, cp_state

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        #pivots = [[0,0], [0,1], [1, 0], [1,1]]
        for r in range(2):
            for c in range(2):
                if state[r][c] != ' ' and state[r][c] == state[r+1][c+1] == state[r+2][c+2] == state[r+3][c+3]:
                    return 1 if state[r][c]==self.my_piece else -1

        # TODO: check / diagonal wins
        #pivots = [[-1,0], [-1, 1], [-2,0], [-2,1]]
        for r in range(-2,0):
            for c in range(2):
                if state[r][c] != ' ' and state[r][c] == state[r-1][c+1] == state[r-2][c+2] == state[r-3][c+3]:
                    return 1 if state[r][c]==self.my_piece else -1
                
        # TODO: check box wins
        for r in range(4):
            for c in range(4):
                if state[r][c] != ' ' and state[r][c] == state[r][c+1] == state[r+1][c] == state[r+1][c+1]:
                    return 1 if state[r][c]==self.my_piece else -1

        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
