from constants import the_file as gg

# Gang: this class represents the soldiers of a game. Supposedly there can be up to 50 active of them at a time
class Gang:
  def __init__(self, position, card_id, player, life, attack, defense, shooting, movement, name, subtype, abilities, color):
    self.idd = card_id # cards have unique id. at the beginning of game all the cards are in one of player's library. the libraries are getting them ids when initialised. id of gang helps the game to know what to do with (until now hidden) card
    self.gng_id = -1   # will be set as a next step
    self.owner = player
    self.position = position

    self.life      = 10* life
    self.attack    = attack
    self.defense   = defense
    self.shooting  = shooting
    self.movement  = movement
    self.name      = name
    self.subtype   = subtype
    self.abilities = [o for o in abilities]
    self.morale    = 100

    self.life_temp      = self.life # actual hp

    self.attack_temp    = 0 # actual bonus to attack, defense ...
    self.defense_temp   = 0
    self.shooting_temp  = 0
    self.movement_temp  = 0
    self.morale_temp    = 0
    self.movement_current = movement
    
    self.armor  = ''
    self.weapon = ''
    self.spell  = ''
    self.movement_path = []
    self.command = ''
    self.destination = False
    self.free_movement = 'none'

    self.colorchar = color
    self.color = 0
    c = color[0]
    if c == 'g': self.color = gg.GREEN
    if c == 'r': self.color = gg.RED
    if c == 'b': self.color = gg.BLUE
    if c == 'x': self.color = gg.BLACK
    if c == 'w': self.color = gg.WHITE
    if c == 'y': self.color = gg.YELLOW

    #self.passive_effect_stack = ['a1D2'] # decrease attack by one and increase defense by 2
    self.passive_effect_stack = '' # list of strings. their sum (together with similar strings in weapon &armor) makes the values of four _temp parameters
    return None
  
  def set_gang_id(self, n): self.gng_id = n; return True
  def get_id(self): n = self.gng_id; return n
  def identity(self): x = self.idd; return x
  def get_owner(self): x = self.owner; return x
  def get_life(self): x = self.life; return x
  def get_hp(self): x = self.life_temp; return x
  def get_attack(self):   self.recount_buffs(); x = self.attack +   self.attack_temp;   return x
  def get_defense(self):  self.recount_buffs(); x = self.defense +  self.defense_temp;  return x
  def get_shooting(self): self.recount_buffs(); x = self.shooting + self.shooting_temp; return x
  def get_movement(self): self.recount_buffs(); x = self.movement + self.movement_temp; return x
  def get_morale(self):   self.recount_buffs(); x = self.morale +   self.morale_temp;   return x
  def get_current_movement(self): x = self.movement_current; return x
  def get_name(self): x = self.name; return x
  def get_subtype(self): x = self.subtype; return x
  def get_abilities(self): x = [o for o in self.abilities]; return x
  def get_position(self): x = self.position; return x
  def null_movement(self): self.movement_current = 0; return True
  def set_position(self, pos): self.position = pos; return True
  def add_buff(self, buff): self.passive_effect_stack.append(buff); return True
  def get_hp_life_ratio(self): a = float(self.life_temp) / float(self.life); return a
  def set_movement_path(self, x):
    self.movement_path = [o for o in x]
    if x == []: self.null_destination()
    return True
  def get_movement_path(self): x = [o for o in self.movement_path]; return x
  def null_movement_path(self): return self.set_movement_path([])
  def set_command(self, x): self.command = x; return True
  def get_command(self): x = self.command; return x
  def get_color(self): x = self.color; return x
  def get_colorchar(self): x = self.colorchar; return x
  def get_relative_value(self): rv = 99* self.get_attack() + 99* self.get_defense() + 99* self.get_shooting() + self.get_life() + self.get_hp() //10; return rv
  def set_destination(self, d): self.destination = d; return True
  def get_destination(self): d = self.destination; return x
  def null_destination(self): self.destination = False; return True

  # get_color_char(): returns the color of gang for some method in Screen
  def get_color_char(self):
    c = self.color
    if c == gg.YELLOW:return 'y'
    if c == gg.BLUE:  return 'b'
    if c == gg.RED:   return 'r'
    if c == gg.GREEN: return 'g'
    if c == gg.BLACK: return 'x'
    if c == gg.WHITE: return 'w'
    return False
  
  # get_typewalk(): important for finding the best path between two Fields
  def get_typewalk(self):
    word = 'normal'
    if self.get_subtype() == 'fish': word = 'fish'
    elif self.abilities[gg.FLYING]: word = 'flying'
    elif self.abilities[gg.NATIVE]:
      c = self.color
      if c in ('green', 'red', 'yGellow'): word = 'forestwalk'
      if c in ('blue', 'x-black', 'yBellow'): word = 'swampwalk'
    return word

  # decrease_movement(): mandatory effect of moving ;)
  def decrease_movement(self, n = 3582):
    self.movement_current -= n
    if self.movement_current < 0: self.movement_current = 0
    return True
  
  # when Gang is fighting other Gang, Battlefield calculates how bad it was and calls this method
  def damage(self, amount):
    self.life_temp -= amount
    return True if self.life > 0 else False
  
  # recount_len_two(): help method of recount_buffs() (every buff consist from 2 letters)
  def recount_len_two(self, one, two):
      sign = 1 if one.isupper() else -1
      c = one.tolower()
      if c == 'a': self.attack_temp   += sign* two
      if c == 'd': self.defense_temp  += sign* two
      if c == 's': self.shooting_temp += sign* two
      if c == 'm': self.movement_attack_temp += sign* two
      if c == 'o': self.morale_temp += sign* two
      return True    
  
  # recount_buffs(): when asked for value of attack (for example), class will first add (or substract) all temporary effects like armor
  def recount_buffs(self):
    self.morale_temp, self.attack_temp, self.defense_temp, self.shooting_temp, self.movement_temp = 0, 0, 0, 0, 0
    llist = self.passive_effect_stack + self.armor + self.weapon
    first, temp = False, ''
    for letter in llist:
      if not first: temp = letter; first = True
      else: recount_len_two(temp, letter); first = False
    return True
  
  # convert_value(): converts the char as it appeard in data/cards file into a real value
  def convert_value(self, char):
      c = char
      if c.isdigit(): return int(c)
      if c.islower(): return ord(c) - ord('a') + 10
      if c.isupper(): return ord(c) - ord('A') + 20
      print('\n\nwrong input for Gang.recount_values.convert_value(): ' +c +'\n')
      return False

  # refresh(): getting the movement at the beginning of owner's turn
  def refresh(self):
    self.movement_current = self.get_movement()
    cc = self.get_colorchar()
    if self.abilities[gg.NATIVE]:
      if cc in ('green', 'red', 'yGellow'): self.free_movement = 'forestwalk'
      if cc in ('blue', 'x-black', 'yBellow'): self.free_movement = 'swampwalk'
      if cc in ('white'): self.free_movement = 'plainswalk'
    return True
  # end of refresh()
  
  # clean(): destructor
  def clean(self):
    del self.idd
    del self.gng_id
    del self.owner
    del self.position
    
    del self.life
    del self.attack
    del self.defense
    del self.shooting
    del self.movement
    del self.name
    del self.subtype
    del self.abilities
    del self.morale

    del self.life_temp
    del self.attack_temp
    del self.defense_temp
    del self.shooting_temp
    del self.movement_temp
    del self.morale_temp
    del self.movement_current
    
    del self.armor
    del self.weapon
    del self.spell
    
    del self.passive_effect_stack
    del self.movement_path
    del self.command
    del self.color
    del self.colorchar
    del self.destination
    del self.free_movement
    
    return True
# end of class Gang


# following classes are not in use at the point

class Ability:
  def __init__(self, keyword, value = True):
    self.keyword = keyword
    self.basic = value
    self.modified = value
    self.current = value
    
    return None
  
  # clean(): destructor
  def clean(self):
    
    return True
# end of class Ability



class Visibility():
  def __init__(self, native_terrain):
    self.native = native_terrain
    
    return None
  
  # clean(): destructor
  def clean(self):
    del self.native
    
    return True
# end of class Visibility



class Movement():
  def __init__(self, native_terrain):
    self.native = native_terrain
    
    return None
  
  # clean(): destructor
  def clean(self):
    del self.native
    
    return True
# end of class Movement





class Combat_bonus:
  def __init__(self):
    
    return None
  
  # clean(): destructor
  def clean(self):
    
    return True
# end of class Combat_bonuses
