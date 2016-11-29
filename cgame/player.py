from constants import the_file as gg

from .crd import Card_list
from .crd import Manacost

class Player:
  def __init__(self, owner):
    self.owner = owner          # gg.HOME or gg.AWAY
    self.library  = Card_list() # library with creatures, spells etc
    self.library2 = Card_list() # library with lands and buildings
    self.hand    = Card_list()
    self.grave   = Card_list()  # regular grave
    self.grave2  = Card_list()  # invisible (inactive) 'grave' of currently-in-game cards, which are there as class Soldier at the point (Battlefield class is responsible for linking soldiers ids to proper cards ids)
    self.life = 2000
    self.mana = [0, 0, 0, 0, 0]        # red, green, blue, black, white
    self.mana_temp = [0, 0, 0, 0, 0]   # current mana (previous line is overall mana)
    self.goods = [0, 0, 0]             # wood, money, food
    self.progress = [0, 0, 0, 0, 0]    # progress towards land-search triggers
    self.empty_manacost = Manacost()   # empty slot for use in upper structures
    self.passive_effect_stack = [] # list of strings. their sum (together with similar strings in weapon &armor) makes the values of four _temp parameters
    return None


  def get_empty_manacost(self): self.empty_manacost.null(); return self.empty_manacost
  def get_overall_mana(self): return [o for o in self.mana]
  def get_mana(self):         return [o for o in self.mana_temp]
  def get_goodies(self):      return [o for o in self.goods]
  def get_life(self): x = self.life; return x
  def identify(self): x = self.owner; return x
  def null_progress(self, n): progress[n] = 0; return True
  def null_manapool(self): self.mana_temp = [0, 0, 0, 0, 0]; return True

  # refresh(): the beginning of turn phase
  def refresh(self):

    # refresh the manapool
    def untap(): self.mana_temp = [o for o in self.mana]; return True
    
    # upkeep is call-sign for all beginning-of-turn passive battlefield effects
    def upkeep(): return True
  
    # player will draw some cards derived from battlefield settings and game progress
    def draw():
      self.draw_card()
      return True
    
    untap(); upkeep(); draw()
    return True
  # end of refresh()

  # copy_manapool_to_manacost(): transfers current manapool to format useful for casting the card process
  def copy_manapool_to_manacost(self):
    ret, m = self.empty_manacost, self.mana_temp
    ret.white, ret.black, ret.blue, ret.green, ret.red = m[4], m[3], m[2], m[1], m[0]
    ret.total = self.get_total_current_mana()
    return ret

  # load_manapool_from_manacost(): this method will be called as a result of casting the card process
  def load_manapool_from_manacost(self, manacost):
    m = manacost
    self.mana_temp[4] = m.white
    self.mana_temp[3] = m.black
    self.mana_temp[2] = m.blue
    self.mana_temp[1] = m.green
    self.mana_temp[0] = m.red
    return True
  
  # load_manapool_from_array(): or alternativelly this one
  def load_manapool_from_array(self, arrayy):
    arr = [o for o in arrayy]
    for i in range(5): self.mana_temp[i] = arr[i]
    return True

  # set_negative_manacost(): creating one of proper return values for compare_manacost()
  def set_negative_manacost(self):
    ret = self.empty_manacost
    ret.total, ret.red, ret.green, ret.blue, ret.black, ret.white = -1, -1, -1, -1, -1, -1
    return ret
  
  # get_total_current_mana(): returns the sum of all plaeyr's current mana
  def get_total_current_mana(self):
    c = 0
    for o in self.mana_temp: c += o
    return c
  count_mana = get_total_current_mana

