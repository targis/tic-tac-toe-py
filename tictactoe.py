# MVC

# model
class Player:
    def __init__(self, name, sign):
        self.name = name
        self.sign = sign

    def get_sign(self):
        return self.sign

    def get_name(self):
        return self.name


class Board:
    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    def __init__(self):
        self.cells = None
        self.clear()

    def get_cells(self):
        return self.cells[:]

    def get_empty_cells_idxs(self):
        return tuple(i for i, cell in enumerate(self.cells) if not cell)

    def set_cell(self, idx, value):
        self.cells[idx] = value

    def no_more_empty_cells(self):
        return '' not in self.cells

    def is_win_combination_filled_with(self, sign):
        # for wc in Board.win_combinations:
        #     if all(self.cells[i] == sign for i in wc):
        #         return True
        # return False
        return any(all(self.cells[i] == sign for i in wc)
                   for wc in Board.win_combinations)

    def clear(self):
        self.cells = [''] * 9


# view
class View:
    EMPTY = '\u2219'

    def game_started(self):
        print('-' * 19)
        print('|   TIC TAC TOE   |')
        print('-' * 19)

    def get_player_name(self, number):
        return input(f'input player #{number} name: ')

    def show_board(self, cells):
        for i in 0, 3, 6:
            print(' '.join(c if c else View.EMPTY for c in cells[i:i + 3]))

    def get_player_move(self, name, empty_cells_idsx):
        while True:
            inj = ', '.join(str(eci) for eci in empty_cells_idsx)
            move = input(f'{name}, your move ({inj}): ')
            if not move.isdigit():
                print('must be a number')
                continue
            move = int(move)
            if move not in empty_cells_idsx:
                print('wrong value')
                continue
            return move

    def no_more_moves(self):
        print('no more moves left')

    def show_winner(self, name):
        print(f'player {name} is a winner!')

    def one_more_game(self):
        return input('one more game? (yes/no)').lower == 'yes'

    def game_over(self):
        print('-' * 17)
        print('|   Game over   |')
        print('-' * 17)


# controller
class Game:
    def __init__(self):
        self.view = View()
        self.board = Board()
        self.player1 = None
        self.player2 = None

    def create_players(self):
        name1 = self.view.get_player_name(number=1)
        name2 = self.view.get_player_name(number=2)
        self.player1 = Player(name=name1, sign='\u00D7')
        self.player2 = Player(name=name2, sign='\u25EF')

    def gameplay(self):
        self.view.show_board(cells=self.board.get_cells())
        current_player = self.player1
        while True:
            move = self.view.get_player_move(
                name=current_player.get_name(),
                empty_cells_idsx=self.board.get_empty_cells_idxs()
            )
            self.board.set_cell(
                idx=move,
                value=current_player.get_sign()
            )
            self.view.show_board(cells=self.board.get_cells())
            if self.board.no_more_empty_cells():
                self.view.no_more_moves()
                break
            if self.board.is_win_combination_filled_with(sign=current_player.get_sign()):
                self.view.show_winner(name=current_player.get_name())
                break
            current_player = self.player2 if current_player \
                                             == self.player1 else self.player1

    def start(self):
        self.view.game_started()
        self.create_players()
        while True:
            self.gameplay()
            if not self.view.one_more_game():
                break
            self.board.clear()
        self.view.game_over()


if __name__ == '__main__':
    game = Game()
    game.start()
