from constants import the_file as gg

# Field: the game is played at the territory consisting of 15 Fields. More details in Battlefield constructor
class Field:
  def __init__(self, idd, owner, terrain):
    self.idd     = idd
    self.owner   = owner
    self.terrain = terrain
    return None
  
  def set_owner(self, o): self.owner = o
  def get_owner(self): x = self.owner; return x
  def get_type(self) : x = self.terrain; return x
  def identity(self) : x = self.idd; return x

  # clean(): destructor
  def clean(self):
    del self.idd; del self.owner; del self.terrain
    
    return True
# end of class Field

