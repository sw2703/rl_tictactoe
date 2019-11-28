import ttt_play


class TabularPolicy():
    """ By default, a rush policy, i.e. selects the first available move.
    """

    def __init__(self):
        self.init_v_dict()
        self.init_move_dict()

    def init_v_dict(self):
        self.v_dict = dict()
        for num in range(int('1' + '0' * 9, 3), int('2' * 10, 3) + 1):
            self.v_dict[num] = 0

    def init_move_dict(self):
        self.move_dict = dict()
        for num in range(int('1' + '0' * 9, 3), int('2' * 10, 3) + 1):
            try:
                self.move_dict[num] = self.rush_move(num)
            except(RuntimeError):
                pass

    def rush_move(self, num_base10):
        state = ttt_play.State(from_base10=num_base10)
        for x in range(3):
            for y in range(3):
                if state.board[x][y] == 0:
                    state.board[x][y] = state.turn
                    state.change_turn()
                    return state.get_num()
        raise RuntimeError('Cannot make a move on a full board!')
