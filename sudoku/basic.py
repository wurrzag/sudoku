class Manager:

  # *** converts string to '1-9' minus string
  def neg(self, st):
    key = '123456789'
    for s in st: key = key.replace(str(s), '')
    return key

  # *** converts array of integers to string
  def to_str(self, arr, ch = ''):
    for pirate in arr: ch += str(pirate)
    return ch

  # *** takes list of integers as 'what'
  # *** returns whether ANY of them is within 'in_what', which may be array of ints or string
  def is_there(self, what, in_what):
    if type(in_what) == str:
      for w in what:
        if str(w) in in_what: return True
    else:
      for w in what:
        if w in in_what: return True
    return False

  # *** returns whether two couples of coordinates shares row, column or area  
  def is_same_row(self, a, b): return True if a[0] == b[0] else False
  def is_same_column(self, a, b): return True if a[1] == b[1] else False
  def is_same_area(self, a, b): return True if a[0]//3 == b[0]//3 and a[1]//3 == b[1]//3 else False
   
  # *** returns True if given shadow consists from AT LEAST ONE number from 'group'
  # *** and at the same time NONE of the other numbers   
  def is_this_group_only(self, one_shadow, group, sign = False):  
    for number in group:
      if str(number) in one_shadow:
        sign = True; break
    if not sign: return False
    for absent_number in self.neg(self.to_str((group))):
      if absent_number in one_shadow: 
        return False
    return True    


  # *** validity test for board being not correct, not finished or finished properly
  def validity_test(self, game):
    k = game.count_shadows(False); l = game.count_unknowns() # number of fields with nonzero shadow and number of yet-unfilled fields
    return 'wrong board' if k != l else 'unfinished board' if l else self.is_board_solved_properly(game)
  # *** is sudoku properly done due the rules?
  def is_board_solved_properly(self, game):
    for key in range(1, 10):
      for i in range (9):
        if not(self.is_there([key], game.row(i)) and self.is_there([key], game.column(i)) and self.is_there([key], game.area(i))): return 'wrong board'
    return 'properly finished board'

  
  
# *** ******************** CUT'N'PASTE FROM NET ****************************
# ***                                                                    ***
# *** finds unique n-combinations (couples, triples, ...) of group       ***
  def make_unique_groups(self, group, n):
    ucomb = []
    for uc in self.xuniqueCombinations(group, n): ucomb += [uc]
    return ucomb
  
  def xuniqueCombinations(self, items, n):
    if n==0: yield []
    else:
        for i in range(len(items)):
            for cc in self.xuniqueCombinations(items[i+1:],n-1):
                yield [items[i]]+cc