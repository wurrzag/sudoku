from constants import the_file as gg
from .crd import Manacost

# Card: one of key structures; players have Cards in hand (library, grave) and through mana (one of theirs attributes) can either
# forge the card into Gang or Building class instance or make some (presumably) great effect to the battlefield and its inhabitans
class Card:
  def __init__(self, card_id, player, string):
    self.idd = card_id # cards have unique id. at the beginning of game all the cards are in one of player's library. the libraries are getting them ids when initialised
    self.owner = player
    self.__initialisation(string)
    return None
    
  # initialisation(): recognize the type of a card and call the appropriate method to read and save it's parameters  
  def initialisation(self, string):
    if string[0] == 'c': self.init_creature(string[1:])
    if string[0] in ('a', 'z', 'x'): self.init_equipment(string)
    return True
  # end of initialisation()
  
  # convert_value(): converts char from cards file into proper value ('a' - 'J' are there for >10 numbers)
  def convert_value(self, char):
    c = char
    if c.isdigit(): return int(c)
    if c.islower(): return ord(c) - ord('a') + 10
    if c.isupper(): return ord(c) - ord('A') + 20
    print('\n\nwrong input for battlefield.init_creature.convert_value(): ' +c +'\n')
    return False

  # isgreat(), ungreat(): help methods of init_creature()
  def isgreat(self, c): return True if c == '4' or c == '2' or c.isupper() else False
  def ungreat(self, c):
    if    c == '4': d = '3'
    elif  c == '2': d = '1'
    else: d = c.lower()
    return d

  # init_creature(): save the values if the card is 'creature' type
  def init_creature(self, line):
    self.card_type = gg.CREATURE
    self.card_type_string = 'gang'
    manacost = line[:line.index('.')]; line = line[line.index('.') +1:]
    basics = line[:line.index('.')]; line = line[line.index('.') +1:]
    name = line[:line.index('.')]; line = line[line.index('.') +1:]
    if '.' in line: subtype = line[:line.index('.')]; line = line[line.index('.') +1:]
    else: subtype = line; line = ''
    if ';' in line: abilities = line[:line.index(';')]; line = line[line.index(';') +1:]
    else: abilities = line; line = ''
    line = line.strip()
    
    # the rest of line is 'special effect'
    self.area_of_effect = gg.NONE
    self.special_effect = ''
    self.manacost_of_effect = Manacost('')
    if len(line):
      c = line[0]; line = line[1:]
      if c == 'a': self.area_of_effect = gg.SELF
      if c == 'b': self.area_of_effect = gg.CHOSEN_FRIEND
      if c == 'c': self.area_of_effect = gg.ALL_FRIENDS
      if c == 'x': self.area_of_effect = gg.ENGAGED_ENEMY
      if c == 'y': self.area_of_effect = gg.CHOSEN_ENEMY
      if c == 'z': self.area_of_effect = gg.ALL_ENEMIES
      if c == 'o': self.area_of_effect = gg.SPECIAL
      manac = line[:line.index(',')]; line = line[line.index(',') +1:]
      self.manacost_of_effect = Manacost(manac)
      self.special_effect = line

    self.manacost  = Manacost(manacost)
    self.life      = self.convert_value(basics[0])
    self.attack    = self.convert_value(basics[1])
    self.defense   = self.convert_value(basics[2])
    self.shooting  = self.convert_value(basics[3])
    self.movement  = self.convert_value(basics[4])
    self.name      = name.strip()
    self.subtyp    = subtype.strip()

    self.abilities_string = abilities
    self.abilities = [0] * gg.NUMBER_OF_ABILITIES
    for one in abilities:
      c = self.ungreat(one) if self.isgreat(one) else one
      mult = 2 if self.isgreat(one) else 1  # value 1 for basic scout (for example) and 2 for master scout
      if c == 'a': self.abilities[gg.ILL] = mult
      if c == 'b': self.abilities[gg.BUILDER] = mult
      if c == 'c': self.abilities[gg.CASTER] = mult
      if c == 'd': self.abilities[gg.DECOY] = mult
      if c == 'e': self.abilities[gg.FLEE] = mult
      if c == 'f': self.abilities[gg.FLYING] = mult
      if c == 'g': self.abilities[gg.FEAR] = mult
      if c == 'h': self.abilities[gg.HASTE] = mult
      if c == 'i': self.abilities[gg.IMMUNE] = mult
      if c == 'j': self.abilities[gg.FIRSTSTRIKE] = mult
      if c == 'k': self.abilities[gg.SLOWSTRIKE] = mult
      if c == 'l': self.abilities[gg.FLANKING] = mult
      if c == 'm': self.abilities[gg.MENTAT] = mult
      if c == 'n': self.abilities[gg.NATIVE] = mult
      if c == 'o': self.abilities[gg.DECOY] = mult
      if c == 'p': self.abilities[gg.PROVOKE] = mult
      if c == 'q': self.abilities[gg.POISONOUS] = mult
      if c == 'r': self.abilities[gg.RAMPART] = mult
      if c == 's': self.abilities[gg.SNIPER] = mult
      if c == 't': self.abilities[gg.TRAMPLE] = mult
      if c == 'u': self.abilities[gg.SCOUT] = mult
      if c == 'v': self.abilities[gg.VIGILANCE] = mult
      if c == 'w': self.abilities[gg.WALLCRUSHER] = mult
      if c == 'x': self.abilities[gg.HEALER] = mult
      if c == 'y': self.abilities[gg.SPY] = mult
      if c == 'z': self.abilities[gg.WORKER] = mult
      if c == '1': self.abilities[gg.LEADER] = mult
      if c == '3': self.abilities[gg.COMMANDER] = mult
      
    return True
  # end of init_creature()
  
  # init_equipment(): save the values if the card is 'equip' type
  def init_equipment(self, string):
    c = string[0]; line = string[1:]
    if c == 'a': self.card_type = gg.ARMOR;  self.card_type_string = 'armor'
    if c == 'z': self.card_type = gg.WEAPON; self.card_type_string = 'weapon'
    if c == 'x': self.card_type = gg.SPELL;  self.card_type_string = 'spell'
    manacost = line[:line.index('.')]; line = line[line.index('.') +1:]
    name = line[:line.index('.')]; line = line[line.index('.') +1:]
    
    effect1 = line[:line.index('.')]; line = line[line.index('.') +1:]
    self.basic  = self.parse_skill_line(effect1.strip())
    self.kicker = self.parse_skill_line(line.strip())
    
    self.name = name.strip()
    self.manacost = Manacost(manacost)
    return True
  # end of init_equipment()  
      
  # parse_skill_line(): split the whole line of skill definitions to sum of each one of them
  def parse_skill_line(self, string):
    line, ret = string.strip(), []
    while len(line):
      c = line[0]
      if c in ('x', 'X'): a = line.index('}') +1; ret.append(line[:a]); line = line[a:]
      elif c == ';': ret.append(line); line = ''
      else: ret.append(line[:2]); line = line[2:]
    return ret
  # end of parse_skill_line()

  # get_color(): slightly bandit method for purposes of Screen class
  def get_color(self):
    m, colr = self.manacost, ''
    if m.blue:  colr = 'blue'
    if m.black: colr = 'x-black' if colr == '' else 'yBellow'
    if m.red:   colr = 'red'   if colr == '' else 'yellow'
    if m.green:
      if colr == '': colr = 'green'
      else: colr = 'yGellow' if colr == 'red' else 'yellow'
    if m.white: colr = 'white' if colr == '' else 'yellow'
    return 'v-none' if colr == '' else colr
  # end of get_color()
    
  # get_abilities_string(): return the prope keyword for each of abilities; the condition letters are as they appear in data/cards file  
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
  
  # get_effect_casting_cost_string(): traslate the manacost of effect to displayable text
  def get_effect_casting_cost_string(self):
    mc = self.manacost_of_effect
    st = '+'
    if mc.red: st += str(mc.red) + 'red, '
    if mc.green: st += str(mc.green) + 'gre, '
    if mc.blue: st += str(mc.blue) + 'blu, '
    if mc.black: st += str(mc.black) + 'bla, '
    if mc.white: st += str(mc.white) + 'whi, '
    if mc.colorless: st += str(mc.colorless) + 'non, '
    if mc.tap: st += '+tap'
    elif st == '+': st = 'automatic:'
    else: st = st[:-2]
    return st
  # end of get_effect_casting_cost_string()
  
  def identity(self): x = self.idd; return x
  def get_owner(self): x = self.owner; return x
  def get_type(self): x = self.card_type; return x
  def get_type_string(self): x = self.card_type_string; return x
  def get_life(self): x = self.life; return x
  def get_attack(self): x = self.attack; return x
  def get_defense(self): x = self.defense; return x
  def get_shooting(self): x = self.shooting; return x
  def get_movement(self): x = self.movement; return x
  def get_name(self): x = self.name; return x
  def get_subtype(self): x = self.subtyp; return x
  def get_special(self): x = self.special; return x
  def get_abilities(self): x = [o for o in self.abilities]; return x
  def get_abilities_string(self): x = self.abilities_string; return x
  def get_effect(self): x = self.special_effect; return x
  def get_effect_area(self): x = self.area_of_effect; return x
  def get_basic_effect(self):  x = self.basic;  return x
  def get_kicker_effect(self): x = self.kicker; return x
  def get_effect_manacost(): x = self.manacost_of_effect; return x

  def get_number_of_abilities(self):
    a = 0
    if self.get_type() == gg.SQUAD:
      for i in self.abilities:
        if i: a += 1
      if len(self.special_effect): a += 2
    return a

  # clean(): destructor
  def clean(self):
    if self.card_type == gg.CREATURE:
      self.manacost.clean(); del self.manacost
      del self.life
      del self.attack
      del self.defense
      del self.shooting
      del self.movement
      del self.subtyp
      del self.abilities
      del self.abilities_string
      del self.area_of_effect
      del self.special_effect
      self.manacost_of_effect.clean(); del self.manacost_of_effect
      
    if self.card_type in (gg.ARMOR, gg.WEAPON, gg.SPELL):
      del self.basic; del self.kicker

    del self.name
    del self.idd
    del self.owner
    del self.card_type
    del self.card_type_string

    return True
  __initialisation = initialisation
# end of class Card
