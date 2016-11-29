from constants import the_file as gg
from random import randint

# Help: help class of Screen
class Help:
  def __init__(self):
    return None
  # end of __init__()
  
  def random(self, m, n, how_many_throws = 0):
    if not how_many_throws: return randint(m, n)
    result = []
    for i in range(how_many_throws): result.append(randint(m, n))
    return result
    
  # what_color(), self.colorchar(): translate char sign to color code or back
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
    if a == ' ': return gg.NONECOLOR
    print("\n\nscreen.what_color(): wrong color: " + str(a) +'\n')
    return False

  # colorchar(): returns the propper letter for Screen's parsing method
  def colorchar(self, color):
    if color == gg.WHITE:   return 'w'
    if color == gg.GRAY:    return 'x'
    if color == gg.RED:     return 'r'
    if color == gg.GREEN:   return 'g'
    if color == gg.YELLOW:  return 'y'
    if color == gg.BLUE:    return 'b'
    if color == gg.VIOLET:  return 'v'
    if color == gg.LBLUE:   return 'l'
    if color == gg.bgRED:   return 'R'
    if color == gg.bgGREEN: return 'G'
    if color == gg.bgYELLOW:return 'Y'
    if color == gg.bgBLUE:  return 'B'
    if color == gg.bgVIOLET:return 'V'
    if color == gg.bgLBLUE: return 'L'
    if color == gg.bgGRAY:  return 'G'
    if color == gg.bgWHITE: return 'W'
    if color == gg.NONECOLOR: return ' '
    print('\n\nscreen.colorchar(): something is wrong ---', str(color) +'\n')
    return False
  # end of colorchar()

  # invert_color(): the definition of what inverted color means
  def invert_color(self, color):
    if color == gg.WHITE:   return gg.bgGRAY
    if color == gg.GRAY:    return gg.bgGRAY
    if color == gg.RED:     return gg.bgRED
    if color == gg.GREEN:   return gg.bgGREEN
    if color == gg.YELLOW:  return gg.bgYELLOW
    if color == gg.BLUE:    return gg.bgBLUE
    if color == gg.VIOLET:  return gg.bgVIOLET
    if color == gg.LBLUE:   return gg.bgLBLUE
    print('\n\nscreen.invert_color(): wrong color', str(color) +'\n')
    return False

  # get_the_dimmer_version_of(): definition of what 'dimmer shade' of color means
  def get_the_dimmer_version_of(self, color):
    if color == gg.WHITE:   return gg.VIOLET
    if color == gg.GRAY:    return gg.VIOLET
    if color == gg.RED:     return gg.YELLOW
    if color == gg.GREEN:   return gg.YELLOW
    if color == gg.YELLOW:  return gg.GREEN
    if color == gg.BLUE:    return gg.VIOLET
    if color == gg.VIOLET:  return gg.BLUE
    if color == gg.LBLUE:   return gg.BLUE
    return False

  '''
  def draw_table(self):
    for i in range(3):
      for j in range(4):
        self.draw(i*8 +2, j*20 +3, 'boxfat 0313', 'w')
        if i == 1 and j != 0: self.draw(i*8 +3, j*20 +2, 'arrow-l 05', 'w')
        if i == 2 and j == 2: self.draw(i*8 +3, j*20 +2, 'arrow-l 05', 'w')
        if i == 0 and j == 2: self.draw(i*8 +3, j*20 -3, 'arrow-r 05', 'w')
        if i == 2 and j < 2: self.draw(i*8 +2, j*20 +9, 'arrow-u 05', 'w')
        if i == 0 and j == 2: self.draw(i*8 +5, j*20 +9, 'arrow-d 05', 'w')
    return True
  '''

  # cut_numbers_from_string(): returns the string without all numerical values
  def cut_numbers_from_string(self, string):
    ret = ''
    for one in string:
      if not one.isdigit(): ret += one
    return ret
  
  # translate the manacost value to reasonable text
  def translate_skill_manacost(self, text):
    arr = text.replace(' ', '').replace('+', '').split(',')
    out = ''
    for a in arr:
      if a[1:] == 'red': out += a[0]+ '_red_mana '
      if a[1:] == 'gre': out += a[0]+ '_green_mana '
      if a[1:] == 'blu': out += a[0]+ '_blue_mana '
      if a[1:] == 'bla': out += a[0]+ '_black_mana '
      if a[1:] == 'whi': out += a[0]+ '_white_mana '
      if a[1:] == 'non': out += a[0]+ '_colorless_mana '
      if a[1:] in ('tap', 'ap'): out += 'spend_all movement'
    return out


# justify(): reformat and allign text string to format readable by Terminal()
  def justify(self, text, width):
    def justif(text, width):
      text += ' ';
      line = ""; num_spaces = 0; word = ''; start = True; output = ""
      for letter in text:
        if letter != ' ': word += letter
        else:
          if len(line) + len(word) + 1 > width:
            if start: start = False
            else: output += '\n'
            if not num_spaces: output += line
            else:
              count = 0; freespace = width - len(line)
              for i in line:
                output += i
                if i == ' ':
                  output += (freespace // num_spaces) * ' '
                  if count < freespace % num_spaces: output += ' '
                  count += 1
            line = word; word = ''; num_spaces = 0
          else: 
            if len(line): line += ' '; num_spaces += 1
            line += word; word = ''
      output += '\n'; output += line
      return output
    
    def format_text_to_array(text):
      t, o = text +'\n' , []; n = t.count('\n')
      for i in range(n):
        #a = 1 if i == n -1 else 0
        o.append(t[:t.find('\n')]); t = t[t.find('\n') +1:]
      return o
    return format_text_to_array(justif(text, width))
  # end of justify()
  
  # insert_empty_lines(): puts an empty lines in between justified text
  def insert_empty_lines(self, text, n):
    txt = []
    for t in text:
      txt.append(t)
      for i in range(n): txt.append('')
    return txt
  
  
  # clean(): destructor
  def clean(self):
    return True
# end of class Help
