from constants import the_file as gg

# Signal: all system valuables are stored here; single-instance available virtually everywhere
class Signal:
  def __init__(self):
    #self.command = ''      # what command to run
    self.whos_on_turn = gg.HOME
    self.new_screen_overwrite = True
    self.new_screen_palette = gg.NONECOLOR
    self.cursor = 4        # the where the cursor is right now
    self.sub_cursor = 0    # sub cursor used for scrolling between the abilities of a card
    self.cursor_color = gg.YELLOW
    self.home_player_battlefield_cursor_position = 4
    self.away_player_battlefield_cursor_position = 4
    self.previous_gamestate = ''
    self.animation_colours = []
    self.homedeck = ''
    self.awaydeck = ''
    self.active_hand = None
    self.battlefield_style = 'default'
    self.current_state_of_game = ''
    self.battlefield_movement_active = False

    self.list_of_all_cards_in_game = []
    self.list_of_all_gangs_in_game = []
    self.currently_commanded_gangs = []
    self.passability_mask = []
    self.color_importance = [gg.BLUE, gg.VIOLET, gg.GREEN, gg.LBLUE, gg.RED, gg.YELLOW, gg.WHITE, gg.GRAY, gg.bgBLUE, gg.bgVIOLET, gg.bgGREEN, gg.bgLBLUE, gg.bgRED, gg.bgYELLOW, gg.bgWHITE, gg.bgGRAY]
    
    self.__initialisation()
    return None
  # end of __init__()
  # initialisation(): second half of __init__()
  def initialisation(self, decks = ''):
    self.table_color = gg.GRAY
    self.home_player_color1 = gg.RED
    self.home_player_color2 = gg.VIOLET
    self.away_player_color1 = gg.LBLUE
    self.away_player_color2 = gg.BLUE
    
    with open('./data/config', 'r') as f:
      for line in f:
        if 'deck_home' in line: homedeck = './decks/' + line[line.index('=') +1:].strip()
        if 'deck_away' in line: awaydeck = './decks/' + line[line.index('=') +1:].strip()
    try: a = awaydeck; a = homedeck
    except NameError: print('\n\n\nONE OF THE PLAYERS HAVE NOT HIS DECK SET\n\nyou can fix it by editing data/config\n'); gg.getch(); return False
    self.homedeck, self.awaydeck = homedeck, awaydeck
    return True
  # end of initialisation()
  
  def set_starting_turn(self, who):
    self.whos_on_turn = who
    return True

  def get_decks_names(self): a = [self.homedeck, self.awaydeck]; return a
  def set_decks_names(self, name1, name2): self.homedeck = name1; self.awaydeck = name2; return True
  def set_cursor(self, c): self.cursor = c; return True
  def get_cursor(self): c = self.cursor; return c
  def set_sub_cursor(self, c): self.sub_cursor = c; return True
  def get_sub_cursor(self): c = self.sub_cursor; return c
  def set_previous_state(self, c): self.previous_gamestate = c; return True
  def get_previous_state(self): c = self.previous_gamestate; return c
  def get_whos_on_turn(self): x = self.whos_on_turn; return x
  def switch_whos_on_turn(self): x = self.get_whos_on_turn(); self.whos_on_turn = gg.HOME if x == gg.AWAY else gg.AWAY; return True
  def set_which_hand_is_active(self, txt): self.active_hand = txt; return True
  def what_hand(self): x = self.active_hand; return x
  def set_battlefield_style(self, what): self.battlefield_style = what; return True
  def get_battlefield_style(self): x = self.battlefield_style; return x
  def switch_battlefield_style(self): x = 'minimap' if self.battlefield_style == 'default' else 'default'; self.battlefield_style = x; return True

  def set_current_state_of_game(self, x): self.current_state_of_game = x; return True
  def get_current_state_of_game(self): x = self.current_state_of_game; return x
  def set_passability_mask(self, x): self.passability_mask = [o for o in x]; return True
  def get_passability_mask(self): x = [o for o in self.passability_mask]; return x


  def set_battlefield_movement_switch(self, switch):
    self.battlefield_movement_active = switch
    if switch == False:
      self.currently_commanded_gangs = []
    return True
  
  def get_battlefield_movement_switch(self): x = self.battlefield_movement_active; return x

  def set_currently_commanded_gangs(self, x): self.currently_commanded_gangs = [o for o in x]; return True
  def get_currently_commanded_gangs(self): x = [o for o in self.currently_commanded_gangs]; return x
  def set_currently_commanded_gang(self, x): self.currently_commanded_gangs = [x]; return True
  def get_currently_commanded_gang(self): x = self.currently_commanded_gangs[0]; return x


  def get_cursor_color(self): x = self.cursor_color; return x
  def get_table_color(self): c = self.table_color; return c
  def set_table_color(self, so): self.table_color = so; return True
  def set_colors_for_animation(self, entree): self.animation_colors = [o for o in entree]; return True
  def get_colors_for_animation(self): outree = [o for o in self.animation_colors]; return outree
  def get_colors_priority(self): return [o for o in self.color_importance]
  def get_current_player_color(self) : return self.get_players_colors('1 ') if self.get_whos_on_turn() == gg.HOME else self.get_players_colors('3 ')
  def get_current_player_colors(self): return self.get_players_colors('12') if self.get_whos_on_turn() == gg.HOME else self.get_players_colors('34')

  def get_players_colors(self, key = '1234'):
    ret = []
    if '1' in key: ret.append(self.home_player_color1)
    if '2' in key: ret.append(self.home_player_color2)
    if '3' in key: ret.append(self.away_player_color1)
    if '4' in key: ret.append(self.away_player_color2)
    if not len(ret): print("\n\nSomething is wrong in Signal.get_players_colors()\n\n"); gg.getch(); return False
    return ret[0] if len(ret) == 1 else ret

  def save_the_cards(self, llist):
    self.list_of_all_cards_in_game = []
    for o in llist: self.list_of_all_cards_in_game.append(o)
    return True
  
  def save_the_animals(self, llist):
    self.list_of_all_gangs_in_game = []
    for o in llist: self.list_of_all_gangs_in_game.append(o)
    return True
    
  def get_card(self, idd): c = self.list_of_all_cards_in_game[idd]; return c
  def get_gang(self, idd): u = self.list_of_all_gangs_in_game[idd]; return u
  get_card_by_id = get_card

  def set_player_battlefield_cursor(self, cursor_value = -1):
    c = self.get_cursor() if cursor_value == -1 else cursor_value
    if   self.get_whos_on_turn() == gg.HOME: self.home_player_battlefield_cursor_position = c
    elif self.get_whos_on_turn() == gg.AWAY: self.away_player_battlefield_cursor_position = c
    else: print('\n\ngamestate.py.Signal.set_player_battlefield_cursor(): game dont know whos on turn\n'); gg.getch(); return False
    return True

  def get_player_battlefield_cursor(self):
    if   self.get_whos_on_turn() == gg.HOME: x = self.home_player_battlefield_cursor_position; return x
    elif self.get_whos_on_turn() == gg.AWAY: x = self.away_player_battlefield_cursor_position; return x
    else: print('\n\ngamestate.py.Signal.get_player_battlefield_cursor(): game dont know whos on turn\n'); gg.getch()
    return False

  def get_whether_to_shift(self, key):
    if self.get_whos_on_turn() == gg.AWAY: return False
    if 'Hand' in key or 'Base' in key or key in ('___Game', 'table_shifted'): return True
    else: return False

  def get_current_player_color_string(self):
    color = self.away_player_color1 if self.get_whos_on_turn() == gg.AWAY else self.home_player_color1
    word = 'UNKNOWN'
    if color == gg.BLUE or color == gg.LBLUE: word = 'BLUE'
    if color == gg.GREEN or color == gg.YELLOW : word = 'YELLOW-GREEN'
    if color == gg.RED or color == gg.VIOLET: word = 'RED'
    if color == gg.WHITE or color == gg.GRAY: word = 'WHITE'
    return word


  def overwrite_the_new_screen(self): return True if self.new_screen_overwrite else False
  def palette_of_new_screen(self): x = self.new_screen_palette; return x

  def set_new_screen(self, wd):
    self.new_screen_overwrite = wd == 'black'
    if wd == 'gray': new_screen_palette = gg.GRAY
    if wd == 'blue': new_screen_palette = gg.BLUE
    if wd == 'white': new_screen_palette = gg.NONECOLOR
    return True
  
  # clean(): destructor
  def clean(self):
    #self.command = ''      # what command to run
    self.list_of_all_cards_in_game = []
    self.list_of_all_gangs_in_game = []
    self.currently_commanded_gangs = []
    self.passability_mask = []
    
    self.color_importance = [gg.BLUE, gg.VIOLET, gg.GREEN, gg.LBLUE, gg.RED, gg.YELLOW, gg.WHITE, gg.GRAY, gg.bgBLUE, gg.bgVIOLET, gg.bgGREEN, gg.bgLBLUE, gg.bgRED, gg.bgYELLOW, gg.bgWHITE, gg.bgGRAY]
    del self.whos_on_turn
    del self.new_screen_overwrite
    del self.new_screen_palette
    del self.cursor
    del self.sub_cursor
    del self.cursor_color
    del self.home_player_battlefield_cursor_position
    del self.away_player_battlefield_cursor_position
    del self.previous_gamestate
    del self.animation_colours
    del self.homedeck
    del self.awaydeck

    del self.active_hand
    del self.battlefield_style
    del self.current_state_of_game
    del self.battlefield_movement_active

    del self.color_importance
    del self.table_color
    del self.home_player_color1
    del self.home_player_color2
    del self.away_player_color1
    del self.away_player_color2

    #for one in self.list_of_all_cards_in_game: one.clean(); for one in self.list_of_all_gangs_in_game: one.clean() ## ## ## battlefield is doing that, so it can't be here
    del self.list_of_all_cards_in_game
    del self.list_of_all_gangs_in_game
    del self.currently_commanded_gangs
    del self.passability_mask
    return True
  __initialisation = initialisation
  # end of Signal class
