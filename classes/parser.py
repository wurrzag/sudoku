from constants import the_file as gg
from random import randint

# Parser: nearly all the 'robotic processes' are defined here; single-instance main worker of a program available virtually everywhere
class Parser:
  def __init__(self):
    self.method = 'none'    # what method to execute
    self._initialise()
    return None

  # initialise(): all walk-throughs of battlefield ought to be known from beginning    
  def initialise(self):
    self.define_all_paths()
    return True
    
  def set_method(self, which): self.method = which; return True
  
  #e(): the 'run' method of this class # executes the chosen method
  def e(self, command, one_method = 'none'):
    def get_param(inputstring, Nth):
      st = inputstring
      for i in range(Nth): st = st[st.find(' ') +1:]
      return st[:st.find(' ')] if ' ' in st else st
  
    meth = self.method if one_method == 'none' else one_method
    params = command
    if meth == 'get screen exits': return self.get_screen_exits(params)
    if meth == 'char -> keyboard command': return self.what_key(params)
    #if meth == 'key code -> string': return self.params_to_string(params)
    #if meth == 'justify': return self.justify(get_param(params, 0), int(get_param(params, 1)))
    #if meth == 'int -> screen command': return self.coords_to_parsable_line(int(get_param(params, 0)), int(get_param(params, 1)), get_param(params, 2), get_param(params, 3))
    if meth == 'equip abilities to array of strings': return self.equip_string(params)
    print('\n\ncl_gm.Parser.e(): not valid method:{' +meth+ '}\n')
    return False
  # end of e()
  
  
  
  # get_screen_exits(): most important method for the whole (screens-changing) system
  # get_screen_exits(): for every screen(room), this is list of it's exits, ie where the program should continue next if given keyboard key is pressed
  #
  # gg.KEY1: Q or U or 1 or 7
  # gg.KEY2: E or O or 2 or 8
  # gg.KEY3: F or ; or 3 or 9
  # gg.ENTE: Enter or Space. usually the same function as gg.KEY1
  # gg.HELP: H or ? or /
  # gg.ESC : All function keys (code 27) at the moment but should be BackSpace in final version
  # gg.ALL : overrides all previous settings; default exit, executed after ANY keypress
  # gg.DONT_PAUSE: don't haggle with these please; in a way, it is system switch marking all special (invisible) rooms
  # gg.UP,DOWN,LEFT,RIGH(arrows): W S A D or I K J L ; the are never listed as one of the exits as they never ALWAYS change the room but they CAN be used that manner
  def get_screen_exits(self, key):
    if key == '___Start': exits = {gg.ALL: '___Game'}
    if key == '___Game':  exits = {gg.ENTE: '___Deckmaking', gg.KEY3: 'Switch_bf_view', gg.ESC: '___Quit'}
    if key == '___Fight': exits = {gg.ALL: '___Other_player_turn', gg.DONT_PAUSE: True}
    if key == '___Other_player_turn': exits = {gg.ALL: '___Game'}
    if key == '___Deckmaking': exits = {gg.ALL: '___Game', gg.DONT_PAUSE: True}
    if key == '___Info_screen': exits = {gg.ESC: '___Quit', gg.KEY1: '___Game', gg.ALL: '___Game'}
    if key == '___Message_log': exits = {gg.ESC: '___Quit', gg.KEY1: '___Game', gg.ALL: '___Game'}
    if key == '___Quit': exits = {gg.ALL: '___Quit_for_real'}
    if key == '___Hand_right': exits = {gg.KEY3: '___Game', gg.KEY2: '__Hand_right_buildings', gg.ESC: '___Game'}
    if key == '___Hand_left' : exits = {gg.KEY3: '___Game', gg.KEY2: '__Hand_left_buildings' , gg.ESC: '___Game'}
    if key ==  '__Hand_right_buildings': exits = {gg.KEY3: '___Game', gg.KEY2: '__Hand_right_landsearch', gg.ESC: '___Game'}
    if key ==  '__Hand_left_buildings' : exits = {gg.KEY3: '___Game', gg.KEY2: '__Hand_left_landsearch' , gg.ESC: '___Game'}
    if key ==  '__Hand_right_landsearch': exits = {gg.KEY3: '___Game', gg.KEY2: '___Hand_right', gg.ESC: '___Game'}
    if key ==  '__Hand_left_landsearch' : exits = {gg.KEY3: '___Game', gg.KEY2: '___Hand_left' , gg.ESC: '___Game'}
    
    #if key == 'Movement': exits = {gg.ALL: '___Game', gg.DONT_PAUSE: True}
    if key == 'invitation': exits = {gg.ALL: '<--'}
    if key == 'ridiculous': exits = {gg.ALL: '<--'}
    if key == 'no_visible_units': exits = {gg.ALL: '<--'}
    if key == 'allgangTablEscreen': exits = {gg.ALL: '<--', gg.DONT_PAUSE: True}
    if key == 'table': exits = {gg.ALL: '<--', gg.DONT_PAUSE: True}
    if key == 'table_shifted': exits = {gg.ALL: '<--', gg.DONT_PAUSE: True}
    if key == 'command_the_gang': exits = {gg.ALL: '<--', gg.DONT_PAUSE: True}
    if key == 'spellcasting': exits = {gg.ALL: '<--', gg.DONT_PAUSE: True}
    if key == 'Switch_bf_view': exits = {gg.ALL: '___Game', gg.DONT_PAUSE: True}
    if key == '___Quit_for_real': exits = {gg.DONT_PAUSE: True, gg.ALL: '<--'}
    try: return exits
    except UnboundLocalError: print('\n\n\nParser.get_screen_exits(): wrong key: {' +key+ '}\n\n\n'); gg.getch()
    return False
  # end of get_screen_exits()
  
  # what_key(): all the keyboard configuration is defined by this method
  def what_key(self, a):
    if a == 'A': return gg.UP
    if a == 'B': return gg.DOWN
    if a == 'C': return gg.RIGH
    if a == 'D': return gg.LEFT
  
    if a.isalnum():
      if a.isalpha(): a = a.lower()
      if a == 'w': return gg.UP
      if a == 's': return gg.DOWN
      if a == 'a': return gg.LEFT
      if a == 'd': return gg.RIGH
      if a == 'q': return gg.KEY1
      if a == 'e': return gg.KEY2
      if a == 'f': return gg.KEY3
      if a == '1': return gg.KEY1
      if a == '2': return gg.KEY2
      if a == '3': return gg.KEY3
    
      if a == 'i': return gg.UP
      if a == 'k': return gg.DOWN
      if a == 'j': return gg.LEFT
      if a == 'l': return gg.RIGH
      if a == 'u': return gg.KEY1
      if a == 'o': return gg.KEY2
      #if a == ';': return gg.KEY3 # is not alnum
      if a == '7': return gg.KEY1
      if a == '8': return gg.KEY2
      if a == '9': return gg.KEY3

      if a == 'h': return gg.HELP
      if a == 'z': return gg.SEL
      if a == 'x': return gg.SEL
      if a == 'c': return gg.SEL
      if a == 'v': return gg.SEL
      if a == 'b': return gg.SEL
      if a == 'n': return gg.SEL
      if a == 'm': return gg.SEL
    
    else: # if a.isalnum()
      o = ord(a)
      if o == 13: return gg.ENTE
      if o == 32: return gg.ENTE
      if o == 27: return gg.ESC
      if o == 127: return gg.BACK
      if o == ord(';'): return gg.KEY3
      if o == ord('?'): return gg.HELP
      if o == 3: return gg.CT_C
      if o == 4: return gg.CT_C
    return gg.NONE
  # end of what_key()
  
  # equip_string(): returns what should be displayed as a description of some shield/sword effect
  def equip_string(self, string):
    def spaceit(numbers):
      ret, num = '', numbers
      for n in num: ret += n + '-'
      return ' '+ ret[:-1]
    
    ret, strr, count = [], [o for o in string], 0
    for line in strr:
      style = False if ';' in line or ('}' in line and line.index('}') - line.index('{') >2) else True
      if '}' in line: count += 1
    if count >1: style = False
    
    for line in strr:
      if ';' in line:
        area_of_effect, rest, temp, numbers = line[1], '', line[3:], ''
        for t in temp:
          if t.isdigit(): numbers += t
          else: rest += t
        addup = spaceit(numbers) if len(numbers) else ''
        switch = True if area_of_effect.isupper() else False
        if area_of_effect != 'o': ret.append(self.translate_area_of_effect(area_of_effect))
        ret.append(rest + addup + ':')
        with open('./data/abilities') as abi:
          for a in abi:
            if rest == a[:a.find(' ')]:
              jus = self.justify(a[a.find(' ') +1:], 17)
        for j in jus: ret.append('  ' + j)
        if switch: ret.append('(end of combat)')
       
      elif '{' in line:
        d = 'gain ability:' if line[0].isupper() else 'loose ability:'
        ret.append(d)
        lllisstt = ''
        for letter in line[line.index('{') +1 : line.index('}')]:
          lllisstt += self.get_ability_string(letter) + ' '
        jus = self.justify(lllisstt[:-1].strip(), 17)
        for j in jus: ret.append(j)
        
      else:
        sign = '+' if line[0].isupper() else '-'
        if line[0].lower() == 'h': sign = ''
        ret.append(self.translate_stat(line[0]) + ' ' + sign + str(self.letter_to_value(line[1])))
      
      if style: 
        dull = [o for o in ret]
        ret = []
        for d in dull:
          if len(d.strip()): ret.append(d)
        ret = self.insert_empty_lines(ret, 1)
      
    #print(ret); gg.getch()
    return ret
  # end of equip_string()

  # translate_turn(): translate who's on turn into text word recognisible by Gang_list
  def translate_turn(self, turn, neg = False):
    if neg == False:
      if turn == gg.HOME: return 'home'
      if turn == gg.AWAY: return 'away'
    else:
      if turn == gg.HOME: return 'away'
      if turn == gg.AWAY: return 'home'
    return 'none'

  # translate_area_of_effect(): very similar to equip_string()
  def translate_area_of_effect(self, area_of):
    area = area_of
    if area == 'a': return 'on self-'
    if area == 'b': return 'chosen friend-'
    if area == 'c': return 'all sector friends-'
    if area == 'x': return 'on engaged enemy-'
    if area == 'y': return 'chosen enemy-'
    if area == 'z': return 'all sector enemies-'
    return False
  
  # translate_stat(): another one
  def translate_stat(self, char):
    c = char
    if c == 'h': return 'damage'
    elif c == 'H': return 'heal'
    else:
      c = c.lower()
      if c == 'a': return 'attack'
      if c == 'd': return 'defense'
      if c == 's': return 'shooting'
      if c == 'm': return 'movement'
      if c == 'l': return 'life'
    return False
    
  # letter_to_value(): translate the letter from data/cards file into a real value
  def letter_to_value(self, letter):
    l = letter
    if l.isdigit(): return int(l)
    if l.islower(): return ord(l) - ord('a') +10
    if l.isupper(): return ord(l) - ord('A') +20
    return False

  # move_one_turn(): sub method of count_movement_coeficient(); simulates how far is Gang able to go within one turn
  def move_one_turn(self, entry_path, movement_value, creature_color, movement_type = 'normal'):
    field, path, move, color, typ = -1, entry_path, movement_value, creature_color, movement_type
    if move <= 0: return path[0]
    else: path = path[1:]
    free_movement_type = []
    if typ == 'forestwalk': free_movement_type = [0, 1, 2]
    if typ == 'swampwalk' : free_movement_type = [3, 4, 5]
    if typ == 'plainswalk': free_movement_type = [6, 7, 8]
    while(move > 0 and len(path)):
      f = path[0]; path = path[1:]
      if f in free_movement_type: free_movement_type = []
      elif typ == 'flying': move -= 1
      else:
        if f in (0, 1, 2):
          if color in ('red', 'green'): move -= 1
          else: move -= 3
        elif f in (3, 4, 5):
          if color in ('blue','black'): move -= 1
          else: move -= 2
        else: move -= 1
      #print('           field, moveleft: '+ str(f) +' '+  str(move))
    #print  ('result >>> field, moveleft: '+ str(f) +' '+  str(move) + '\n')

    if move < 0: move = 0
    return [f, move]
  # end of move_one_turn()

  # count_movement_coeficient(): sub method of find_path(); counts how many enemies there are on the way
  def count_movement_coeficient(self, fields_accessibility_mask, entry_path, movement_value, creature_color, movement_type = 'normal'):
    travel_days, coef, mask, path, move, color, typ = 0, 0, [o for o in fields_accessibility_mask], [o for o in entry_path], movement_value, creature_color, movement_type
    
    pubs = [] # list of movement-finishing fields
    while(len(path) > 1):
      evalu = self.move_one_turn(path, move, color, typ)
      departure, moveleft = evalu[0], evalu[1]
      path = path[path.index(evalu[0]):]
      travel_days += 1
      pubs.append(departure)
    coef_time = gg.TRAVEL_DAYS* travel_days + gg.MOVEMENT_LEFT* moveleft

    #IMPASSABLE_ENEMY  = 10**4       # sector contains enemy
    #IMPASSABLE_ENGAGE = 10**8       # there is a fight in a sector
    #IMPASSABLE_ALLY   = 10**12      # sector contains four allies (the limit; cannot finish move here no matter what)

    coef_army, path = 0, [o for o in entry_path]
    coef_army = 0
    for o in path: coef_army += mask[o]
    
    path = [o for o in entry_path]
    for o in path:
      if not o in pubs:                                                       # if it is passing-through tile
        if typ == 'flying': coef_army -= mask[o]                              # flyings can ignore everyone if it is not one of final stops
        elif mask[o] >= gg.IMPASSABLE_ALLY: coef_army -= gg.IMPASSABLE_ALLY   # four friends doesn't take effect, if it is not one of stops
      if (o in (0, 1, 2) and typ == 'forestwalk') or (o in (3, 4, 5) and typ == 'swampwalk'): # if it is native-walk at his native grounds
        if mask[o] >= gg.IMPASSABLE_ENGAGE: coef_army -= gg.IMPASSABLE_ENGAGE # nativewalks can ignore the combat but they still cares a bit about of how many creatures there are in total on the way
    # the what is left there now should be the sum of unskippable-enemies number and relative strength plus those of not-cheated-around others-overriding 'strong' switches

    #print('RESULT >>> '+ str(entry_path) +' '+ str(travel_days) +':'+ str(pubs) +' '+ str(coef_time) +' '+ str(coef_army) +'\n'*3)
    #gg.getch()
    return [coef_time + coef_army, pubs]
  # end of movement_coeficient()

  # find_path(): key method for movement of a gang feature; returns the best movement path between two points of Battlefield
  def find_path(self, fields_accessibility_mask, start_field, finish_field, movement_value, creature_color, walktype = 'normal'):
    mask, path, begin, end, move, color, typ = [o for o in fields_accessibility_mask], [], start_field, finish_field, movement_value, creature_color, walktype
    if begin == end: return False
    if color[1] == 'B': color = 'blue'
    if color[1] == 'G': color = 'green'
    if color[1] == '-': color = 'black'
    #print(self.move_one_turn([9, 10, 0, 1, 2, 13, 12], move, color, typ)); gg.getch()
    
    alll = [o for o in self.fish_paths] if typ == 'fish' else [o for o in self.all_paths]
    valid = []
    for one in alll:
      if begin in one and end in one:
        if one.index(begin) > one.index(end): one = one[::-1]
        valid.append(one[one.index(begin) : one.index(end) +1])
    valid_unique = []
    for one in valid:        # by the end of this loop, valid_unique contains all valid paths between given fields; there are 16 of them from west to east end
      if not one in valid_unique: valid_unique.append(one)
    movement_coeficient, pubs = [], [] # next, they will be sorted by obstacles-coeficient
    for one in valid_unique:
      aaa = self.count_movement_coeficient(mask, one, move, color, typ)
      movement_coeficient.append(aaa[0])
      pubs.append(aaa[1])

    minimum, index = gg.BIGGER_THAN_ALL, -1
    for i in range(len(movement_coeficient)):
      #valid_unique[i].append(movement_coeficient[i])
      #print(valid_unique[i])
      mc = movement_coeficient[i]
      if mc < minimum: minimum = mc; index = i
    
    #print(str(valid_unique) +' = '+ str(index) +': '+ str(valid_unique[index]) +'  --stops:'+ str(pubs[index]))
    #gg.getch()
    return [valid_unique[index], pubs[index]]

