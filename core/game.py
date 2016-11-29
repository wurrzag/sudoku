from constants import the_file as gg

from . import state
from . import screen
from classes import table

# Manager: the main loop of a game; assures the synchronisation of screendraw and keys pressing
class Manager:
  def __init__(self):
    self.terminal = screen.Screen()
    self.gamestate = state.State(self.terminal)

    gs = self.gamestate
    self.signal = gs.get_signal_instance()
    self.parser = gs.get_parser_instance()
    self.effect = gs.get_effect_instance()
    self.animation = self.terminal.get_animation_instance()
    
    self.terminal.create_signal(self.signal)
    self.terminal.create_parser(self.parser)
    self.gamestate.receive_animation(self.animation)
    
    self.table = table.Table(self.terminal, self.signal)
    # DONT MOVE THESE LINES
    
    #self.battlefield = gs.get_battlefield_instance()
    return None
  # end of __init__()
  
  # run() - this is where the whole game is
  def run(self):
    pars, comm, signal, state, effect, table  = self.parser, self.terminal, self.signal, self.gamestate, self.effect, self.table
    #keyqueue = ['___Start']
    #keyqueue = ['___Game']
    keyqueue = ['___Game', 'invitation', 'ridiculous']
    #keyqueue = ['___Hand_right']
    #signal.switch_battlefield_style()
    
    state.create_battlefield()
    
    self.gamestate.battlefield.cheat() # DON'T HASH THIS LINE. PLAYERS WILL NOT HAVE MANA and mana cards are not developed yet, so they will not be able to cast any card at all
    self.cheat(); # HASH THIS LINE TO GET EMPTY BATTLEFIELD as a starting point of game (note: you have lot of cards in hand then and the game will crash once you have more than 14 of them so don't just switch turns, if you choose this option. you can decrease the number of cards in both hands at the start in constructor of Battlefield (look for '7 cards' string))
    state.set_starting_turn(gg.AWAY)   # must be after cheat... (can be gg.HOME or gg.AWAY)

    for one in pars.all_paths: print(one)  # list of all predefined walk-through-battlefield paths
    #self.print_path_masks()               # list of fields accessibility indexes (home, away)
    
    mask = self.gamestate.battlefield.get_fields_passability(self.signal.get_whos_on_turn())
    pars.find_path(mask, 12, 2, 2, 'x-black', 'swampwalk') # mask, start, destination, movement_value, creature_color, creature_type_of_movement
    #gg.getch()


    # THE MAIN LOOP starts here    
    while(len(keyqueue)):
      key = keyqueue[-1]   # last item on a queue means the current one state of game
      signal.set_current_state_of_game(key)  # synchronisation with signal...
      current_state = pars.e(key, 'get screen exits') # get the information of what is available at this screen
      if not current_state: break
      exits = []; other = []   # all normal and special exits from given screen
      for c in current_state:
        if c < gg.FIRST_BORDER: exits.append(c)
        else: other.append(c)
        
      if key == '___Other_player_turn': state.set_new_turn() # calling the beginning of turn processes if the turn begins

      prev = signal.get_previous_state()
      # remembering the position of battlefield cursor for each player
      if key != '___Game' and prev == '___Game':
        signal.set_player_battlefield_cursor()
        if key != 'Switch_bf_view': signal.set_battlefield_movement_switch(False) # if you command the gang, all other than 'changing the battlefield style of view' screen will cancel the command
      if key == '___Game' and prev != '___Game': signal.set_cursor(signal.get_player_battlefield_cursor())

      # reseting both cursors if we are in new screen (different from previous one)
      elif key != prev: signal.set_cursor(0); signal.set_sub_cursor(-1)
      
      
      signal.set_previous_state(key) # remembering the previous state for the procedures at the beginning of a loop
      new_state = '' # setting new_state to default to see whether it is something different at the end of turn
      
      if 'table' in key:
        name, command = effect.get_table_name(), effect.get_table_args()
        if name != '': res = self.run_table(name, command)   # executing the table
        if type(res) == str: new_state = res # if string was returned by table, it is a new state demand
      
      
      if not gg.DONT_RESET_SCREEN in other: comm.reset()
      #else: comm.comm.resetcolor() #current_state[DONT_RESET_SCREEN])
      if not gg.DONT_DRAW_SCREEN in other:
        comm.draw_screen(key)  # drawing the static part of screen (ie part without arguments from Battlefield needed)
        state.draw(key)        # drawing the other half (it calls the Screen (self.comm) anyway); the state's draw() method includes some system-values-changing procedures in case of special screens made for that purpose within it
        if signal.get_whether_to_shift(key): comm.comm.rshift(21) # majority of screens is distinguishing HOME or AWAY player's turn by shifting the three main buttons to left(HOME) side of screen and shifting the rest of screen appropriatelly
        comm.go()

      if not gg.DONT_PAUSE in other: press = pars.e(gg.getch(), 'char -> keyboard command') # waits for any key to be pressed
      # 'DONT_PAUSE' must always be combined with 'ALL' in Parser.get_screen_exits(), otherwise it will not read the keyboard and not switch the state and therefore the loop will freeze
      # it is no problem to have there 'ALL' alone. That's the case of all 'click to continue' screens as the matter of fact
      if gg.ALL in exits: new_state = current_state[gg.ALL] # if ALL switch is set, whatever key triggers new state
      elif press in exits: new_state = current_state[press] # if not, any of 'exit buttons' can do so as well
      else:                                                 # third option is arrows-movement
        
        signal.set_sub_cursor(state.get_sub_cursor_change(key, press)) # sub cursor movement must be executed before cursor movement because cursor might force the whole screen (and bunch of (sub)cursor-movement vital system variables) to change but sub cursor can't
        now, then = signal.get_cursor(), state.get_cursor_change(key, press) # finding out whether the key pressed is one of cursor keys
        if now != then:               # if the keypress actually changed the main cursor position
          signal.set_cursor(then)     # cursor change based on keypress
          signal.set_sub_cursor(-1)   # reset the subcursor (other card, gang or field have other abilities and value from previous sub cursor position might crash the program)
                    
      if len(new_state):              # if new state has been triggered...
        if new_state == '<--': keyqueue = keyqueue[:-1]                # if '<--' string is defined as new state, it means the screen removes itself from queue (and the previous screen in queue is on turn now)
        elif new_state.strip('_')[0].isupper(): keyqueue = [new_state] # if the name of state starts with big letter, it is meant to be alone in new queue
        else: keyqueue.append(new_state)                               # otherwise the new state is appended to the end of queue

      interrupt = effect.change_screen();                  # checking whether there is interrupt style of change screen demand
      if len(interrupt): keyqueue = [o for o in interrupt] # and executing it if so

    # end of main loop
    return True
  # end of run()  
  

  # run_table(): executes the table
  def run_table(self, name, command):
      ani, tab, comm, pars, bt, signal, effect = self.animation, self.table, self.terminal, self.parser, self.gamestate.battlefield, self.signal, self.effect
      tab.locate_point_of_program(name, command)
      tab.reset()
      while(7):
          tab.fix_cursor()
          comm.reset()
          tab.draw()
          if tab.get_whether_to_shift(): comm.comm.rshift(21)
          if name == 'list_of_cards':
              comm.comm.dshift(2)
              comm.draw_main_buttons('123', 'escape;escape;escape')
          comm.go()
          if tab.run(pars.e(gg.getch(), 'char -> keyboard command')): break
          tab.set_system_cursor()
        
      return self.eval_table(name, tab.get_final_result())
  # end of run_table()
  
  # eval_table(): make after-table effects based on table's results
  def eval_table(self, name, arg):
    signal, bt, res = self.signal, self.gamestate.battlefield, self.table.get_final_result()
    if name == 'colorless_manacost':
      bt.get_player(signal.get_whos_on_turn()).load_manapool_from_array([o for o in arg]) # reducing mana spent within the table from manapool
    if name == 'list_of_gangs':
      boo, gng = res[0], res[1]
      if boo:
        signal.set_currently_commanded_gang(gng)
        signal.set_battlefield_movement_switch(True) # if some the unit was chosen, the game switches to "setting the movement of unit" mode
      signal.set_player_battlefield_cursor(gng.get_position())
      
    return True
  # end of eval_table()


  # cheat(): temporal method for setting some more interresting Battlefield situation than empty fields and no mana for players
  def cheat(self):
    self.gamestate.set_starting_turn(gg.HOME)
    self.gamestate.battlefield.cheat('home')    
    self.gamestate.set_starting_turn(gg.AWAY)
    self.gamestate.battlefield.cheat('away')
    return True

  # print_path_masks(): temporal method; printing informations only
  def print_path_masks(self):
    print('HOME HOME HOME'); gg.getch()
    self.gamestate.battlefield.get_fields_passability(self.signal.get_whos_on_turn())
    print('AWAY AWAY AWAY'); gg.getch()
    awawaw = gg.HOME if self.signal.get_whos_on_turn() == gg.AWAY else gg.AWAY
    self.gamestate.battlefield.get_fields_passability(awawaw)
    gg.getch()
    return True


  def clean(self):
    self.terminal.clean(); del self.terminal
    self.gamestate.clean(); del self.gamestate
    self.table.clean(); del self.table
    return True
# end of Manager class
