from constants import the_file as gg

# this class serves as list of all units (gangs) in game;
# dead units have a coord of -1; they can never live again
class Gang_list:
  def __init__(self):
    self.ll = []    # list of gangs
    return None
  
  def add(self, gang): self.ll.append(gang); return True
  def get_all(self): return [o for o in self.ll]
  def length(self): a = len(ll); return a

  def get(self, command = ''):
    llist, com = [], command
    for i in range(len(self.ll)):
      if self.ll[i].get_position() >= 0 and self.ll[i].get_position() < gg.IN_QUEUE_BORDER: # append only live units. they can be recreated (from the same card) but not resurrected
        llist.append(self.ll[i])
    return llist if command == '' else self.filtr(com, llist)
  
  def filtr(self, text, llist): 
    pars = Gang_parser(text, llist)
    ret = pars.e(); pars.clean(); del pars
    return ret

  # clean(): destructor
  def clean(self):
    #for one in self.ll: one.clean() # batllefield is doing that so it can't be here
    del self.ll
    
    return True
# end of class Gang_list

# create-and-run-once help-class of Gang_list
class Gang_parser:
  def __init__(self, command, ganglist):
    self.meth = command
    self.llist = ganglist
    return None
  
  # e(): the 'run' method which somehow includes all the other member methods
  def e(self):
    ret, doubles = [], []
    for one in self.meth.split(): # == upgraded: split(' ')
      two = one.split(':'); doubles.append([two[0], two[1]])
    for gang in self.llist:
      good = True
      for command in doubles:
        key, val = command[0], self.translate_parameter(command[1])
        if key == 'position' and val != gang.get_position(): good = False
        if key == 'owner': 
          if val == 'home' and gang.get_owner() == gg.AWAY: good = False
          if val == 'away' and gang.get_owner() == gg.HOME: good = False
        if key == 'unmoved' and not gang.get_current_movement(): good = False
          
      if good: ret.append(gang)
    return ret
  # end of e()
  
  # translate_parameter(): converts text to whatever type
  def translate_parameter(self, parameter):
    def isnum(t):
      for i in range(len(t)):
        o, a, z = ord(t[i]), ord('0'), ord('9')
        if o < a or o > z: return False
      return True

    def istext(what):
      t = what.upper()
      for i in range(len(t)):
        o, a, z = ord(t[i]), ord('A'), ord('Z')
        if o < a or o > z: return False
      return True
  
    p = parameter
    if p == 'True': return True
    if p == 'False': return False
    if isnum(p): return int(p)
    if istext(p): return p
    print('\n\nSomething wrong in glist.py.translate_parameter():' +str(type(p))); gg.getch()

    return None
  # end of translate_parameter()

  # clean(): destructor
  def clean(self):
    del self.meth
    del self.llist
    return True
# end of class Gang_parser
