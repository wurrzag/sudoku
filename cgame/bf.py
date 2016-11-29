from constants import the_file as gg

from .player import Player
from .card import Card
from .field import Field
from .gang import Gang
from .glist import Gang_list

# Battlefield:  the very main data class; directly it contains 15 Fields, 2 Players and Gang_list (full of Gangs) but through Players it contains all the current Cards too
class Battlefield:
  def __init__(self, name1, name2):
    self.homedeck = name1
    self.awaydeck = name2
    self.gangs = Gang_list()
    self.player_home = Player(gg.HOME)
    self.player_away = Player(gg.AWAY)
    self.list_of_all_cards_in_game = []
    self.current_turn = None
    
    # HOME wilderness AWAY
    #      ┌──┬──┬──┐    
    #   ┌──┤ 0│ 1│ 2├──┐  
    #┌──┤10├──┼──┼──┤13├──┐
    #│ 9├──┤ 3│ 4│ 5├──┤12│
    #└──┤11├──┼──┼──┤14├──┘
    #   └──┤ 6│ 7│ 8├──┘  
    #      └──┴──┴──┘    
    #
    #home sorting path:(9, 10, 11, 0, 3, 6, 1, 4, 7, 2, 5, 8, 13, 14, 12)
    #away sorting path:(12, 13, 14, 2, 5, 8, 1, 4, 7, 0, 3, 6, 10, 11, 9)
    #
    # battlefield fields
    self.fields = [None] * 15
    self.territory_at_start = [[gg.NONE, gg.NONE, gg.NONE],
                               [gg.NONE, gg.NONE, gg.NONE],
                               [gg.NONE, gg.NONE, gg.NONE],
                               [gg.NONE, gg.NONE, gg.NONE],
                               [gg.NONE, gg.NONE, gg.NONE]]
    

    self.__aditional_initialisation()
    return None
  # end of __init__()
  # aditional_initialisation(): second part of __init__()
  def aditional_initialisation(self):
    # setting starting type and ownership of fields on battlefield
    for i in range(15):
      if   i < 3:  terrain = gg.FOREST
      elif i < 6:  terrain = gg.RIVER
      elif i < 9:  terrain = gg.PLAIN
      elif i < 12: terrain = gg.BASE_H
      elif i < 15: terrain = gg.BASE_A
      self.fields[i] = Field(i, self.territory_at_start[i//3][i%3], terrain)
    
    # load the definition of all cards
    self.all_existing_cards = []; all_lines = []
    f = open('./data/cards', 'r')
    for line in f:
      if len(line.strip()) == 0 or line[0] == '#': continue
      self.all_existing_cards.append(Card(0, gg.AWAY, line))
      all_lines.append(line)
    f.close()
    # all_existing_cards now contains exactly what one would suppose it does
    
    # help method
    def include_card(card_id, player, textline):
      switch = False
      for one in range(len(self.all_existing_cards)):
        if self.all_existing_cards[one].get_name() == textline:
          switch = True; self.list_of_all_cards_in_game.append(Card(card_id, player, all_lines[one]))
      return switch

    
    # loading the first deck
    card_id, first, second = 0, open(self.homedeck, 'r'), open(self.awaydeck, 'r')
    for line in first:
      if len(line.strip()) == 0 or line[0] == '#': continue
      else:
        if include_card(card_id, gg.HOME, line.strip()):
          self.player_home.add_card_into_library(card_id)
          card_id += 1
        else: print('\n\nWrong card name:', '|' + line.strip() + '|', '\n'); gg.getch()
    
    # loading the second deck    
    for line in second:
      if len(line.strip()) == 0 or line[0] == '#': continue
      else:
        if include_card(card_id, gg.AWAY, line.strip()):
          self.player_away.add_card_into_library(card_id)
          card_id += 1
        else: print('\n\nWrong card name:', '|' + line.strip() + '|', '\n'); gg.getch()
    first.close(); second.close()
    
    # both players have library full of integers
    # those integers are unique card-ids. the usage would be for example:
    # self.list_of_all_cards_in_game[self.player_away.library.draw_a_card()].get_name()
    
    # very useful debug-print
    print('\nall_existing_cards:')
    for one in self.all_existing_cards: print('|' + one.get_name() + '|')
    print('\nlist_of_all_cards_in_game:')
    for a in self.list_of_all_cards_in_game:
      print(a.get_owner(), a.identity(), a.get_name())
      if a.get_type() == gg.SQUAD: (a.get_attack(), a.get_defense(), a.get_shooting())
    print('\nBEFORE DRAWING THE CARDS:')
    print('\nfirst library:\nlength = ', self.player_home.library.length())
    print(self.player_home.library.get())
    print('\nsecond library:\nlength = ', self.player_away.library.length())
    print(self.player_away.library.get())
    print('\nboth players hand &grave:')
    print(self.player_home.hand.get(), self.player_away.hand.get(), self.player_home.grave.get(), self.player_away.grave.get())
    # end of very useful debug-print
    
    # 7 cards for both players
    #for a in range(7): self.player_home.draw_card(); self.player_away.draw_card()
    #for i in (0, 20, 25, 35, 42, 44, 59): self.player_home.draw_card(i)
    for i in (0, 1, 2, 3, 4, 5, 6): self.player_home.draw_card(i)
    #for i in (62, 68, 75, 84, 90, 118, 80): self.player_away.draw_card(i)
    for i in (60, 61, 62, 63, 64, 65, 66): self.player_away.draw_card(i)
    
    # another debug print. from here...
    print('\nAFTER DRAWING THE CARDS:')
    print('\nfirst library:\nlength = ', self.player_home.library.length())
    print(self.player_home.library.get())
    print('\nsecond library:\nlength = ', self.player_away.library.length())
    print(self.player_away.library.get())
    print('\nboth players hands:')
    print(str(self.player_home.hand.get())+ '\n'+ str(self.player_away.hand.get()))
    print('\n&graves:')
    print(str(self.player_home.grave.get())+ '\n'+ str(self.player_away.grave.get()))
    # ... to here
    
    #gg.getch()
    ## ## ## UNHASH PREVIOUS LINE TO READ THE DEBUG PRINTS ## ## ##
    
    return True
  # end of aditional_initialisation()
  
  
  
  
  
  
  # cheat: temporary method; gives both players lot of mana and some units on battlefield for testing purposes 
  def cheat(self, param = ''):
    if param == 'home':
      # following lines will crash the program if cards with given ids (0, 1, 2, 3, 60, 70, 80, 90) will not be within current player's hand; check (cheat) that in constructor parent method assures the 'home' section is called at 'home' turn and opposite
      self.play_card( 0); self.get_all_gangs()[0].set_position(7)
      self.play_card( 1); self.get_all_gangs()[1].set_position(10)
      self.play_card( 2); self.get_all_gangs()[2].set_position(7)
      self.play_card( 3); self.get_all_gangs()[3].set_position(7)
      self.play_card( 4); self.get_all_gangs()[4].set_position(3)
      self.play_card( 5); self.get_all_gangs()[5].set_position(7)
      self.play_card( 6); self.get_all_gangs()[6].set_position(10)
      self.get_all_gangs()[3].damage(51)
      self.get_all_gangs()[4].damage(11)
    elif param == 'away':
      # following lines will crash the program if cards with given ids will not be within current player's hand
      self.play_card(60); self.get_all_gangs()[ 7].set_position(5)
      self.play_card(61); self.get_all_gangs()[ 8].set_position(0)
      self.play_card(62); self.get_all_gangs()[ 9].set_position(14)
      self.play_card(63); self.get_all_gangs()[10].set_position(13)
      self.play_card(64); self.get_all_gangs()[11].set_position(12)
      self.play_card(65); self.get_all_gangs()[12].set_position(8)
      self.play_card(66); self.get_all_gangs()[13].set_position(8)
      self.get_all_gangs()[8].damage(26)
      self.get_all_gangs()[9].damage(26)
      
      self.get_all_gangs()[6].decrease_movement()
      #print(str(self.get_all_gangs()[5].get_current_movement())); gg.getch()
      
    else:
      for i in range(4): self.player_home.increase_manapool('red')
      for i in range(4): self.player_home.increase_manapool('green')
      for i in range(3): self.player_away.increase_manapool('blue')
      for i in range(3): self.player_away.increase_manapool('white')
      for i in range(2): self.player_away.increase_manapool('black')
      #for i in range(1): self.player_away.increase_manapool('red')
      #for i in range(1): self.player_away.increase_manapool('green')
      #for i in range(1): self.player_away.increase_manapool('black')
      #self.player_home.reset_mana(); self.player_away.reset_mana()
      #self.player_away.spent_mana('white', 3)
      #self.player_away.spent_mana('blue', 1)
      #self.player_home.spent_mana('green', 3)
      #self.player_home.spent_mana('red', 4)
    return True
  # end of cheat()  

  # get_territory_pissings(): return the controllers of fields
  def get_territory_pissings(self):
    arr = [None] * 15
    for i in range(15): arr[i] = self.get_owner_of_field(i)
    return arr
  
  # refresh_ownership_one_field(): sub method of refresh_territory_pissings()
  def refresh_ownership_one_field(self, field):
    sw_home, sw_away, x = False, False, field
    them = self.gangs.get('position:' +str(x)) # list of al gangs residing given field
    for one in them:
      if one.get_owner() == gg.HOME: sw_home = True
      if one.get_owner() == gg.AWAY: sw_away = True
    if sw_away and not sw_home: self.fields[x].set_owner(gg.AWAY)
    if not sw_away and sw_home: self.fields[x].set_owner(gg.HOME)
    return True
 
  # refresh_territory_pissings(): recount the true controllers of the fields at every turn's start
  def refresh_territory_pissings(self):
    for i in range(15): self.refresh_ownership_one_field(i)
    return True
  
  # yieldd(): give player wood, gold and food based on controlled wilderness territory at the beginning of his turn
  def yieldd(self):
    turn = self.get_whos_on_turn()
    player = self.player_home if turn == gg.HOME else self.player_away
    for i in range(0, 3):
      if self.fields[i].get_owner() == turn: player.add_goods([3, 1, 1])
    for i in range(3, 6):
      if self.fields[i].get_owner() == turn: player.add_goods([1, 3, 1])
    for i in range(6, 9):
      if self.fields[i].get_owner() == turn: player.add_goods([1, 1, 3])
    return True
  # end of yieldd()
 
  # refresh(): the definition of all beginning the turn actions
  def refresh(self):
    self.refresh_territory_pissings()
    self.yieldd()
    gngs = self.get_all_gangs('owner:' +self.translate_turn(self.get_whos_on_turn()))
    for gng in gngs: gng.refresh() # all gangs _of_given_player_ will get full movement again
    self.move_the_lazies()         # move all the gangs which do have a movement path commanded
    return True
  # end of refresh()
  
  # evaluate_fight(): loosing the hitpoints through fighting is defined here; the method will be way longer, this is only temporal solution for gangs can go off the battlefield since they can enter already
  def evaluate_fight(self):
    for i in range(15):
      hm, aw = self.get_all_gangs('owner:home' + ' position:' +str(i)), self.get_all_gangs('owner:away' + ' position:' +str(i))
      if len(hm) and len(aw):
        str_h, str_a = 0, 0
        for h in hm: str_h += h.get_attack() + h.get_defense()
        for a in aw: str_a += a.get_attack() + a.get_defense()
        for h in hm: h.damage(7* str_a)
        for a in aw: a.damage(7* str_a)
        for h in hm:
          if h.get_hp() <= 0: h.set_position(-1)
        for a in aw:
          if a.get_hp() <= 0: a.set_position(-1)
    return True
  # end of evaluate_fight()
  
  # move_the_lazies(): moving of all units with movement command active
  def move_the_lazies(self):
    filt     = 'owner:home' if self.get_whos_on_turn() == gg.HOME else 'owner:away'
    filt_neg = 'owner:home' if self.get_whos_on_turn() == gg.AWAY else 'owner:away'
    for one in self.get_all_gangs(filt):
      movem, path2, clr = one.get_current_movement(), one.get_movement_path(), one.get_colorchar()
      #if one.get_name() == 'Sprite': print(path2); gg.getch()
      if not(movem and len(path2)): continue
      path, switch = path2[1:], False
      while movem > 0 and len(path):
        switch = True
        step, fld = 0, path[0]
        path = path[1:]
        if   fld in (0, 1, 2): # forested hills
          if one.free_movement == 'forestwalk': one.free_movement = 'none'
          else:
            step = 1 if clr in ('green', 'red', 'yGellow') else 3
        elif fld in (3, 4, 5): # swampy river
          if one.free_movement == 'swampwalk': one.free_movement = 'none'
          else:
            step = 1 if clr in ('blue', 'x-black', 'yBellow') else 2          
        elif fld in (6, 7, 8) and one.free_movement == 'plainswalk': one.free_movement = 'none' # plains
        else: step = 1
        movem -= step
        #print(len(self.get_all_gangs(filt_neg + ' position:' +str(fld))))
        if len(self.get_all_gangs(filt_neg + ' position:' +str(fld))):
          path = []; movem = 0
      if switch: one.set_position(fld)
      else: one.set_position(path2[0])
      one.decrease_movement(); one.set_movement_path(path)
    return True
  # end of move_the_lazies()
  
  # get_fields_passability(): returns the parameter for Parser's method of find_path(); the parameter is mask of passability indexes for 15 fields of the game
  def get_fields_passability(self, playerr):
    fpass, pl = [0] *15 , playerr
    
    #field = self.get_all_gangs('position:8'); print(field[1].get_name())
    #print(len(field))
    for i in range(15): # for 15 fields
      #print('\n'+ str(i) +':')
      field = self.get_all_gangs('position:' +str(i))
      sw_home, sw_away = False, False   # whether there are home units on this field and whether away
      own_creatures = 0                 # number of friends in this field
      for f in range(len(field)):
        #print(str(field[f].get_owner()) +'  '+ str(field[f].get_name()))
        if field[f].get_owner() == pl: # (home units)
          sw_home = True
          own_creatures += 1
        else: # (enemy units)
          sw_away = True
          fpass[i] += gg.IMPASSABLE_ENEMY                       # add value of enemy being there
          fpass[i] += field[f].get_relative_value()             # add relative value of enemy as a minor factor
        
      if own_creatures >= 4: fpass[i] += gg.IMPASSABLE_ALLY     # get the switch of full-house of friends for each field
      if sw_home and sw_away: fpass[i] += gg.IMPASSABLE_ENGAGE  # set the switch of engaged field
        
    #gg.getch()
    return fpass
  # end of get_fields_passability()
  
  # add_gang(): create a gang from (just played) card and add it to the list of all gangs
  def add_gang(self, card):
    position = 9 if self.current_turn == gg.HOME else 12
    new = Gang(position, card.identity(), card.get_owner(), card.get_life(), card.get_attack(), card.get_defense(), card.get_shooting(), card.get_movement(), card.get_name(), card.get_subtype(), card.get_abilities(), card.get_color())
    self.gangs.add(new)
    return True

  # play_card(): move the card between appropriate libraries and make appropriate effects
  def play_card(self, identifier):
    idd = identifier
    card, pl = self.get_all_cards()[idd], self.get_player(self.get_whos_on_turn())
    if card.get_type() == gg.CREATURE:
      pl.cast_spell(idd)    # move the card from hand to secret grave ie out of active game at the point
      self.add_gang(card)   # adds the gang to the list
      index, allg = 0, self.get_all_gangs()
      for one in allg: one.set_gang_id(index); index += 1
    return True
  # end of play_card()
    
  # get_gang(): get the gang by id
  def get_gang(self, gang_id):
      for one in self.get_all_gangs():
          if one.identity() == gang_id: return one
      return False
    
  # clean(): destructor
  def clean(self):
    del self.territory_at_start
    del self.homedeck
    del self.awaydeck
    del self.current_turn

    self.player_home.clean(); del self.player_home
    self.player_away.clean(); del self.player_away

    for card in self.list_of_all_cards_in_game: card.clean()
    del self.list_of_all_cards_in_game

    for one in self.all_existing_cards: one.clean()
    del self.all_existing_cards

    for one in self.fields: one.clean()
    del self.fields

    for one in self.gangs.get_all(): one.clean()
    self.gangs.clean(); del self.gangs

    return True
  __aditional_initialisation = aditional_initialisation


  def translate_turn(self, turn, neg = False):
    if neg == False:
      if turn == gg.HOME: return 'home'
      if turn == gg.AWAY: return 'away'
    else:
      if turn == gg.HOME: return 'away'
      if turn == gg.AWAY: return 'home'
    return 'none'

  def get_owner_of_field(self, field): f = field; return self.fields[f].get_owner()
  def get_all_existing_cards(self): return self.all_existing_cards
  def get_all_cards(self): x = [o for o in self.list_of_all_cards_in_game]; return x
  def get_all_gangs(self, param = ''): x = self.gangs.get(param); return x
  def get_player(self, who): return self.player_home if who == gg.HOME else self.player_away
  def set_current_turn(self, x): self.current_turn = x; return True
  def get_whos_on_turn(self): x = self.current_turn; return x
  
# end of class Battlefield

