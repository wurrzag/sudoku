from constants import the_file as gg
from random import randint

# Card_list: this class serves as library, hand and grave for both players
class Card_list:
  def __init__(self):
    self.ll = [] # list of integers. every integer is unique id among the cards in game
    return None
  
  def add(self, card_id): self.ll.append(card_id); return True
  def remove(self, card_id): self.ll.remove(card_id); return True
  def get(self): return [o for o in self.ll]
  def length(self): return len(self.ll)

  # draw_a_card(): removes the random card from library and parent method adds it to hand
  #
  #                it is used to move a random card from any list to any list 
  #                all lists in the game are:
  #                (2x library, 1x hand, 2x grave) x 2  # (... 2 players)
  def draw_a_card(self):
    card = self.ll[randint(0, len(self.ll) -1)]
    return self.draw_a_card_by_id_number(card)
  # parent method will use directly this method to move given-id element from somewhere to anywhere else too
  def draw_a_card_by_id_number(self, card): self.remove(card); return card

  def get_card(self, pos): x = self.ll[pos]; return x
  
  # clean(): destructor
  def clean(self):
    del self.ll # battlefield is cleaning all cards one by one...
    return True
# end of class Card_list


# one of parameters of every card
class Manacost():
  def __init__(self, string = ''):
    self.white, self.green, self.blue, self.red, self.black, self.colorless,     self.wood, self.gold, self.food, self.tap = 0,0,0,0,0,0,   0,0,0,False
    for c in string:
      multiplier = 1 if c.islower() else 2 # big letter means 2 mana of given color
      c = c.lower()
      if c == 'g': self.green += multiplier
      if c == 'w': self.white += multiplier
      if c == 'u': self.blue += multiplier
      if c == 'b': self.black += multiplier
      if c == 'r': self.red += multiplier
      if c == 'x': self.colorless += multiplier
      
      if c == 'f': self.wood += 5* multiplier # one letter in cards definition file means 5 or 10 of these
      if c == 's': self.gold += 5* multiplier
      if c == 'p': self.food += 5* multiplier
      if c == 't': self.tap = True
      
    self.total = self.green + self.white + self.blue + self.red + self.black + self.colorless
    return None
  
  #def null(self):
  #  self.white, self.green, self.blue, self.red, self.black, self.colorless,     self.wood, self.gold, self.food = 0,0,0,0,0,0,   0,0,0
  #  self.total = 0
  #  return True
  
  def clean(self):
      del self.green
      del self.white
      del self.blue
      del self.black
      del self.red
      del self.colorless
      del self.wood
      del self.gold
      del self.food
      del self.total
      return True
  #end of class Manacost