# get_total_current_mana(): returns the sum of all plaeyr's mana
  def get_total_mana(self):
    c = 0
    for o in self.mana: c += o
    return x
  count_mana_full = get_total_mana

  # compare_manacost(): checks the given manacost (of card) with current manapool. Returns Manacost()
  # whatever else return value than -1 in all parameters means the player can cast the card and if he does so
  # the return value of this method can be used as argument for load_manapool_from_manacost() to get the remaining (ie current) manapool
  def compare_manacost(self, mana_cost):
    ret, m = self.copy_manapool_to_manacost(), mana_cost
    ret.white -= m.white
    ret.black -= m.black
    ret.red   -= m.red
    ret.green -= m.green
    ret.blue  -= m.blue
    if m.total > ret.total or ret.white <0 or ret.black <0 or ret.red <0 or ret.blue <0 or ret.green<0:
      ret = self.set_negative_manacost()
    return ret
  # end of compare_manacost()

  # add_progress(): adds the values towards 5 color of mana landsearch progress
  def add_progress(self, kvuintle):
    k = [o for o in kvuintle]
    for n in range(5): progress[n] += k[n]
    return True

  # increase_manapool(): increases player's total manapool; this is what happens when player play the mana source card
  def increase_manapool(self, color):
    if color == 'red':   self.mana[0] += 1; self.mana_temp[0] += 1
    if color == 'green': self.mana[1] += 1; self.mana_temp[1] += 1
    if color == 'blue':  self.mana[2] += 1; self.mana_temp[2] += 1
    if color == 'black': self.mana[3] += 1; self.mana_temp[3] += 1
    if color == 'white': self.mana[4] += 1; self.mana_temp[4] += 1
    return True
  
  # add_goods(): adds the wood, gold, food into storage
  def add_goods(self, arr):
    self.goods[0] += arr[0]
    self.goods[1] += arr[1]
    self.goods[2] += arr[2]
    return True
  
  # spent_mana(): aternative way of emptying the manapool as effect of playing the card
  def spent_mana(self, color, amount):
    if color == 'red': self.mana_temp[0] -= amount
    if color == 'green': self.mana_temp[1] -= amount
    if color == 'blue': self.mana_temp[2] -= amount
    if color == 'black': self.mana_temp[3] -= amount
    if color == 'white': self.mana_temp[4 ] -= amount
    if color == 'wood': self.goods[0] -= amount
    if color == 'gold': self.goods[1] -= amount
    if color == 'food': self.goods[2] -= amount
    return True

  # reset_mana(): regaining the mana at the beginning of turn
  def reset_mana(self):
    for i in range(5): self.mana_temp[i] = self.mana[i]
    return True

  
  def add_card_into_grave  (self, card_id): self.grave.add(card_id); return True
  def add_card_into_library(self, card_id): self.library.add(card_id); return True
  def add_card_into_hand   (self, card_id): self.hand.add(card_id); return True
  def remove_card_from_grave  (self, card_id): self.grave.remove(card_id); return card_id
  def remove_card_from_hand   (self, card_id): self.hand.remove(card_id); return card_id
  def remove_card_from_library(self, card_id): self.library.remove(card_id); return card_id

  def sort_libraries(self, id_number = False): self.discard_from_to('library', 'library2', id_number)
  def draw_card     (self, id_number = False): self.discard_from_to('library', 'hand'    , id_number)
  def brain_freeze  (self, id_number = False): self.discard_from_to('library', 'grave'   , id_number)
  def unearth       (self, id_number = False): self.discard_from_to('grave'  , 'hand'    , id_number)
  def genesis       (self, id_number = False): self.discard_from_to('grave'  , 'library' , id_number)
  def discard       (self, id_number = False): self.discard_from_to('hand'   , 'grave'   , id_number)
  def unsummon      (self, id_number = False): self.discard_from_to('grave2' , 'hand'    , id_number)
  def death         (self, id_number = False): self.discard_from_to('grave2' , 'grave'   , id_number)
  def cast_spell    (self, id_number = False): self.discard_from_to('hand'   , 'grave2'  , id_number)
  def brainstorm    (self, id_number = False): self.discard_from_to('hand'   , 'library' , id_number)

  # discard_from_to(): move the card between two of the cardlists owned by player
  def discard_from_to(self, from_where, to_where, id_number = False):
    def move_card_by_id (card_id, from_where, to_where): to_where.add(from_where.draw_a_card_by_id_number(card_id)); return True
    def move_card_random(         from_where, to_where): to_where.add(from_where.draw_a_card()); return True
    def translate_parameter(what):
      if what == 'grave':   return self.grave
      if what == 'grave2':  return self.grave2
      if what == 'hand':    return self.hand
      if what == 'library': return self.library
      if what == 'library2':return self.library2
      print('\n\nbattlefield.py.Player.discard_from_to: wrong parameter' + str(what) + '\n')
      return False
    
    source, destination = translate_parameter(from_where), translate_parameter(to_where)
    if type(id_number) == int: move_card_by_id(id_number, source, destination)
    else: move_card_random(source, destination)
    return True
  # end of discard_from_to()
  
  # clean(): destructor
  def clean(self):
    del self.owner
    self.library.clean(); del self.library
    self.library2.clean(); del self.library2
    self.hand.clean(); del self.hand
    self.grave.clean(); del self.grave
    self.grave2.clean(); del self.grave2
    del self.life
    del self.mana
    del self.mana_temp
    del self.goods
    del self.progress
    self.empty_manacost.clean(); del self.empty_manacost
    del self.passive_effect_stack
    
    return True
# end of class Player
