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

    def be_greedy(self):
        """ Change move_dict to be greedy according to v_dict
        Returns:
            True if any move has changed.
        """
        policy_has_changed = False
        for num in range(int('1' + '0' * 9, 3), int('2' * 10, 3) + 1):
            s = ttt_play.State(from_base10=num)
            if not s.is_terminal():
                afterstates = s.legal_afterstates()
                v_dict_slice = {
                    s: self.v_dict[s] for s in afterstates}
                old_move = self.move_dict[num]
                if s.turn == 1:
                    self.move_dict[num] = max(
                        v_dict_slice, key=v_dict_slice.get)
                else:
                    self.move_dict[num] = min(
                        v_dict_slice, key=v_dict_slice.get)
                if old_move != self.move_dict[num]:
                    policy_has_changed = True
        return policy_has_changed

    def print_progression(self, state):
          """ Print the progression of a game starting from state till the end,
              where both players follow this policy.
          """
          state.print_board()
          num = state.get_num()
          print("This state has value %f" % self.v_dict[num])
          if not state.is_terminal():
               afterstate = ttt_play.State(from_base10 = self.move_dict[num])
               self.print_progression(afterstate)
