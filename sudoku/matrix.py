from copy import deepcopy

class Zweiboard:
  def __init__(self, matrix = [], shadow = []):
    self.board = [[0] * 9 for _ in range(9)] # array of integers as a board
    self.shadow = [['123456789'] * 9 for _ in range(9)] # array of strings as a list of candidates for every field in board
    if len(matrix): self.__load(matrix, shadow)
  
  def load(self, board, shadow = []):
    for i in range(81): self.board[i//9][i%9] = board[i//9][i%9]
    if len(shadow):
      for i in range(81): self.shadow[i//9][i%9] = shadow[i//9][i%9]
      
  def get_board(self): return deepcopy(self.board)
  def get_shadow(self): return deepcopy(self.shadow)
    
  def row(self, row): return self.board[row]
  def column(self, col): return [row[col] for row in self.board]
  def area(self, area):
    out = []
    for i in range(9):
      x = 3* (area//3) + i//3; y = 3* (area%3) + i%3
      out += [self.board[x][y]]
    return out
  
  
  # *** showing the board and/or shadow board
  def show(self, mask = [1, 0]): # default: show the board and skip the shadow board
    if mask[0]: # showing the board
      for row in self.board: print(8* ' ' + str(row).replace(',', '').replace('[', '').replace(']', '').replace('0', chr(183)))
      print(36* '_' + ' sum of candidates = ' + str(self.count_shadows()))
    if mask[1]: # showing shadow board
      for row in self.shadow:
        line = ''
        for cell in row: line += '%8s' % cell
        print(line)
        
  # *** sum of candidates (shadows) for all slots
  def count_shadows(self, trigger = True): # by default, count shadows. by alternative, count just number of fields with nonzero shadows
    count = 0
    for row in self.shadow:
      for string in row: count += len(string) if trigger else 1 if len(string) else 0
    return count

  # *** sum of yet unfilled slots
  def count_unknowns(self):
    count = 0
    for row in self.board:
      for slot in row:
        if not slot: count += 1
    return count

      
  # *** writes specific number into slot (and shadow to zero) and
  # *** removes number's candidates from row, column and area it belongs to
  def write(self, row, col, what):
    out = self.__class__(self.board, self.shadow)
    out.board[row][col] = what; out.shadow[row][col] = ''
    out = out.lighten('column', row, col, str(what))
    out = out.lighten('row'   , row, col, str(what))
    out = out.lighten('area'  , row, col, str(what))
    return out

  # *** removes given type of candidates (1-9) in given scale (row,column,area)
  def lighten(self, typ, row, col, mask, exceptions = []):
    out = self.__class__(self.board, self.shadow)
    for what in mask:
      if typ == 'slot':
        if not [row, col] in exceptions: out.shadow[row][col] = out.shadow[row][col].replace(what, '')
      if typ == 'row':
        for y in range(9):
          if not [row, y] in exceptions: out.shadow[row][y] = out.shadow[row][y].replace(what, '')
      if typ == 'column':
        for x in range(9):
          if not [x, col] in exceptions: out.shadow[x][col] = out.shadow[x][col].replace(what, '')
      if typ == 'area':
        for slot in range(9):
          x = 3* (row //3) + slot //3; y = 3* (col //3) + slot %3
          if not [x, y] in exceptions: out.shadow[x][y] = out.shadow[x][y].replace(what, '')
    return out    
  
  # *** writes all sure-candidates (fields with only one shadow) on board (note: methods.hidden_elements(1) solves the rest of them)
  def write_singles(self):
    export = self.__class__(self.board, self.shadow); again = True
    while(again):
      again = False         # if there is nothing to add to desk, end this loop
      for row in range(9):
        for col in range(9):
          if len(export.shadow[row][col]) == 1: # only one candidate for cell means sure-candidate
            again = True    # if we are filling a cell in sudoku, there is a chance another run will reval new one
            export = export.write(row, col, int(export.shadow[row][col])) # write the sure-candidate to board
    return export

  __load = load
  
class Zweiboard_cut():
  def __init__(self, b, s):
    self.bd = deepcopy(b); self.sh = deepcopy(s)
  
class Stack_of_boards: # class necessary for proper work of paths.try_branches()
  def __init__(self): self.stack = []
  def push(self, board, shadow):
    self.stack.append(Zweiboard_cut(board, shadow))
  def length(self): return len(self.stack)
  def pop(self):
    if self.length(): return self.stack.pop()      
    return []