# define_all_paths(): calculates all possible maximum paths for fish and all other; run once at the beginning
  def define_all_paths(self):
    paths = []
    paths.append([6,7,4,1,2])    
    paths.append([8,7,4,1,0])    
    paths.append([6,3,4,5,2])    
    paths.append([8,5,4,3,0])    
    paths.append([6,3,4,1,2])    
    paths.append([6,7,4,5,2])    
    paths.append([8,7,4,3,0])    
    paths.append([8,5,4,1,0])    
    paths.append([6,3,0,1,2])    
    paths.append([8,5,2,1,0])    
    paths.append([6,7,8,5,2])    
    paths.append([8,7,6,3,0])
    
    current_paths = [o for o in paths]
    for both_ends in range(2):
      new = []
      for d in current_paths:
        if   d[-2:] == [7, 6]: new.append(d+ [11, 10]); new.append(d+ [11,  9])
        elif d[-2:] == [1, 0]: new.append(d+ [10, 11]); new.append(d+ [10,  9])
        elif d[-2:] == [7, 8]: new.append(d+ [14, 12]); new.append(d+ [14, 13])
        elif d[-2:] == [1, 2]: new.append(d+ [13, 12]); new.append(d+ [13, 14])
        elif d[-3] != 4: continue
        elif d[-2:] in ([3, 0], [3, 6]):
          new.append(d[:-1]+ [10,  9])
          new.append(d[:-1]+ [11,  9])
          new.append(d)
        elif d[-2:] in ([5, 2], [5, 8]):
          new.append(d[:-1]+ [13, 12])
          new.append(d[:-1]+ [14, 12])
          new.append(d)
      current_paths = []
      if both_ends: 
        for one in new: current_paths.append(one)
      else:
        for one in new: current_paths.append(one[::-1])
      #for one in current_paths: print(one)
      #print('\n'); gg.getch()
    # end of double loop
    for one in current_paths: paths.append(one)
    paths.append([ 9, 10, 0, 1, 2, 13, 12])
    paths.append([11, 10, 0, 1, 2, 13, 12])
    paths.append([ 9, 10, 0, 1, 2, 13, 14])
    paths.append([11, 10, 0, 1, 2, 13, 14])
    paths.append([ 9, 11, 6, 7, 8, 14, 12])
    paths.append([10, 11, 6, 7, 8, 14, 12])
    paths.append([ 9, 11, 6, 7, 8, 14, 13])
    paths.append([10, 11, 6, 7, 8, 14, 13])
    self.all_paths = [o for o in paths]
        
    fish = []
    fish.append([9, 10, 3, 4, 5, 13, 12])
    fish.append([9, 10, 3, 4, 5, 14, 12])
    fish.append([9, 11, 3, 4, 5, 13, 12])
    fish.append([9, 11, 3, 4, 5, 14, 12])
    fish.append([10, 11])
    fish.append([13, 14])
    self.fish_paths = [o for o in fish]
    return True
