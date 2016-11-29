from sudoku import basic # basic functions
from sudoku import data  # some sudoku's from solve book and internet
from sudoku import paths # analysis definition and brute-force method

SW_MASK = [1, 0] # whether to show board and shadow board in show(). default is [1, 0]. to see the result of any one method, switch it to [1, 1]. no report is [0, 0]
SW_BASIC_ANALYSIS = 0b11000  # five bytes to switch five methods on/off as a part of basic analysis. default is 0b11000 and 0b10000 is still reasonable (but tested as overally slower even when locally faster)
SW_FULL_ANALYSIS  = 0b11111  # five bytes to switch five methods on/off as a part of  full analysis. default is 0b11111 and 0b11110 is still reasonable
                             # methods are: NAKED_PAIRS, HIDDEN_COUPLES, NAKED_TRIPLES, HIDDEN_TRIPLES, INTERSECTION_REMOVAL

def solve(problem):
  # *** printing the final result(s) method
  def last_show(typ, data):
    if typ == 'normal': last_show_two(data)
    elif typ == 'special' and len(data) > 1:
      print(36* ' ' + 'MULTIPLE SOLUTIONS:')
      for i in range(len(data)):
        print(' --- solution no. ' + str(i+1))
        last_show_two(data.pop())
  def last_show_two(elem):
    board = gate.meth.new_board(elem)
    board = gate.meth.initial_reduce(board)
    board.show(SW_MASK); print(bs.validity_test(board))
    
  # *** the real start od program
  bs = basic.Manager()
  gate = paths.Manager(bs, SW_BASIC_ANALYSIS, SW_FULL_ANALYSIS) # instance of algorithms classes
  sudoku = gate.meth.new_board(problem) # load the board
  sudoku = gate.meth.initial_reduce(sudoku) # adjust the shadow mask properly
                                        # other methods from methods.py (naked pairs etc) can be called in this manner
  sudoku.show(SW_MASK)                  # show the task at hand
  sudoku = sudoku.write_singles()       # make the most primitive attempt to reduce the candidates
  sudoku = gate.full_analysis(sudoku)   # proper attempt to reduce candidates and solve the board
  res_sud = sudoku.get_board()          # output ought to be 9x9 matrix

  validity = bs.validity_test(sudoku); special_end = False # finds out the state of board
  if validity == 'unfinished board':    # if there is some job left
    result = gate.try_branches(sudoku)  # run the brute force method
    if   len(result) == 1: res_sud = result.pop() # if there is just one matrix as a possible solution, load it into the original board
    elif len(result) == 0: print("Something is wrong (Sheldon's personal seat is Penny-butted)")
    else: special_end = True            # triggering the 'alternative solutions' event
  if special_end:                       # alternative returning value
    last_show('special', result); return result
  else:                                 # casual returning value
    last_show('normal', res_sud); return res_sud
# *** the end
#
#
# for one in data.get_all_valid_sudokus(): solve(one) # this way i found the bug which is:
# BUG BUG BUG BUG BUG BUG BUG BUG BUG BUG BUG BUG:

SHOW_BUG = False # turns the bug presentation on/off
switch = True    # run the program and then change this switch and run it again to see the bug 

if SHOW_BUG:
  if switch:
    solve(data.problem); solve(data.problem2) # works right
  else:
    solve(data.problem2); solve(data.problem) # doesn't solve the second one
    
else: solve(data.problem)
  
# aditional info: in case of malfunction, program runs the try_branches() but it just don't find the solution. Funny message 16 lines up from here serves as a proof of that
