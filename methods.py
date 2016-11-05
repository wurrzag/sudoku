from .matrix import Zweiboard  # class for sudoku (double) board

# five constants used in Manager.all_methods() to determine which specific methods to run
NAKED_PAIRS          = 0b10000 # very fast method
HIDDEN_COUPLES       = 0b01000 # somewhat fast method
NAKED_TRIPLES        = 0b00100 # slow method
HIDDEN_TRIPLES       = 0b00010 # slow method
INTERSECTION_REMOVAL = 0b00001 # slow method

class Manager:
  def __init__(self, basic_py_instance):
    self.bs = basic_py_instance
    
  # *** tranzit method (sudoku.py <--> matrix.py)
  def new_board(self, arr):
    return Zweiboard(arr)

  # *** initial setting of shadows after loading new desk
  def initial_reduce(self, imp):
    out = Zweiboard(imp.board, imp.shadow)
    for row in range(9): # within the whole board...
      for col in range(9):
        if out.board[row][col]:
          out = out.write(row, col, out.board[row][col]) # write down all numbers, which are really written there because write() removes also candidates (shadows) accordingly
    return out    
          
  # *** main loop called from basic_analysis() and full_analysis() (in paths.py)
  def all_methods(self, imp, switch = 0b11111):
    exp = Zweiboard(imp.board, imp.shadow); start = 9**9
    if switch & NAKED_PAIRS:    exp = self.naked_pairs(exp)
    if switch & HIDDEN_COUPLES: exp = self.hidden_elements(exp, 1); exp = self.hidden_elements(exp, 2)
    if switch & NAKED_TRIPLES:  exp = self.naked_triples(exp)
    if switch & HIDDEN_TRIPLES: exp = self.hidden_elements(exp, 3)
    if switch & INTERSECTION_REMOVAL: exp = self.intersection_removal(exp)
    if switch & NAKED_PAIRS: # naked pairs are way-faster than other methods (as being the only one which doesn't manually check all rows, columns and areas for some conditions), so it can run couple more times by the end of full analysis
      while(start > exp.count_shadows()): # with "couple more times" meaning "until completely unefficient"
        start = exp.count_shadows(); exp = self.naked_pairs(exp)   
    return exp

  
  # ********************************************************************
  # *******************      ANALYSIS METHODS      *********************
  # ********************************************************************

  # ********************************************************************
  # **********************************
  # *** naked pairs
  def naked_pairs(self, imp):
    out = Zweiboard(imp.board, imp.shadow)
    pairs = []
    for row in range(9):             # search the board...
      for col in range(9):
        if len(out.shadow[row][col]) == 2: # if given field have exactly 2 shadows, add it to list of such fields (pairs[])
          is_new = True                    
          for pair in pairs:
            if out.shadow[row][col] == pair[0]: is_new = False; pair += [[row, col]] # if this specific 2-letter shadow is already on the list, add new [coordinates] there
          if is_new: pairs += [[out.shadow[row][col], [row, col]]] # or else add [shadow, coordinates] to list    
    
    for pair in pairs:     # for every len==2 shadow in board
      if len(pair) >= 3:   # if it is there at least 2 times (2 fields in board)
        u_comb = self.bs.make_unique_groups(pair[1:], 2)  # make list of unique couples amongst all coordinates with this combination
        for com in u_comb:
          # check every unique couple whether it shares row, column or area and act accordingly if so
          if self.bs.is_same_area  (com[0], com[1]): out = out.lighten('area'  , com[0][0], com[0][1], pair[0], pair[1:])
          if self.bs.is_same_row   (com[0], com[1]): out = out.lighten('row'   , com[0][0], com[0][1], pair[0], pair[1:])
          if self.bs.is_same_column(com[0], com[1]): out = out.lighten('column', com[0][0], com[0][1], pair[0], pair[1:])
          
    return out.write_singles()


  # ********************************************************************
  # **********************************
  # *** hidden couples, triples, quads
  def hidden_elements(self, imp, how_many):
    out = Zweiboard(imp.board, imp.shadow)
    u_comb = self.bs.make_unique_groups([1, 2, 3, 4, 5, 6, 7, 8, 9], how_many)
    for group in u_comb:     # run the test for every possible n-combination of numbers 1-9
      for where in range(9): # and for row, column and area 1-9
        
        if not self.bs.is_there(group, out.row(where)): # if none of the numbers from given combination is present in given row
          match = []; index = 0
          for slot in out.row(where):   # for every single field in given row
            if self.bs.is_there(group, out.shadow[where][index]):  # if any one number from combination is present
              match += [[where, index]] # add that field to the list
            index += 1
          if len(match) == how_many: # if there is same amount of numbers and fields into which any of them can fit
            for m in match: out = out.lighten('slot', m[0], m[1], self.bs.neg(self.bs.to_str(group))) # remove all other candidates from those fields

        if not self.bs.is_there(group, out.column(where)):
          match = []; index = 0
          for slot in out.column(where): # for every single field in given column
            if self.bs.is_there(group, out.shadow[index][where]):
              match += [[index, where]]
            index += 1
          if len(match) == how_many:
            for m in match: out = out.lighten('slot', m[0], m[1], self.bs.neg(self.bs.to_str(group)))

        if not self.bs.is_there(group, out.area(where)):
          match = []; index = 0
          for slot in out.area(where):   # for every single field in given area
            x = 3* (where //3) + index //3; y = 3* (where %3) + index %3
            if self.bs.is_there(group, out.shadow[x][y]):
              match += [[x, y]]
            index += 1
          if len(match) == how_many:
            for m in match: out = out.lighten('slot', m[0], m[1], self.bs.neg(self.bs.to_str(group)))
    
    return out.write_singles()
  

  # ********************************************************************
  # **********************************
  # *** naked triples
  def naked_triples(self, imp):
    out = Zweiboard(imp.board, imp.shadow)
    u_comb = self.bs.make_unique_groups([1, 2, 3, 4, 5, 6, 7, 8, 9], 3) # make every posible unique triple from 1-9
    for group in u_comb:     # and run the rest for each of them
      for scale in range(9): # for rows 1-9, columns 1-9 and areas 1-9
      
        # rows
        if not self.bs.is_there(group, out.row(scale)): # run the test only if none of the numbers is presented in given row (column,area)
          match = []
          for column in range(9):               # for (shadow of) each field in given row
            if self.bs.is_this_group_only(out.shadow[scale][column], group): match += [[scale, column]] # if that field fits the proper condition, ad it's coords to the list
          if len(match) == 3:                   # if there are just three such equals                 
            out = out.lighten('row', scale, 0, self.bs.to_str(group), match) # we can remove given candidates from rest of row (column, area)
          
        # columns    
        if not self.bs.is_there(group, out.column(scale)):
          match = []
          for row in range(9):
            if self.bs.is_this_group_only(out.shadow[row][scale], group): match += [[row, scale]]
          if len(match) == 3:
            out = out.lighten('column', 0, scale, self.bs.to_str(group), match)
          
        # areas    
        if not self.bs.is_there(group, out.area(scale)):
          match = []
          for slot in range(9):
            x = 3* (scale //3) + slot //3; y = 3* (scale %3) + slot %3
            if self.bs.is_this_group_only(out.shadow[x][y], group): match += [[x, y]]
          if len(match) == 3:
            out = out.lighten('area', x, y, self.bs.to_str(group), match)
            
    return out.write_singles()


# ********************************************************************
# **********************************
# *** pointing pairs &triples + box line reduction            
  def intersection_removal(self, imp):
    out = Zweiboard(imp.board, imp.shadow)
    for number in range(1, 10): # for every number between 1-9
      for scale in range(9):    # check that number against 9 rows, 9 columns and 9 areas
      
        # row - check          
        match = []; check = [0, 0, 0] # list of proper fields and (3x 0/1 switch of) their allegiance to 1,2,3th third of given row
        for column in range(9):
          if str(number) in out.shadow[scale][column]: match += [[scale, column]]; check[column // 3] = 1 # if candidate is presented in this shadow, make entry about that
        if len(match) == 1: out = out.write(match[0][0], match[0][1], number) # we can write the number directly if it have shadow in only one field of row
        elif len(match) == 2 or len(match) == 3:         # if it have candidates in 2-3 fields
          mask = 100* check[0] + 10* check[1] + check[2] # create a mask of 1/2/3th third of the row
          if mask == 1 or mask == 10 or mask == 100:     # if all fields are in the same third
            out = out.lighten('area', match[0][0], match[0][1], str(number), match) # remove shadow of that number from the rest of given area ('match' serves as list of exvceptions)
          
        # column - check
        match = []; check = [0, 0, 0]
        for row in range(9):
          if str(number) in out.shadow[row][scale]: match += [[row, scale]]; check[row // 3] = 1
        if len(match) == 1: out = out.write(match[0][0], match[0][1], number)
        elif len(match) == 2 or len(match) == 3:
          mask = 100* check[0] + 10* check[1] + check[2] # create a mask of 1/2/3th third of the column
          if mask == 1 or mask == 10 or mask == 100:
            out = out.lighten('area', match[0][0], match[0][1], str(number), match)
          
        # area - horizontal - check
        match = []; check_row = [0, 0, 0]; check_column = [0, 0, 0]
        for slot in range(9):
          x = 3* (scale//3) + slot//3; y = 3* (scale%3) + slot%3
          if str(number) in out.shadow[x][y]:
            match += [[x, y]]; check_row[slot //3] = 1; check_column[slot %3] = 1 # two masks for horizontal AND vertical thirds of area
        if len(match) == 1: out = out.write(match[0][0], match[0][1], number)
        elif len(match) == 2 or len(match) == 3:
          mask = 100* check_row[0] + 10* check_row[1] + check_row[2] # create a mask of 1/2/3th row of the area
          if mask == 1 or mask == 10 or mask == 100:     # and clean whole row if there is just one row with occurence
            out = out.lighten('row', match[0][0], match[0][1], str(number), match)
          mask = 100* check_column[0] + 10* check_column[1] + check_column[2] # create a mask of 1/2/3th column of the area
          if mask == 1 or mask == 10 or mask == 100:     # and clean whole column if there is just one column with occurence
            out = out.lighten('column', match[0][0], match[0][1], str(number), match)
      
    return out.write_singles()
