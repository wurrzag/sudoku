from constants import the_file as gg
from copy import deepcopy
from time import sleep

from . import colo

LINES = 24
LETTERS = 80

class Console:
  def __init__(self):
    self.O = [[' '] * LETTERS for _ in range(LINES)]
    self.C = [[gg.WHITE] * LETTERS for _ in range(LINES)]
    self.bac_O = [[' '] * LETTERS for _ in range(LINES)]
    self.bac_C = [[gg.WHITE] * LETTERS for _ in range(LINES)]
    self.__reset()
    return None
  
  # various - maintenance methods
  def reset(self):
    self.current_color = gg.WHITE
    self.changes = []
    self.chsorted = []
    for i in range(LINES): self.chsorted.append([])
    for x in range(LINES):
      for y in range(LETTERS): self.O[x][y], self.C[x][y] = ' ', gg.WHITE
    return True
  
  def save(self):
    for i in range(LINES):
      for j in range(LETTERS):
        self.bac_C = self.C
        self.bac_O = self.O
    return True

  def load(self):
    for i in range(LINES):
      for j in range(LETTERS):
        self.C = self.bac_C
        self.O = self.bac_O
    return True

  def resetcolor(self, color = gg.WHITE):
    clr = color
    for x in range(LINES):
      for y in range(LETTERS): self.C[x][y] = clr
    return True
    
  def setcolor(self, color = gg.NONECOLOR):
    if color == gg.NONECOLOR: return False
    else: self.current_color = color; return True
    print('\n\nsomething nasty in Terminal.setcolor\n')
    return False
    
  # various - sub methods of run()
  def set_eol_characters(self):
    for i in range(LINES):
      self.O[i][LETTERS -1] = '·'; self.C[i][LETTERS -1] = gg.GRAY
      self.O[i][0]          = '·'; self.C[i][0]          = gg.GRAY
    return True
  
  def scan_color_changes(self):
    for x in range(LINES):
      for y in range(LETTERS):
        if y:
          if self.C[x][y] != self.C[x][y-1]: self.changes += [[x, y, self.C[x][y]]]          
    return True
  
  def sort_color_changes(self):
    for ch in self.changes: self.chsorted[ch[0]].append([ch[1], ch[2]])
    return True  
  
  def bubblesort(self, line):
    l = [o for o in line]
    if len(l) < 2: return l
    change = True
    while change:
      change = False
      for i in range(len(line) -1):
        if l[i][0] < l[i+1][0]: a=l[i]; l[i]=l[i+1]; l[i+1] = a; change = True
    return l
        
  # run() - draw the whole screen
  def run(self, command = False, argument = False):
    pause = 0
    if type(command) == str and command == 'animation': pause = argument
    self.set_eol_characters(); self.scan_color_changes(); self.sort_color_changes()
    index = -1
    for line in self.O:
      index += 1; col = self.bubblesort(deepcopy(self.chsorted[index]))
      if not len(col): print(colo.r(gg.GRAY) +''.join(line))
      else:
        pos = 0; printline = colo.r(gg.GRAY)
        while len(col):
          p = col[-1]; col = col[:-1]
          #printline += '\033[40m' 
          printline += ''.join(line[pos:p[0]]) + colo.r(p[1])
          pos = p[0]
        printline += ''.join(line[pos:])
        print(printline)
    sleep(pause)    
    return True 
  # end of run()
    
  # load_object(): the only input method of this class. 'pattern' is array of strings
  def load_object(self, what_line_co_ord, what_letter_co_ord, pattern, color = gg.NONECOLOR):
    px, py, obj = what_line_co_ord, what_letter_co_ord, [o for o in pattern]
    if type(color) == str: clr = self.what_color(color)
    else: clr = self.current_color if color == gg.NONECOLOR else color
    
    index = -1
    for line in obj:
      index += 1
      for i in range(len(line)):
        x = px + index; y = py + i
        try:
          self.C[x][y] = clr
          self.O[x][y] = line[i]
        except IndexError: aaaaa=0
    return True
  
  # rshift(), lshift() - right, left scrolling (rotationally, by one pixel)
  def lsh(self):
    saveO, saveC = [], []
    for i in range(LINES): saveC.append(self.C[i][0]); saveO.append(self.O[i][0])
    for column in range(1, LETTERS):
      for row in range(LINES):
        self.O[row][column -1] = self.O[row][column]
        self.C[row][column -1] = self.C[row][column]
    for i in range(LINES): self.C[i][LETTERS -1], self.O[i][LETTERS -1] = saveC[i], saveO[i]
    return True
  
  def rsh(self):
    saveO, saveC = [], []
    for i in range(LINES): saveC.append(self.C[i][LETTERS -1]); saveO.append(self.O[i][LETTERS -1])
    for inv_column in range(LETTERS -1):
      column = LETTERS -1 -1 -inv_column
      for row in range(LINES):
        self.O[row][column +1] = self.O[row][column]
        self.C[row][column +1] = self.C[row][column]
    for i in range(LINES): self.C[i][0], self.O[i][0] = saveC[i], saveO[i]
    return True
  
  def rshift(self, pixels):
    arr = [[0] * pixels for _ in range(LINES)]
    col = [[0] * pixels for _ in range(LINES)]
    for x in range(LINES):
      for y in range(pixels):
        a = LETTERS - pixels
        arr[x][y] = self.O[x][y +a]
        col[x][y] = self.C[x][y +a]
    for i in range(LETTERS - pixels)[::-1]:
      for j in range(LINES):
        self.O[j][i +pixels] = self.O[j][i]
        self.C[j][i +pixels] = self.C[j][i]
    for x in range(LINES):
      for y in range(pixels):
        self.O[x][y] = arr[x][y]
        self.C[x][y] = col[x][y]
    return True
  
  def dshift(self, pixels):
    arr = [[0] * LETTERS for _ in range(pixels)]
    col = [[0] * LETTERS for _ in range(pixels)]
    for x in range(pixels):
      xx = LINES - pixels +x
      for y in range(LETTERS):
        arr[x][y] = self.O[xx][y]
        col[x][y] = self.C[xx][y]
    for i in range(LINES - pixels)[::-1]:
      for j in range(LETTERS):
        self.C[i +pixels][j] = self.C[i][j]
        self.O[i +pixels][j] = self.O[i][j]
    for x in range(pixels):
      for y in range(LETTERS):
        self.O[x][y] = arr[x][y]
        self.C[x][y] = col[x][y]
    return True
    
   
  # what_color() - translate the letter code to color code
  def what_color(self, a):
    if a == 'w': return gg.WHITE
    if a == 'x': return gg.GRAY
    if a == 'r': return gg.RED
    if a == 'g': return gg.GREEN
    if a == 'y': return gg.YELLOW
    if a == 'b': return gg.BLUE
    if a == 'v': return gg.VIOLET
    if a == 'l': return gg.LBLUE
    if a == 'R': return gg.bgRED
    if a == 'G': return gg.bgGREEN
    if a == 'Y': return gg.bgYELLOW
    if a == 'B': return gg.bgBLUE
    if a == 'V': return gg.bgVIOLET
    if a == 'L': return gg.bgLBLUE
    if a == 'X': return gg.bgGRAY
    if a == '.' or a == ' ': return gg.NONECOLOR
    print('\n\nParser.what_color(): wrong color:',a,';\n')
    return False  
 
  # clean() - destructor
  def clean(self):
    del self.current_color
    del self.changes
    del self.chsorted
    del self.O
    del self.C
    return True
    
  __reset = reset
  write = load_object
# end of class Console
    
