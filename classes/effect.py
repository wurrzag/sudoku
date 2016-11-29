from constants import the_file as gg

# Effect: the most important switches of a program including 'change the screen now' switch. Most of them are being deleted (reseted) after first reading of them
# single instance available only in State to force some commands for Manager (game.py)
class Effect:
  def __init__(self):
    self.command = ''
    self.changing_screen = []
    self.table_name = ''
    self.table_arguments = []
    self.table_initialisation_active = False
    self.active_card = None
    return None
  # end of __init__()

  
  def set_new_screen(self, llist): self.changing_screen = [o for o in llist]; return True
  def change_screen(self): x = [o for o in self.changing_screen]; self.changing_screen = []; return x
  def save_values_for_table(self, name, args): self.table_name = name; self.table_arguments = [o for o in args]; return True
  def get_table_name(self): a = self.table_name; self.table_name = ''; return a
  def get_table_args(self): a = [o for o in self.table_arguments]; self.table_arguments = []; return a
  def set_active_card(self, idd): self.active_card = idd; return True
  def get_active_card(self): a = self.active_card; self.active_card = None; return False if a == None else a

  
  
  # clean(): destructor
  def clean(self):
    del self.command
    del self.changing_screen
    del self.table_name
    del self.table_arguments
    del self.table_initialisation_active
    del self.active_card
    return True
# end of Effect class

