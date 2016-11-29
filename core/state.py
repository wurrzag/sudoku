from constants import the_file as gg
from cgame import bf as battlefield
from classes import signal
from classes import parser
from classes import effect

# State: most of program calculations is determined here; includes special screen effects and cursor drawing and movement; means "current STATE of a game"
class State:
  def __init__(self, terminal_instance):
    self.terminal = terminal_instance
    
    self.signal = signal.Signal()
    self.parser = parser.Parser()
    self.effect = effect.Effect()
    self.__aditional_initialisation()
    return None
  def aditional_initialisation(self):
    self.bt_key1_active = True
    self.bt_key2_active = True
    self.bt_key3_active = True
    return True
  # end of __init__()
    
  # create_battlefield(): the battlefield initialisation
  def create_battlefield(self, name1 = '', name2 = ''):
    if name1 == '':
      dn = self.signal.get_decks_names()
      self.battlefield = battlefield.Battlefield(dn[0], dn[1])
    else: self.battlefield = battlefield.Battlefield(name1, name2)
    self.signal.save_the_cards(self.battlefield.get_all_cards())
  def receive_animation(self, instance): self.animation = instance; return True

  def get_signal_instance(self): return self.signal
  def get_parser_instance(self): return self.parser
  def get_effect_instance(self): return self.effect
  #def get_battlefield_instance(self): return self.battlefield
    
  # draw(): draws the dynamic part of screen (cursor ect), lot of the program itself is within this method
  def draw(self, current_state, arg = None):
    key, ani, comm, bt, signal, parser, eff = current_state, self.animation, self.terminal, self.battlefield, self.signal, self.parser, self.effect
    actual_player, cursor = signal.get_whos_on_turn(), signal.get_cursor()
    current_player = bt.get_player(actual_player)
    hand_left_right_buttons_description = 'play the card;next screen buildings;back to battle'
    
    if key == '___Game':
      # default version of battlefield
      if signal.get_battlefield_style() == 'default':
        comm.draw_territory_borders(bt.get_territory_pissings())
        comm.draw_bf_cursor(signal.get_cursor(), signal.get_cursor_color())
        comm.draw_minisoldiers(bt.get_all_gangs())
      # end of default version of battlefield
      # minimap version of battlefield
      if signal.get_battlefield_style() == 'minimap':
        cursor = signal.get_cursor()
        comm.draw_current_field_units(cursor, bt.get_all_gangs('position:' +str(cursor)), bt.fields[cursor].get_type())
      # end of minimap version of battlefield
      if signal.get_battlefield_movement_switch():
        self.command_units_draw(signal.get_battlefield_style())
      self.draw_battlefield_buttons()

      
    elif key == 'Switch_bf_view': signal.switch_battlefield_style()
    
    elif key == '__Hand_right_buildings' or key == '__Hand_left_buildings':
      comm.parse('0505g text buildings')
      comm.draw_main_buttons('23', 'manage the buildings;next screen landsearch;back to battle')

    elif key == '__Hand_right_landsearch' or key == '__Hand_left_landsearch':
      comm.parse('0505l text landsearch')
      comm.draw_main_buttons('23', 'manage the landsearch;next screen (cards);back to battle')
        
    elif key == '___Hand_right' or key == '___Hand_left':
      if key == '___Hand_right': 
        signal.set_which_hand_is_active('right')
        comm.draw_hand(bt.get_player(gg.AWAY), 'right') # right side belongs to AWAY
      if key == '___Hand_left' :
        signal.set_which_hand_is_active('left')
        comm.draw_hand(bt.get_player(gg.HOME), 'left')  #  left side belongs to HOME
      ch = ' '
      if (key == '___Hand_right' and actual_player == gg.AWAY) or (key == '___Hand_left' and actual_player == gg.HOME): # if the player is looking at his own hand...
        ch = ''
        if current_player.hand.length():
          mc = signal.get_card(current_player.hand.get_card(cursor)).manacost    # manacost of card currently under cursor
          if current_player.compare_manacost(mc).red >= 0: ch = '1'              # if he can cast the card, button 1 will be active ## .red is 'for example'. The method returns -1 in all 5 colors if player can't cast the card
      comm.draw_main_buttons(ch +'23', hand_left_right_buttons_description)
    
    elif key == 'spellcasting':
      card_id = eff.get_active_card()
      if type(card_id) == int: times = signal.get_card(card_id).manacost.total
      else: times = 2
      gcl = signal.get_current_player_colors()
      ani.m('cast card', [times, gcl[0], gcl[1]])

    # elif key == '___Info_screen': this screen is debug screen which is meant never to execute in final version of game; hash, unhash or modify whatever you need there
    #
    # to get the info screen displayed, you need to set it as one of exits from one of rooms in classes/parser.py/get_screen_exits()
    # example: "    if key == '___Deckmaking': exits = {gg.ESC: '___Quit', gg.KEY1: '___Game'}"
    # means: if we are in '___Deckmaking' screen, pressing gg.ESC (the what games understand to be 'Escape') goes to '___Quit' screen and pressing gg.KEY1 goes to '___Game' screen
    # the keypresses definition is in comment line above get_screen_exits() and main screens of the game are: '___Game', '___Right_hand', '___Left_hand' and '___Engage'
    # by default, game starts with 0 units in battlefield and 0 mana in both player's hands. That's very unfavorable for testing of unit's movement/fighting.
    # you can change the start-game settings right before the main loop (one line above 'while(len(keyqueue)):' in core/game.py) by unhashing the 'state.battlefield.cheat()' line
    # in cheat() you can modify the details. I hope the methods are self-explaining (player_home.increase_manapool(manacolor), play_card(card_id), Gang.set_position(<0..14>) etc)
    # only if you need some specific cards to be in player's hand at the start, this cannot be done in cheat() but in the constructor itself; look there for two hashed lines with 'draw_card()' phrase
    # ... (and hash the 'proper' lines instead or you will start with 15 cards and they will be displayed in a weird way together as that can't happen during regular gameplay)
    elif key == '___Info_screen':
      comm.parse('0165w text ___Info_screen') # this is how simple print works. 'w' is 'white'

      ## ## ## library, hand, grave... ## ## ##
      hh, hg, ah, ag = bt.get_player(gg.HOME).hand, bt.get_player(gg.HOME).grave2, bt.get_player(gg.AWAY).hand, bt.get_player(gg.AWAY).grave2
      for i in range(hh.length()):
        #idd = hh.get_card(i)
        #card = bt.get_all_cards()[idd]
        #st = str(idd) +card.get_name()
        comm.write(3+ i, 20, [str(hh.get_card(i)) +bt.get_all_cards()[hh.get_card(i)].get_name()], gg.GREEN)
      for i in range(hg.length()): comm.write(3+ i, 35, [str(hg.get_card(i)) +bt.get_all_cards()[hg.get_card(i)].get_name()], gg.RED)
      for i in range(ah.length()): comm.write(3+ i, 50, [str(ah.get_card(i)) +bt.get_all_cards()[ah.get_card(i)].get_name()], gg.LBLUE)
      for i in range(ag.length()): comm.write(3+ i, 65, [str(ag.get_card(i)) +bt.get_all_cards()[ag.get_card(i)].get_name()], gg.BLUE)
      comm.write(2, 20, ['home hand      home grave2    away hand      away grave2    '], gg.VIOLET)
      
      ind = 0
      ## ## ## all active gangs ## ## ##
      for one in bt.get_all_gangs():
        ind += 1
        text = str(one.get_owner()) +' ' +str(one.identity()) +' '  +one.get_name()
        comm.write(ind, 1, [text], gg.WHITE)  
      
      ## ## ## both players gangs ## ## ##
      ind = 10
      for one in bt.gangs.get('owner:home'):
        ind += 1
        text = str(one.get_owner()) +' ' +str(one.identity()) +' '  +one.get_name() +' ' +str(one.get_position())
        comm.write(ind, 20, [text], gg.WHITE)  
      ind = 10
      for one in bt.gangs.get('owner:away'):
        ind += 1
        text = str(one.get_owner()) +' ' +str(one.identity()) +' '  +one.get_name() +' ' +str(one.get_position())
        comm.write(ind, 50, [text], gg.WHITE)

      
    elif key == '___Message_log':
      comm.parse('1010w text ___Message_log')
      #bt.gangs.get()[0].set_position(5)
      
    elif key == 'allgangTablEscreen': self.run_allgangs_table(signal.get_player_battlefield_cursor())
    
    elif key == '___Fight': bt.evaluate_fight()
    
    elif key == '___Deckmaking':
      allc = bt.get_all_existing_cards()
      self.effect.save_values_for_table('list_of_cards', [len(allc), allc, 'horizontal', 'caption:List of all cards'])
      self.effect.set_new_screen(['___Game', 'table'])
    return True
  #end of draw() method

  # get_cursor_change(): this method is responsible for translating the arrow-presses to proper cursor position-changes
  def get_cursor_change(self, room, key):
    ani, bt, cursor, effect, signal = self.animation, self.battlefield, self.signal.get_cursor(), self.effect, self.signal
    return_value, current_player = cursor, bt.get_player(signal.get_whos_on_turn())
    if room == '___Game': # all except default exits key-presses on battlefield screen are checked here
      if key == gg.KEY1 and not self.bt_key1_active: return return_value
      if key == gg.KEY2 and not self.bt_key2_active: return return_value
      if key == gg.KEY3 and not self.bt_key3_active: return return_value
      if key == gg.KEY1:
        if signal.get_battlefield_movement_switch():
          for one in signal.get_currently_commanded_gangs():
            one.set_destination(cursor)
            mask = bt.get_fields_passability(signal.get_whos_on_turn())
            start, movement, color, typewalk = one.get_position(), one.get_movement(), one.get_colorchar(), one.get_typewalk()
            tryy = self.parser.find_path(mask, start, cursor, movement, color, typewalk)
            if tryy: one.set_movement_path(tryy[0])
          signal.set_battlefield_movement_switch(False)
          bt.move_the_lazies()
        else:
          gngs = bt.get_all_gangs('unmoved:whatever' +' position:' +str(cursor) +' owner:' +self.parser.translate_turn(signal.get_whos_on_turn()))
          if not len(gngs): return return_value
          signal.set_battlefield_movement_switch(True)
          signal.set_currently_commanded_gangs(gngs)
      if key == gg.KEY2:
        if signal.get_battlefield_movement_switch():
          signal.set_battlefield_movement_switch(False)
        else:
          effect.set_new_screen(['allgangTablEscreen'])
      if cursor < 9:
        x, y = cursor //3, cursor %3
        if key == gg.UP:   x -= 1
        if key == gg.DOWN: x += 1
        if key == gg.LEFT: y -= 1
        if key == gg.RIGH: y += 1
        if x < 0: self.escape_battlefield('up')
        elif x > 2: self.escape_battlefield('down')
        elif y < 0: return_value = 11 if x else 10
        elif y > 2: return_value = 14 if x else 13
        else: return_value = 3* x +y
        
      else:
        if key == gg.UP:
          if cursor in(11, 14): return_value = cursor -1
          if cursor in (9, 12): return_value = cursor +1
          if cursor == 10: return_value = 0
          if cursor == 13: return_value = 2
        if key == gg.DOWN:
          if cursor in(10, 13): return_value = cursor +1
          if cursor in( 9, 12): return_value = cursor +2
          if cursor == 11: return_value = 6
          if cursor == 14: return_value = 8
        if key == gg.LEFT or key == gg.RIGH:
          if cursor == 12:
            if key == gg.LEFT: return_value = 14
            else: self.escape_battlefield('right')
          if cursor == 9:
            if key == gg.RIGH: return_value = 11
            else: effect.set_new_screen(['___Hand_left'])
          if cursor == 10 or cursor == 11: return_value = 3 if key == gg.RIGH else 9
          if cursor == 13 or cursor == 14: return_value = 5 if key == gg.LEFT else 12
    # end of room ___Game
          
    if room == '___Hand_left' or room == '___Hand_right':
      curr = signal.get_whos_on_turn()
      player = bt.player_home if curr == gg.HOME else bt.player_away
      if (curr == gg.HOME and signal.what_hand() == 'right') or (curr == gg.AWAY and signal.what_hand() == 'left'): return return_value
      bracket = player.hand.length()
      if not bracket: return return_value
      if key == gg.LEFT:
        return_value -= 1
        if return_value < 0: return_value = bracket -1
        signal.set_sub_cursor(-1) # -1 means 'turned off'
      if key == gg.RIGH:
        return_value += 1
        if return_value == bracket: return_value = 0
        signal.set_sub_cursor(-1) # -1 means 'turned off'
        
      if key == gg.KEY1:
        player = bt.player_home if signal.get_whos_on_turn() == gg.HOME else bt.player_away
        card = signal.get_card(player.hand.get_card(cursor))
        mc = card.manacost  # manacost of card currently under cursor
        comp = player.compare_manacost(mc)
        if comp.red >= 0:   # if the card is playable
          effect.set_active_card(card.identity()) # animation will read the manacost later
          bt.play_card(card.identity())
          signal.save_the_animals(bt.get_all_gangs())
          player.load_manapool_from_manacost(comp) # reduce player's manapool by non-colorless part of card's manacost
          pos = 21 if signal.get_whether_to_shift('___Game') else 0
          ani.m("white noise", [6, 8, pos+ 3, 20, pos+ 29, signal.get_current_player_colors()])
          
          dm = self.determined_manaspend(current_player, mc.colorless) # find out whether there is only one way of how to cast the spell (derived from current manapool)
          if dm == '00000':                                            # this return value means the manacost is already determined and paid for
            effect.set_new_screen(['___Game', 'spellcasting'])
          else:                                                        # if not, execute the table where user will choose which mana to spend on this spell
            effect.save_values_for_table('colorless_manacost', [mc.colorless, dm]) # amount of colorless mana to pay and mask of player's manapool goes as the arguments for next table
            effect.set_new_screen(['___Game', 'spellcasting', 'table'])
    # end of rooms ___Hand_left, ___Hand_right

    return return_value
    #end of get_cursor_change()

  # get_sub_cursor_change(): active in case of browsing the cards. subcursor there is a position of ability currently displayed with -1= none of (description of the whole card instead)
  def get_sub_cursor_change(self, room, key):
    signal, bt = self.signal, self.battlefield
    return_value = signal.get_sub_cursor()
    if room == '___Hand_left' or room == '___Hand_right':
      curr = signal.get_whos_on_turn()
      if (curr == gg.HOME and signal.what_hand() == 'right') or (curr == gg.AWAY and signal.what_hand() == 'left'): return return_value
      player = bt.player_home if curr == gg.HOME else bt.player_away
      if not player.hand.length(): return return_value
      bracket = signal.get_card_by_id(player.hand.get_card(signal.get_cursor())).get_number_of_abilities()
      if not bracket: return return_value
      if key == gg.UP:
        return_value -= 1
        if return_value < 0: return_value = bracket -1
        #signal.set_sub_cursor(0)
      if key == gg.DOWN:
        return_value += 1
        if return_value == bracket: return_value = 0
        #signal.set_sub_cursor(0)
    return return_value
  # end of get_sub_cursor_change()  
  
  # escape_battlefield(): the definition of where should program go when player escapes from the battlefield one of four basic directions
  def escape_battlefield(self, direction):
    dirr, signal, effect, bt = direction, self.signal, self.effect, self.battlefield
    if dirr == 'right': effect.set_new_screen(['___Hand_right'])
    if dirr == 'left' : effect.set_new_screen(['___Hand_left'])
    if dirr == 'up'   : effect.set_new_screen(['___Fight'])
    if dirr == 'down' : effect.set_new_screen(['___Fight'])
      
    return True
  
  # run_allgangs_table(): the setting for one of most difficult tables in the game
  def run_allgangs_table(self, cursor_position = -1):
      cp, bt, turn, signal = cursor_position, self.battlefield, self.signal.get_whos_on_turn(), self.signal
      allg = bt.get_all_gangs()
      shift = 'shift_it' if turn == gg.HOME else ''
      current_player = 'player:home' if turn == gg.HOME else 'player:away'
      self.store_passability()
    
      table_position = -1
      if cp != -1:
        field_gangs = bt.get_all_gangs('position:' +str(cp))
        for i in range(len(field_gangs)):
          one = field_gangs[i]
          if one.get_owner() == turn: table_position = one.get_id()
          if one.get_owner() == turn: break
        if len(field_gangs) and table_position == -1: table_position = field_gangs[0].get_id()
    
      posit = '' if table_position == -1 else 'jump_to:' +str(table_position)
      
      if not allg: effect.set_new_screen(['___Game', 'no_visible_units'])
      else:
        self.effect.save_values_for_table('list_of_gangs', [len(allg), allg, 'vertical', 'caption:Select the gang to command', shift, current_player, posit])
        self.effect.set_new_screen(['___Game', 'command_the_gang', 'table_shifted'])
  # end of run_allgangs_table()
  
  # store_passability(): synchronising the passability mask in Battlefield and Signal
  def store_passability(self):
    bt, plr = self.battlefield, self.signal.get_whos_on_turn()
    self.signal.set_passability_mask(bt.get_fields_passability(plr))
    #pars.find_path(mask, 12, 9, 2, 'x-black', 'swampwalk')
    return True

  # set_new_turn(): the mechanism of turns-switching is done here  
  def set_new_turn(self):
    sig = self.signal
    sig.switch_whos_on_turn()
    bt, curr = self.battlefield, sig.get_whos_on_turn()
    bt.set_current_turn(curr)
    bt.get_player(curr).refresh()
    bt.refresh()
    return True
  
  # set_starting_turn(): setting some values to default at the beginning of a game
  def set_starting_turn(self, home_or_away):
    bt, sign, who = self.battlefield, self.signal, home_or_away
    sign.set_starting_turn(who)
    bt.set_current_turn(who)
    bt.get_player(gg.HOME).refresh(), bt.get_player(gg.AWAY).refresh()
    return True
  
  # determined_manaspend(): finds out whether the card can be played automatically (player can't choose, what mana to spend as there is no choices to it)
  def determined_manaspend(self, player, colorless_mana):
    pool, mana = player.count_mana(), colorless_mana
    def banzai(x): return True if x > 0 else False
    if mana == 0: return '00000'
    if mana == pool: player.null_manapool(); return '00000'
  
    mask_string, mask_binary, pool_colored, manatext = '', [], player.get_mana(), ['red', 'green', 'blue', 'black', 'white']
    for i in range(5):mask_string += str(pool_colored[i]) ; mask_binary.append(banzai(pool_colored[i]))
    if mask_binary.count(True) == 1: player.spent_mana(manatext[mask_binary.index(True)], mana); return '00000'
    return mask_string
  # end of determined_manaspend()
  
  # draw_battlefield_buttons(): drawings of the three main buttons of a game
  def draw_battlefield_buttons(self):
    active, description, signal, comm, bt = '', '', self.signal, self.terminal, self.battlefield
    field, turn = signal.get_cursor(), signal.get_whos_on_turn()
    
    h, a = self.parser.translate_turn(turn), self.parser.translate_turn(turn, 'negate')
    hm, aw = bt.get_all_gangs('owner:' +str(h) + ' position:' +str(field)), bt.get_all_gangs('owner:' +str(a) + ' position:' +str(field))
    if signal.get_battlefield_movement_switch():
      comm.draw_main_buttons('123', 'move unit here;cancel the movement;switch battlefield style of view')
    else:
      temp = ''
      #if bt.is_there_combat(field): description = 'cannot move engaged unit'; self.bt_key1_active = False
      if   len(hm) and len(aw): description = 'cannot move engaged unit'; self.bt_key1_active = False
      elif len(aw):
        self.bt_key1_active = False; description = 'not yours soldier'
        if len(aw) >1: description = description + 's'
      elif len(hm):
        hmm = bt.get_all_gangs('owner:' +str(h) + ' position:' +str(field) + ' unmoved:whatever')
        if len(hmm):
          self.bt_key1_active = True; active = '1'
          description = 'command the unit' if len(hmm) == 1 else 'move all units of this sector'
        else: description = 'unit already moved'; self.bt_key1_active = False
      else: self.bt_key1_active = False; temp = 'details of all visible gangs' # description empty
      if temp == '':
        temp = 'details of th'
        if len(bt.get_all_gangs('position:' +str(field))) > 1: temp += 'ese units'
        else: temp += 'is unit'
      
      active += '23'; description += ';'+ temp +';switch battlefield style of view'
    
      comm.draw_main_buttons(active, description)
      #comm.draw_main_buttons('123', ';select one specific unit;switch battlefield style of view')
    return True
  # end of draw_battlefield_buttons()
  
  # command_units_draw(): drawing of specialised cursor (in form of walkable path) in case the program is in "command the units" phase
  def command_units_draw(self, style):
    styl, comm, parser, signal, effect, bt = style, self.terminal, self.parser, self.signal, self.effect, self.battlefield

    gngs = signal.get_currently_commanded_gangs()
    start, cursor = gngs[0].get_position(), signal.get_cursor()
    color, typewalk = 'blue', 'normal'
    #pars.find_path(mask, 12, 2, 2, 'x-black', 'swampwalk')
    mask = bt.get_fields_passability(signal.get_whos_on_turn())
    for i in range(len(gngs)):
      movement, color, typewalk = gngs[i].get_movement(), gngs[i].get_colorchar(), gngs[i].get_typewalk()
      tryy = parser.find_path(mask, start, cursor, movement, color, typewalk)
      if tryy: comm.draw_chosen_path(tryy[0], tryy[1], styl)
    return True
  # end of command_units_draw()
   
  # clean(): destructor  
  def clean(self):
    self.battlefield.clean(); del self.battlefield
    self.signal.clean(); del self.signal
    self.parser.clean(); del self.parser
    self.effect.clean(); del self.effect
    del self.bt_key1_active
    del self.bt_key2_active
    del self.bt_key3_active
    return True
  __aditional_initialisation = aditional_initialisation
# end of class State
