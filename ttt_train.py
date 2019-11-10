class Training:
     def __init__(self, n_game, read_path = None, write_path):
          """
          Input:
               n_game: number of games to train for
               read_path, write_path: paths for reading or saving the model
          """
          self.n_game = n_game
          self.write_path = write_path
          if read_path:
               self.read_path = read_path
          else:
               self.read_path = write_path