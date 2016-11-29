from constants import the_file as gg

# Table: every table is run within this class; drawing the table included
class Table:
  def __init__(self, screen_instance, signal_instance):
    self.screen = screen_instance
    self.signal = signal_instance
    self.name = ''
    self.command = []
    self.mc_pay = 0
    self.mc_mask = [0,0,0,0,0]
    self.final_result = []
    self.butt1_active = True
    self.butt2_active = True
    self.butt3_active = True
    
    self.__reset()
    return None
  # end of __init__()

  def locate_point_of_program(self, name, command): self.name = name; self.command = command; return True
  def get_final_result(self): txt = self.final_result; return txt
  
  def get_the_orientation_by_name(self):
    if 'vertical' in self.command: return 'vertical'
    return 'horizontal'

  # reset(): default values for every single table
  def reset(self):
    self.color_table = gg.GRAY
    self.color_text  = gg.VIOLET
    self.cursor = 0
    self.subcursor = -1
    self.set_system_cursor()
    self.final_result = ''
    self.cursor_movement_orientation = self.get_the_orientation_by_name()
    self.bracket = self.get_bracket()
    if self.name != '': self.initialise()
    return True
  # end of reset()
  
  # initialise(): continuation of reset() in case the type of table is already known
  def initialise(self):
    name, args = self.name, self.command
    self.butt1_active = True
    self.butt2_active = True
    self.butt3_active = True
    
    if name == 'colorless_manacost':
      self.mc_pay = args[0]
      for i in range(5): self.mc_mask[i] = int(args[1][i])
    if name == 'list_of_gangs':
      self.command[1] = self.sort_gangs(self.command[1])
      aaa = self.get_where_to_jump()
      if aaa != 'nowhere': self.jump_to(int(aaa))
    return True
  
  # get_where_to_jump(): start the table at certain member's position if desired
  def get_where_to_jump(self):
    st, command = 'nowhere', self.command
    for one in command: 
      if type(one) == str and 'jump_to' in one: st = one[one.index(':') +1:]
    return st
  
  # jump_to(): executing of previous
  def jump_to(self, where):
    gangs = self.command[1]
    for i in range(len(gangs)):
      if gangs[i].get_id() == where: self.signal.set_cursor(i)
    return True
  
  # run(): main method; whether the given keypress is changing the screen; method is also responsible for eny other 'side' effects of the valid keypresses
  def run(self, keypress):
    key = keypress
    # arrows
    if self.cursor_movement_orientation == 'horizontal':
      if key in (gg.LEFT, gg.RIGH): self.move_cursor(key); return False
      if key in (gg.UP,   gg.DOWN): self.move_subcursor(key)
    else: # 'vertical' orientation
      if key in(gg.UP,   gg.DOWN): self.move_cursor(key); return False
      if key in(gg.LEFT, gg.RIGH): self.move_subcursor(key)
    # buttons 1, 2, 3 + enter
    if key in (gg.ENTE, gg.KEY1, gg.KEY2, gg.KEY3, gg.ESC):
      return self.evaluate(key)
    if key == gg.HELP: return self.helpscreen()
    return False
  # end run()
  
  # evaluate(): definition of actions based on any other than arrow keypress; table ends if this method returns True and there's no other way how the table can end
  def evaluate(self, keypress):
    key, name = keypress, self.name
    if (key == gg.KEY1 or key == gg.ENTE) and not self.butt1_active: return False
    if key == gg.KEY2 and not self.butt2_active: return False
    if key == gg.KEY3 and not self.butt3_active: return False
    #print(key, name); gg.getch()
    if name == 'colorless_manacost':
      pay, mask = self.mc_pay, [o for o in self.mc_mask]
      if key in (gg.ENTE, gg.KEY1):
        self.mc_pay -= 1; self.mc_mask[self.cursor] -= 1
          
      if key in (gg.KEY2, gg.KEY3):
        m = min(mask[self.cursor], self.mc_pay)
        self.mc_pay -= m; self.mc_mask[self.cursor] -= m
        
      if not self.mc_pay:
        self.final_result = [o for o in self.mc_mask]
        return True
      else: return False
    # end of name == 'colorless_manacost'
    
    if name == 'list_of_gangs':
      if key in (gg.ESC, gg.KEY2, gg.KEY3): self.final_result = [False, self.command[1][self.cursor]]; return True
      if key in (gg.KEY1, gg.ENTE):
        self.final_result = [True, self.command[1][self.cursor]]; return True # returns the chosen gang
    # end of name == 'list_of_gangs'
    return True
  # end of evaluate()
  
  
  # get_bracket(): length of list ie where should cursor jump from end to beginning and opposite
  def get_bracket(self):
    bracket, name = 1, self.name
    if name == 'colorless_manacost':
      bracket = 5
    elif name == '': bracket = 1
    else: bracket = self.command[0] # all non-specific tables should have bracket as a first element of command
    return bracket
  # end of get_bracket()
  
  # move_cursor(): cursor movement derived from keypress
  def move_cursor(self, keypress):
    key = keypress      
    if self.name == 'colorless_manacost': return self.move_colorless_manacost_cursor(key)
    else: self.move_cursor_normal(key)
    return True
  # end of move_cursor()
  
  # move_subcursor(): subcursor movement (the main item which cursor movement is changing remains uncganged)
  def move_subcursor(self, keypress):
    key = keypress
    if self.name == 'list_of_cards':
      bracket = self.command[1][self.cursor].get_number_of_abilities()
      if not bracket: return True
      if key == gg.UP:
        self.subcursor -= 1
        if self.subcursor < 0: self.subcursor = bracket -1
      if key == gg.DOWN:
        self.subcursor += 1
        if self.subcursor == bracket: self.subcursor = 0
      return True
  # end of move_subcursor()
  
  # move_cursor_normal(): movement definition for standart tables
  def move_cursor_normal(self, keypress):
    key = keypress
    if key in (gg.UP, gg.LEFT):
      self.cursor -= 1
      if self.cursor < 0: self.cursor = self.bracket -1
    if key in (gg.DOWN, gg.RIGH):
      self.cursor += 1
      if self.cursor >= self.bracket: self.cursor = 0
    if self.name in ('list_of_cards'): self.subcursor = -1
    return True
  # end of move_cursor_normal()

  # move_colorless_manacost_cursor(): movement definition for one of special tables
  def move_colorless_manacost_cursor(self, keypress):
    def find_next_left():
      self.move_cursor_normal(gg.LEFT)
      while(not self.mc_mask[self.cursor]): self.move_cursor_normal(gg.LEFT)
      return True
    def find_next_right():
      self.move_cursor_normal(gg.RIGH)
      while(not self.mc_mask[self.cursor]): self.move_cursor_normal(gg.RIGH)
      return True
    if keypress == gg.RIGH or keypress == gg.DOWN: find_next_right()
    else: find_next_left()
    return True
  # end of move_colorless_manacost_cursor()
      
  # get_caption(): look for name of table within list of given input arguments
  def get_caption(self):
    command, caption = self.command, ''
    for one in command: 
      if type(one) == str and 'caption' in one: caption = one[one.index(':') +1:]
    return caption
  # end of get_caption()
  
  # get_whether_to_shift(): finds out if the screen demands to be shifted (screen which demands it within 'gg.HOME' player turn)
  def get_whether_to_shift(self):
    command = self.command
    for one in command:
      if one == 'shift_it': return True
    return False
  # end of get_whether_to_shift()
  
  # get_current_player(): reads the current player from given arguments
  def get_current_player(self):
    command = self.command
    for one in command:
      if type(one) == str and 'player' in one:
        if one[one.index(':') +1:] == 'home': return gg.HOME
        if one[one.index(':') +1:] == 'away': return gg.AWAY
    return False
  
  # sort_gangs: return the sorted list of gangs based on theirs positions
  def sort_gangs(self, input_gangs):
    home_sorting_path = (9, 10, 11, 0, 3, 6, 1, 4, 7, 2, 5, 8, 13, 14, 12)
    away_sorting_path = (12, 13, 14, 2, 5, 8, 1, 4, 7, 0, 3, 6, 10, 11, 9)
    if self.get_current_player() == gg.HOME: path = home_sorting_path
    if self.get_current_player() == gg.AWAY: path = away_sorting_path
    gangs = input_gangs
    if len(gangs) <= 1: return gangs
    contin = True
    while(contin):
      contin = False
      for pos in range(len(gangs) -1):
        if path.index(gangs[pos].get_position()) > path.index(gangs[pos +1].get_position()):
          x = gangs[pos]; gangs[pos] = gangs[pos +1]; gangs[pos +1] = x
          contin = True
    return gangs
  # end of sort_gangs()
  
  # helpscreen(): what should be displayed after pressing 'h' (not ready right now)
  def helpscreen(self):
    comm = self.screen
    comm.reset()
    comm.parse('1510w text table help screen')
    comm.parse('2010y text press any key to continue ...')
    comm.go(); gg.getch()
    return False
  # end of helpscreen()
  
  # set_system_cursor(): help method for synchronisation of table's and system cursor
  def set_system_cursor(self):
    self.signal.set_cursor(self.cursor)
    self.signal.set_sub_cursor(self.subcursor)
    return True
  
  # fix_cursor(): synchronisation with system and fixing the cursor if it is not in visible point
  def fix_cursor(self):
    self.cursor = self.signal.get_cursor()
    self.subcursor = self.signal.get_sub_cursor()
    if self.name == 'colorless_manacost':
      while(not self.mc_mask[self.cursor]): self.move_cursor_normal(gg.RIGH)
    return True

  # get_card_name(): reads the name of displayed Card
  def get_card_name(self, whatcard):
    n, ln = whatcard, len(self.command[1])
    return '' if n < 0 or n >= ln else self.command[1][n].get_name() 
  
  # draw(): guess what
  def draw(self):
    name, comm, color_table, color_text, signal = self.name, self.screen, self.color_table, self.color_text, self.signal
    if name == 'colorless_manacost':
      pay, mask = self.mc_pay, [o for o in self.mc_mask]
      comm.draw_main_buttons('123', 'spend one mana of given color <ENTER works too>;spend all mana of given color;the same as button 2')
      comm.parse('0302v text to pay:')
      for i in range(pay): comm.write(2, 12+ 4* i, ['┌┐','└┘'], gg.GRAY)
      for i in range(5):
        if mask[i]:
          for power in range(mask[i]):
            comm.draw_manasymbol(17 -3* power, 4+ 12* i, 'full', [gg.RED, gg.GREEN, gg.BLUE, gg.VIOLET, gg.WHITE][i])
          y2 = 5+ 12*i
          y3 = '0'+ str(y2) if y2 < 10 else str(y2)
          if self.cursor == i: comm.parse('24' +y3+ 'y arrow-u 04')
          y2 = 6+ 12*i
          y3 = '0'+ str(y2) if y2 < 10 else str(y2)
          if self.cursor == i: comm.parse('24' +y3+ 'y arrow-u 04')
          if self.cursor == i: comm.write(20, 5+ 12*i, ['^','║'], gg.YELLOW)
      comm.parse('0110v text choose what color mana to spend for a spell')
    # enf of name == 'colorless_manacost'

    if name == 'list_of_gangs':
      pass_mask = signal.get_passability_mask()
      gng = self.command[1][self.cursor]
      position = gng.get_position()    # position (in battlefield) of gang under cursor
      comm.parse('0128g text ' +self.get_caption())
      comm.parse('1601g text »»')
      comm.parse('1620g text ««')
      
      butt_mask, butt_text = '', ''

      if (gng.get_owner() != self.get_current_player()):
        butt_text = 'cannot command enemy gang'
        self.butt1_active = False
      else:
        if not gng.get_current_movement():
          butt_text = 'movement already spent'
          self.butt1_active = False
          
        valu = pass_mask[gng.get_position()]
        if valu >= gg.IMPASSABLE_ALLY: valu -= gg.IMPASSABLE_ALLY # this switch is not important right now
        if valu >= gg.IMPASSABLE_ENGAGE:
          butt_text = 'cannot command fighting unit'
          self.butt1_active = False
        
      if not len(butt_text):  
        butt_text = 'Command this gang'; butt_mask = '1'
        self.butt1_active = True
        
      
      butt_mask += '23'; butt_text += ';Cancel the command for this gang;Cancel the selection'
      comm.draw_main_buttons(butt_mask, butt_text)
      
      index = 0
      for gang in self.command[1]: # for each one within all gangs (given as argument)
        start = 16 -self.cursor
        color = gg.YELLOW if index == self.cursor else gg.GRAY
        comm.write(start+ index, 4, [gang.get_name()[:15]], color)
        index += 1
      comm.draw_gang('huge', self.command[1][self.cursor], 3, 23)
      comm.draw_battlefield_minimap(1, 1, position, gg.YELLOW)   # is being highlighted on minimap
    # end of name == 'list_of_gangs'
    
    if name == 'list_of_cards':
      comm.parse('2302w text list of all currently defined cards')
      comm.draw_card(self.command[1][self.cursor])
      ln = 11
      for line in range(3):
        for word in range (5):
          color = gg.bgYELLOW if line == 1 and word == 2 else gg.GRAY
          namestring = self.get_card_name(self.cursor -7 + 5* line + word)[:ln -2]
          if len(namestring) >= ln-2 and namestring[ln-4] == ' ': namestring = namestring[:ln-3] + ' '
          comm.write(1+ 2* line, 1+ ln* word, ['│'], gg.YELLOW)
          comm.write(1+ 2* line, 2+ ln* word, [namestring], color)
    # end of name == 'list_of_cards'
    return True
  # end of draw()
  
  # clean(): destructor
  def clean(self):
    del self.name
    del self.command
    del self.mc_pay
    del self.mc_mask
    del self.final_result
    del self.butt1_active
    del self.butt2_active
    del self.butt3_active
    return True
  __reset = reset 
# end of Table class