# end of define_all_paths()
  

# justify(): reformat text string to format readable by Terminal()
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
  
  # get_ability_string(): returns te proper ability description
  def get_ability_string(self, letter):
    c = self.ungreat(letter)
    if c == 'a': return 'ill'
    if c == 'b': return 'builder'
    if c == 'c': return 'caster'
    if c == 'd': return 'decoy'
    if c == 'e': return 'coward'
    if c == 'f': return 'flying'
    if c == 'g': return 'fear'
    if c == 'h': return 'haste'
    if c == 'i': return 'immune'
    if c == 'j': return 'firststrike'
    if c == 'k': return 'slowstrike'
    if c == 'l': return 'flanking'
    if c == 'm': return 'mentat'
    if c == 'n': return 'native'
    if c == 'o': return 'decoy'
    if c == 'p': return 'provoke'
    if c == 'q': return 'carrier'
    if c == 'r': return 'rampart'
    if c == 's': return 'sniper'
    if c == 't': return 'trample'
    if c == 'u': return 'scout'
    if c == 'v': return 'defender'
    if c == 'w': return 'wallcrusher'
    if c == 'x': return 'healer'
    if c == 'y': return 'spy'
    if c == 'z': return 'worker'
    if c == '1': return 'leader'
    if c == '3': return 'commander'
    return False
  
  def isgreat(self, c): return True if c == '4' or c == '2' or c.isupper() else False
  def ungreat(self, c):
    if    c == '4': d = '3'
    elif  c == '2': d = '1'
    else: d = c.lower()
    return d


  # clean(): destructor
  def clean(self):
    del self.method
    del self.fish_paths
    del self.all_paths
    return True
  _initialise = initialise
# end of Parser class
  
