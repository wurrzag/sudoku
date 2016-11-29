from constants import the_file as gg

from myconsole import terminal
from . import anim as animation
from . import text as textures
from classes import shelp as hlp

# Screen: the majority of all screen-draw is here; includes handy parse() method allowing the more sophisticated style of drawing commands, also reading them from whatever file
class Screen:
  def __init__(self):
    self.textures = textures.Textures()
    self.comm = terminal.Console()
    self.animation = animation.Animation(self.comm, gg.ANIMATION_SPEED)
    self.hlp = hlp.Help()
    return None
 
  def create_signal(self, instance): self.signal = instance; return True
  def create_parser(self, instance): self.parser = instance; return True
  def get_animation_instance(self): return self.animation
  
  def reset(self): return self.comm.reset()
  def go(self): return self.comm.run()
  def write(self, x, y, pattern, color): return self.comm.load_object(x, y, pattern, color)

  # draw_screen(): crossroad of what screen is supposed to draw; the State have it too...
  def draw_screen(self, state_name, arg = None):
    key = state_name
    if key == '___Start': self.parse('.start') # ; self.draw_table()
    elif key == '___Deckmaking': self.parse('.deckmaking')
    elif key == '___Game': self.draw_battlefield()
    elif key == '___Fight': self.draw_fight()
    elif key == '___Other_player_turn': self.draw_switch_turns_message()
    elif key == '___Quit': self.parse('1222w text press any key to exit game')
    elif key == '___Quit_for_real': self.parse('1226b text thanks for playing')
    elif key == 'no_visible_units': self.parse('1227w text no visible units')
    elif key == 'invitation': self.invitation()
    elif key == 'ridiculous': self.parse('.ridiculous')
    return True
  # end of draw_screen()
    
  def get_texture(self, name, p1 = None, p2 = None): return self.textures.get(name, p1, p2)
  
  # various - help methods of parse_line()
  def draw(self, x, y, text, clr, random = False): return self.parse(self.make_line(x, y, text, clr, random)) if random else self.parse(self.make_line(x, y, text, clr))
    
  def make_line(self, x, y, text, colorchar, random = False):
    if type(random) != bool and type(random) != int: return None
    l  = str(x) if x >= 10 else '0'+ str(x)
    l += str(y) if y >= 10 else '0'+ str(y)
    l += colorchar + ' ' + text
    if type(random) == int: l += str(random)
    return l

  def parse(self, what):
    if not len(what): return False
    elif what[0] == '.': self.parse_file('./screens/' + what[1:])
    else: self.parse_line(what)
    return True
  
  def parse_file(self, filename):
    with open(filename, 'r') as whatfile:
      for line in whatfile:
        self.parse_line(line)
    return True
  
  # parse_line(): allows specifically formatted text to be accepted as a input for terminal. for example
  # '0508g thing' means: draw the 'thing' on coords [5, 8] by 'g'reen color ## 'thing' is either a keyword ('box 1020', 'text hello world') or name of texture ('swamp_pattern_1'). Color byte can be ' ' for default color
  # '.first' means read more lines from ./screens/first and 'COLOR w' means set default color to 'w'hite. There are no more commands.
  def parse_line(self, phrase):
    hl, line = self.hlp, phrase.strip() + ' '
    #print('---' + line + '---')
    if len(line) < 2 or line[0] == '#': return False
    if 'COLOR' in line: self.comm.setcolor(hl.what_color(line[6])); return True
    # reading desired color and coordinates from phrase
    row, col = 10* int(line[0]) + int(line[1]), 10* int(line[2]) + int(line[3])
    colour = hl.what_color(line[4])
    line = line[6:]; wd = line[:line.find(' ')] # reading the first word
    # checking for keywords (whether the first word is a command)
    if wd == 'text': self.write(row, col, [line[5:-1]], colour)
    elif wd == 'box': line = line[4:]; x, y = 10* int(line[0]) + int(line[1]), 10* int(line[2]) + int(line[3]); self.write(row, col, self.textures.get('box', x, y), colour)
    elif wd == 'boxempty': line = line[9:]; x, y = 10* int(line[0]) + int(line[1]), 10* int(line[2]) + int(line[3]); self.write(row, col, self.textures.get('boxempty', x, y), colour)
    elif wd == 'boxfat': line = line[7:]; x, y = 10* int(line[0]) + int(line[1]), 10* int(line[2]) + int(line[3]); self.write(row, col, self.textures.get('boxfat', x, y), colour)
    elif wd == 'h-line': line = line[7:]; y = 10* int(line[0]) + int(line[1]); self.write(row, col, self.textures.get('h-line', y), colour)
    elif wd == 'v-line': line = line[7:]; x = 10* int(line[0]) + int(line[1]); self.write(row, col, self.textures.get('v-line', x), colour)
    elif wd == 'corner-cross': self.write(row, col, ['┼'], colour)
    elif wd == 'corner-ul': self.write(row, col, ['┌'], colour)
    elif wd == 'corner-ur': self.write(row, col, ['┐'], colour)
    elif wd == 'corner-dl': self.write(row, col, ['└'], colour)
    elif wd == 'corner-dr': self.write(row, col, ['┘'], colour)
    elif wd == 'corner-Tl': self.write(row, col, ['┤'], colour)
    elif wd == 'corner-Tr': self.write(row, col, ['├'], colour)
    elif wd == 'corner-Tu': self.write(row, col, ['┴'], colour)
    elif wd == 'corner-Td': self.write(row, col, ['┬'], colour)
    elif wd == 'arrow-r':
      line = line[8:]; ln = 10* int(line[0]) + int(line[1])
      self.write(row -1, col +ln -2, ['\\ ', ' >', '/ '], colour)
      self.write(row, col, self.textures.get('h-2line', ln -1), colour)
    elif wd == 'arrow-l':
      line = line[8:]; ln = 10* int(line[0]) + int(line[1])
      self.write(row -1, col -ln, [' /', '< ', ' \\'], colour)
      self.write(row, col -ln +1, self.textures.get('h-2line', ln -1), colour)
    elif wd == 'arrow-u':
      line = line[8:]; ln = 10* int(line[0]) + int(line[1])
      self.write(row -ln, col -1, [' ^ ', '/ \\'], colour)
      self.write(row -ln +1, col, self.textures.get('v-2line', ln -1), colour)
    elif wd == 'arrow-d':
      line = line[8:]; ln = 10* int(line[0]) + int(line[1])
      self.write(row +ln -2, col -1, ['\\ /', ' v '], colour)
      self.write(row, col, self.textures.get('v-2line', ln -1), colour)
    elif wd == 'h-double-line': line = line[14:]; y = 10* int(line[0]) + int(line[1]); self.write(row, col, self.textures.get('h-2line', y), colour)
    elif wd == 'v-double-line': line = line[14:]; x = 10* int(line[0]) + int(line[1]); self.write(row, col, self.textures.get('v-2line', x), colour)
    elif wd == 'h-triple-line': line = line[14:]; y = 10* int(line[0]) + int(line[1]); self.write(row, col, self.textures.get('h-3line', y), colour)
    elif wd == 'v-triple-line': line = line[14:]; x = 10* int(line[0]) + int(line[1]); self.write(row, col, self.textures.get('v-3line', x), colour)
  
    # if the first word is not a command, it is a key of a texture
    else: self.write(row, col, self.textures.get(wd), colour)
    return True
  # end of parse_line()
  
  # draw_main_buttons(): draw the three buttons either empty or full
  def draw_main_buttons(self, which_ones = '', text = ''):
    hl = self.hlp
    w, t, sw1, sw2, sw3 = which_ones, text, False, False, False
    if '1' in w: sw1 = True
    if '2' in w: sw2 = True
    if '3' in w: sw3 = True
    #self.parse('0565g text here we go')
    #self.write(7, 65, hl.justify('hello world this is really nice day today', 12), gg.GREEN)
    t1 = t[:t.find(';')]; t  = t[t.find(';') +1:]
    t2 = t[:t.find(';')]; t3 = t[t.find(';') +1:]
    j1, j2, j3 = hl.justify(t1, 10), hl.justify(t2, 10), hl.justify(t3, 10)    
    if sw1: self.parse('0160g button_1'); self.write( 5 -len(j1) //2, 69, j1, gg.GREEN)
    else  : self.parse('0160x button_empty'); self.write( 5 -len(j1) //2, 69, j1, gg.GRAY)
    if sw2: self.parse('0960y button_2'); self.write(13 -len(j2) //2, 69, j2, gg.YELLOW)
    else  : self.parse('0960x button_empty'); self.write(13 -len(j2) //2, 69, j2, gg.GRAY)
    if sw3: self.parse('1760l button_3'); self.write(21 -len(j3) //2, 69, j3, gg.LBLUE)
    else  : self.parse('1760x button_empty'); self.write(21 -len(j3) //2, 69, j3, gg.GRAY)
    return True
  # end of draw_main_buttons()
  
  # draw_manasymbol(): draws one of three versions of manasymbol
  def draw_manasymbol(self, coord1, coord2, what_size, colour): # what_size is supposed to be 'small', 'big' or 'full'
    hl = self.hlp
    mx, my, size, color = coord1, coord2, what_size, colour
    plains = '..,\'"`°°°°°º·····×»«ⁿⁿ'
    forest  = 'αßπσμτΦΘΩδ∞φε√∩'
    swamp, river = '░▒▒▒▓▓', '≡≈≈≈≈≈≈'
    dull, mini, gray = ' ', '█', '▒'
    
    if color == gg.RED and (size == 'full' or size == 'big'):
      if size == 'big':
        self.write(mx-1, my-1, self.textures.get('box', 3, 6), color)
        self.write(mx, my, self.textures.get('mountain_small'), gg.RED)
      if size == 'full':
        self.write(mx-1, my-1, self.textures.get('boxfat', 3, 6), color)
        self.write(mx, my, self.textures.get('mountain_small'), gg.RED)
    
    elif size == 'full' or size == 'big':
      if   color == gg.WHITE:  pattern = plains
      elif color == gg.VIOLET: pattern = swamp; color = gg.GRAY
      elif color == gg.BLUE:   pattern = river
      elif color == gg.GREEN:  pattern = forest
      if what_size == 'big':
        self.write(mx-1, my-1, self.textures.get('box', 3, 6), color)
        self.draw_field(mx, my, 1, 4, pattern, color)
      elif what_size == 'full':
        self.write(mx-1, my-1, self.textures.get('boxfat', 3, 6), color)
        self.draw_field(mx, my, 1, 4, pattern, color)

    elif what_size == 'small':
      if color == gg.VIOLET: self.draw_field(mx, my, 2, 2, gray, gg.WHITE)
      elif color == gg.GRAY: self.write(mx, my, ['┌┐','└┘'], gg.GRAY)
      #elif color == gg.GRAY: self.write(mx, my, ['▄▄', '▀▀'], gg.GRAY)
      else: self.draw_field(mx, my, 2, 2, mini, color)
      
    else: print("\n\nscreen.py.draw_manasymbol: wrong size. must 'big', 'small' or 'full'\n"); return False
    return True
  # end of draw_manasymbol()
  
  # draw_card(): draws the one card in big format (which is the only one available)
  def draw_card(self, whatcard):
    card, hl, mc = whatcard, self.hlp, whatcard.manacost
    pos, subcursor = 12, self.signal.get_sub_cursor()
    # edges and name of card
    color = card.get_color(); inver = 'x' if color == 'x-black' else color.capitalize()[0]
    self.parse('0601' + inver[0] +' boxfat 1630')
    self.parse('0702' + color[0] +' boxempty 1428')
    self.parse('0702' + color[0] +' box 0428')
    self.write(7, 4, [' '+ card.get_name() +' '], hl.what_color(color[0]))
    st = ' '+ card.get_subtype() +' ' if card.get_type() == gg.SQUAD else ' '+ card.get_type_string() +' '
    pos = 5
    self.write(10, 28 - len(st), [st], hl.what_color(color[0]))
    # drawings of casting cost
    if mc.total == 9: pos -= 2
    for i in range(mc.white): self.draw_manasymbol(8, pos, 'small', gg.WHITE); pos += 3
    for i in range(mc.red): self.draw_manasymbol(8, pos, 'small', gg.RED); pos += 3
    for i in range(mc.green): self.draw_manasymbol(8, pos, 'small', gg.GREEN); pos += 3
    for i in range(mc.blue): self.draw_manasymbol(8, pos, 'small', gg.BLUE); pos += 3
    for i in range(mc.black): self.draw_manasymbol(8, pos, 'small', gg.VIOLET); pos += 3
    for i in range(mc.colorless): self.draw_manasymbol(8, pos, 'small', gg.GRAY); pos += 3
    # the rest
    t = card.get_type()
    if t == gg.SQUAD: self.draw_card_summon(card, subcursor)
    if t in (gg.WEAPON, gg.ARMOR, gg.SPELL): self.draw_card_equip(card)
    
    return True
  # end of draw_card()

  # part of draw_other_half_of_card() - help method of following methods
  def print_description(self, definition_line, colorr):
            hl = self.hlp
            text, shrink, color, a = [], -2, colorr, definition_line
            while(len(text) < 5):
                shrink += 2
                text = hl.justify(a, 19 - shrink)
                if shrink >= 10: break              
            spaces = 12 // len(text) -1 if len(text) else 0
            text = hl.insert_empty_lines(text, spaces)
            txt2 = []
            for one in text: txt2.append(one.replace('_', ' '))
            self.write(9, 34 + shrink //2, txt2, hl.what_color(color))
            return True

  # draw_other_half_of_card(): continuation of draw_card() (the flavor text area)
  def draw_other_half_of_card(self, type_of_operation, textkey, colorr):
    hl, code, namefull, name, color = self.hlp, type_of_operation, textkey, self.hlp.cut_numbers_from_string(textkey), colorr
    self.parse('0732' + color + ' box 1523')
    self.write(7, 35, [' '+ name +' '], hl.what_color(color))
    if code == 'ability':
      if(name[0] == '+'): self.print_description(hl.translate_skill_manacost(namefull), gg.VIOLET)
      else:
        with open('./data/abilities') as abi:
          for a in abi:
            if name == a[:a.find(' ')]: self.print_description(a[a.find(' ') +1:], gg.GRAY)
          
    if code == 'card':
      output = ''
      with open('./txt/cards/'+ name.replace(' ', '_')) as description:
        for a in description: output += a + ' '
      self.print_description(output.replace('\n', '')[:-1], hl.colorchar(hl.get_the_dimmer_version_of(hl.what_color(color))))
      
    return True
  # end of draw_other_half_of_card()
  
  # draw_card_summon(): displaying all the parameters of 'summon' (ie 'creature') card
  def draw_card_summon(self, whatcard, subcursorr):
    card, subcursor = whatcard, subcursorr
    # text-list of abilities
    capt = self.get_card_abilities(card.get_abilities(), card.get_color())
    if card.get_effect_area() != gg.NONE:
      capt += [card.get_effect_casting_cost_string()]
      capt += ['  '+ card.get_effect()]
    
    # finding out what's supposed to be in flavor text area and print it
    pos, index, hl = 12, 0, self.hlp
    for txt in capt:
      space = 10 // len(capt) if len(capt) else 1
      if subcursor == index: self.draw_other_half_of_card('ability', txt.strip(), 'v'); color = gg.bgGRAY
      else: color = gg.WHITE
      self.write(pos, 5, [txt], color)
      pos += space; index += 1
    if subcursor == -1: self.draw_other_half_of_card('card', card.get_name(), card.get_color()[0])
    
    # those important numbers
    color = card.get_color()[0]
    hp, mov, att, deff, sht = str(card.get_life()), str(card.get_movement()), str(card.get_attack()), str(card.get_defense()), str(card.get_shooting())
    st = ' ' +att+ '/' +deff+ ' '
    st2 = '(' +sht+ ') ' if int(sht) else ''
    ln = len(st) + len(st2)
    self.write             (10, 4,          [st],  hl.what_color(color))
    if int(sht): self.write(10, 4 +len(st), [st2], hl.get_the_dimmer_version_of(hl.what_color(color)))

    self.parse('1219r text life: ' + ' '* (2- len(hp)) +hp)
    if int(sht): self.parse('1418b text ranged: ' +sht)
    self.parse('1518l text attack: ' +att)
    self.parse('1717g text defense: ' +deff)
    self.parse('1920y text move: ' +mov)
    return True    
  # end of draw_card_summon()  

  # draw_card_summon(): displaying all the parameters of 'equip' card
  def draw_card_equip(self, whatcard):
    def w(x): return 1 if x else 0
    card, pars, color = whatcard, self.parser, whatcard.get_color()[0]
    # text-list of abilities

    left =  pars.e(card.get_basic_effect(),  'equip abilities to array of strings')
    right = pars.e(card.get_kicker_effect(), 'equip abilities to array of strings')

    self.draw_other_half_of_card('nothing', card.get_name(), color)
    self.write(12,  6, left,  color)
    #if card.get_name() == 'Simplify': self.write(10, 34, right, color)
    if len(right) > 9: self.write(10, 34, right, color)
    else: self.write(12, 34, right, color)
    
    wd, gd, fd = card.manacost.wood, card.manacost.gold, card.manacost.food
    st = ''
    if wd: st += '   wood: ' +str(wd); color = gg.GREEN
    if gd: st += '   gold: ' +str(gd); color = gg.YELLOW
    if fd: st += '   food: ' +str(fd); color = gg.WHITE
    summ = w(wd) + w(gd) + w(fd)
    st = st.strip()
    if summ > 1: color = gg.LBLUE
    if summ == 3: st = ' all: ' +str(wd)
    
    self.write(9, 35, [st], color)
    
    return True    
  # end of draw_card_equip()
  
  # draw_hand(): draws the left/right hand. if the owner is looking, show the cards
  def draw_hand(self, what_player, side_of_board):
    signal, player, side, hl = self.signal, what_player, side_of_board, self.hlp
    
    a, b = player.get_overall_mana(), player.get_mana()
    red   = [a[0], b[0]]
    green = [a[1], b[1]]
    blue  = [a[2], b[2]]
    black = [a[3], b[3]]
    white = [a[4], b[4]]
    
    # drawings of player mana (total and current)
    pos = 2
    for i in range(white[1]): self.draw_manasymbol(2, pos, 'full', gg.WHITE); pos += 6
    for i in range(red[1]): self.draw_manasymbol(2, pos, 'full', gg.RED); pos += 6
    for i in range(green[1]): self.draw_manasymbol(2, pos, 'full', gg.GREEN); pos += 6
    for i in range(blue[1]): self.draw_manasymbol(2, pos, 'full', gg.BLUE); pos += 6
    for i in range(black[1]): self.draw_manasymbol(2, pos, 'full', gg.VIOLET); pos += 6
    pos += 2
    for i in range(white[0] - white[1]): self.draw_manasymbol(2, pos, 'big', gg.WHITE); pos += 6
    for i in range(red[0] - red[1]): self.draw_manasymbol(2, pos, 'big', gg.RED); pos += 6
    for i in range(green[0] - green[1]): self.draw_manasymbol(2, pos, 'big', gg.GREEN); pos += 6
    for i in range(blue[0] - blue[1]): self.draw_manasymbol(2, pos, 'big', gg.BLUE); pos += 6
    for i in range(black[0] - black[1]): self.draw_manasymbol(2, pos, 'big', gg.VIOLET); pos += 6
    
    self.parse('2302r text Life: ' +str(player.get_life()))
    gwot = self.signal.get_whos_on_turn()
    if (gwot == gg.HOME and side == 'left') or (gwot == gg.AWAY and side == 'right'):
      # continue only if player is looking at his own hand
      gd = player.get_goodies()
      cursor, hand_len = signal.get_cursor(), player.hand.length()
      self.parse('2318g text Wood: ' +str(gd[0]))
      self.parse('2332y text Gold: ' +str(gd[1]))
      self.parse('2346w text Food: ' +str(gd[2]))

      # text list of all cards in hand as third line on screen with current one being highlighted by inverted color
      cardname_len = 56 // hand_len if hand_len else 15
      for i in range(hand_len):
        card = signal.get_card_by_id(player.hand.get_card(i))
        color = hl.what_color(card.get_color()[0])
        if cursor == i: color = hl.invert_color(color)
        name = card.get_name()[:cardname_len -2]
        if name[-2] == ' ': name = name[:-1]
        if i: name = '|' +name
        self.write(4, 2+ i* cardname_len, [name], color)
      
      if hand_len: self.draw_card(signal.get_card_by_id(player.hand.get_card(cursor))) # draw the card if there is at least one
    else: self.parse('1010x text this is not your turn asswipe')
    return True
  # end of draw_hand()
  
  # draw_fight(): drawing the end-turn 'fight' phase --- NOT DONE  
  def draw_fight(self):
    hl = self.hlp
    self.parse('0805w text This is the fight screen')
    return True

  # draw draw_switch_turns_message(): black screen with the message in the middle for players have a time to switch in front of a monitor
  def draw_switch_turns_message(self):
    text = 'Player ' + self.signal.get_current_player_color_string() + ' turn'
    self.write(8, 35, [text], self.signal.get_current_player_color())
    return True
    
  # draw_field(): box of random letters from string (plains, bases, forest, ... and other usage)
  def draw_field(self, roww, column, liness, lettters, patttern, colourss):
      hl = self.hlp
      row, col, lines, letters, pattern, colours, onecolor = roww, column, liness, lettters, patttern, colourss, False
      if type(colours) == int: onecolor = colours
      else: colr = hl.random(0, 4, letters * lines)
      for depth in range(lines):
        rand = hl.random(0, len(pattern) -1, letters)
        for i in range(letters):
          x = row +depth; y = col +i
          if type(colours) == int: self.write(x, y, [pattern[rand[i]]], onecolor)
          else: self.write(x, y, [pattern[rand[i]]], colours[colr[depth* letters +i]])
      return True
  # end of draw_field()
  
  # draw_battlefield: draws the static part battlefield
  def draw_battlefield(self):
    if self.signal.get_battlefield_style() != 'default': return True
    hl = self.hlp
    plains = '..,\'"`  °°°°°º·····×»«ⁿⁿ'
    greek  = 'αßπσμτΦΘΩδ∞φε√∩≡'
    base   = ".'··.'··.'··.'··"
    plains += int(3.0* float(len(plains))) * ' '
    greek  += int(0.5* float(len(greek ))) * ' '
    base   += int(1.0* float(len(base  ))) * ' '
    home_base = [gg.RED, gg.VIOLET, gg.VIOLET, gg.GRAY, gg.GRAY]
    away_base = [gg.BLUE, gg.LBLUE, gg.BLUE, gg.GRAY, gg.GRAY]
    forest_color = [gg.GREEN, gg.GREEN, gg.GREEN, gg.GREEN, gg.VIOLET]
    plain_color = [gg.WHITE, gg.WHITE, gg.WHITE, gg.WHITE, gg.WHITE]
    self.draw_field( 5, 10, 7, 7, base, home_base)
    self.draw_field(13, 10, 7, 7, base, home_base)
    self.draw_field( 7,  2,11, 7, base, home_base)
    self.draw_field( 5, 42, 7, 7, base, away_base)
    self.draw_field(13, 42, 7, 7, base, away_base)
    self.draw_field( 7, 50,11, 7, base, away_base)
    self.draw_field(17, 18, 7, 23, plains, plain_color)  # plain
    self.draw_field( 4, 18, 4, 23, greek, forest_color)  # forest
    self.draw_mountains(1, 18)
    self.draw_swamp( 9, 18)
    self.parse('.bf_intersections')
    return True
  # end of draw_battlefield()

  # draw_swamp(): swamp &river part of the map
  def draw_swamp(self, row, col):
      hl = self.hlp
      cx, cy = row, col
      # swamp
      rand = hl.random(1, 3, 8)
      for i in range (8):
        x, y = cx, cy+ i*3
        if i == 7: y -= 1
        self.draw(x, y, 'swamp_pattern_', 'x', rand[i])
      # river  
      dep = 2; river = hl.random(0, 12, 8*5)
      for i in range (8*5):
        dep += -1 if river[i] <3 else 1 if river[i] < 6 else 0
        if dep < -2: dep += 1
        if dep > 8: dep -= 1
        x, y = cx + dep, cy+ i
        self.draw(x, y, 'river_tile', 'b')
        
      dep = 2; river = hl.random(0, 12, 17)
      for i in range (17):
        dep += -1 if river[i] <3 else 1 if river[i] < 6 else 0
        if dep < -2: dep += 1
        if dep > 8: dep -= 1
        x, y = cx + dep, cy- i
        self.draw(x, y, 'river_tile', 'b')
      return True
  # end of draw_swamp()
  
  # draw_mountains(): mountains part of the map
  def draw_mountains(self, row, col):
      hl = self.hlp
      cx, cy = row, col
      greek = 'αßπσμτΦΘΩδ∞φε       '
      # mountain 
      prev_up, up, level = False, False, 0; level0, level1 = 8*3*[False], 8*3*[False]
      for i in range(8*3):
        x = cx +3 -level; y = cy +i
        if level == 0: up = True
        elif level == 3: up = False
        else: up = hl.random(0, 1) == 1
        if up:
          if prev_up: x -= 1; level += 1
          self.write(x, y, ['/'], gg.VIOLET)
        else:
          if not prev_up: x += 1; level -= 1
          self.write(x, y, ['\\'], gg.VIOLET)
        
        if level > 1: level0[i] = True
        if level > 2: level1[i] = True
        prev_up = up
      #additional forest
      for i in range(8*3):
        x = cx +2; y = cy +i
        if level0[i]: self.write(x, y, [greek[hl.random(0, len(greek) -1)]], gg.GREEN)
        if level1[i]: self.write(x -1, y, [greek[hl.random(0, len(greek) -1)]], gg.VIOLET)
      return True
  # end of draw_mountains()
  
  # draw_bf_cursor(): draws the cursor onto battlefield
  def draw_bf_cursor(self, where, shade):
    hl = self.hlp
    cursor, color, switch = where, shade, False
    if cursor < 9: x, y = 8* (cursor //3), 17+ 8* (cursor %3)
    if cursor in ( 9, 12): x = 6; switch = True
    if cursor in (10, 13): x = 4
    if cursor in (11, 14): x = 12
    if cursor == 9: y = 1
    if cursor in (10, 11): y = 9
    if cursor in (13, 14): y = 41
    if cursor == 12: y = 49
    
    if switch: # one of the edge-fields which are bigger and therefore have different cursor drawing
      self.write(x, y,    [9* '▓'], color)
      self.write(x +12, y, [9* '▓'], color)
      self.write(x, y,    13* ['▓'], color)
      self.write(x, y +8, 13* ['▓'], color)
    else:
      self.write(x, y,    [9* '▓'], color)
      self.write(x +8, y, [9* '▓'], color)
      self.write(x, y,    9* ['▓'], color)
      self.write(x, y +8, 9* ['▓'], color)
    return True
  # end of draw_bf_cursor()
  
  # various: help methods of draw_territory_borders()
  def gcol(self, key, maincolor = 1):
      a = self.signal.get_players_colors()
      if key == gg.HOME: x = a[0] if maincolor else a[1]
      if key == gg.AWAY: x = a[2] if maincolor else a[3]
      if key == gg.NONE: x = gg.GRAY
      return x

  def sort_colors(self, couple):
    c, d, arr = couple[0], couple[1], self.signal.get_colors_priority()
    return [c, d] if arr.index(c) < arr.index(d) else [d, c]
  
  # mixed_line(): the line which have different color at the edges than in the middle as a main element of displaying the borders of the two player's territory
  def mixed_line(self, typee, where_x, where_y, length, colours):
    x, y, ln, cl = where_x, where_y, length, colours; error = False
    for i in range(ln):
      c = 1 if i >= 2 and i <= 4 else 0
      if   typee == 'h': self.write(x, y+i, ['─'], cl[c])
      elif typee == 'v': self.write(x+i, y, ['│'], cl[c])
      else: error = True
    if error: print("\n\nstate.mixed_line(): wrong key (must be 'h' or 'v')\n"); return False
    return True

  # draw_territory_borders(): colored borders of fields based on the ownerships of these
  def draw_territory_borders(self, fields_ownership):
    hl, arr = self.hlp, [[None] * 3 for _ in range(5)]
    for i in range(15): arr[i//3][i%3] = fields_ownership[i]

    for rowborder in range(2):
      for field in range(3):
        x = 8+ rowborder * 8; y = 18+ field *8
        colors = self.sort_colors([self.gcol(arr[rowborder][field]), self.gcol(arr[rowborder+1][field])])
        self.mixed_line('h', x, y, 7, colors)

    for columnborder in range(2):
      for field in range(3):
        x = 1+ field * 8; y = 25 + columnborder *8
        colors = self.sort_colors([self.gcol(arr[field][columnborder]), self.gcol(arr[field][columnborder +1])])
        self.mixed_line('v', x, y, 7, colors)
        
    for i in range(3):
      self.draw(i*8 +1, 17, 'v-line 07', hl.colorchar(self.gcol(arr[i][0])))
      self.draw(i*8 +4, 17, 'corner-Tl', hl.colorchar(self.gcol(arr[i][0])))
      self.draw(i*8 +1, 41, 'v-line 07', hl.colorchar(self.gcol(arr[i][2])))
      self.draw(i*8 +4, 41, 'corner-Tr', hl.colorchar(self.gcol(arr[i][2])))
      

    self.parse('COLOR ' + hl.colorchar(self.gcol(arr[3][0], 0))); self.parse('.field30')
    self.parse('COLOR ' + hl.colorchar(self.gcol(arr[3][1], 0))); self.parse('.field31')
    self.parse('COLOR ' + hl.colorchar(self.gcol(arr[3][2], 0))); self.parse('.field32')
    self.parse('COLOR ' + hl.colorchar(self.gcol(arr[4][0], 0))); self.parse('.field40')
    self.parse('COLOR ' + hl.colorchar(self.gcol(arr[4][1], 0))); self.parse('.field41')
    self.parse('COLOR ' + hl.colorchar(self.gcol(arr[4][2], 0))); self.parse('.field42')
    colors = self.sort_colors([self.gcol(arr[3][1], 0), self.gcol(arr[3][2], 0)])
    self.mixed_line('h', 12, 10, 7, colors)
    colors = self.sort_colors([self.gcol(arr[4][1], 0), self.gcol(arr[4][2], 0)])
    self.mixed_line('h', 12, 42, 7, colors)
    return True
  # end of draw_territory_borders()

  # draw_battlefield_minimap(): the minimap version of battlefield in it's alternative view
  def draw_battlefield_minimap(self, posx, posy, cursor, minicursorcolor):
    px, py, cur, tx, cx, cy, col = posx, posy, cursor, self.textures, 0, 0, minicursorcolor
    self.write(px, py, tx.get('battlefield_minimap'), gg.GREEN)
    if cur < 9:
      cx, cy = 2* (cur//3), 6+ 3* (cur%3)
    if cur in (10, 13): cx += 1
    if cur in ( 9, 12): cx += 2
    if cur in (11, 14): cx += 3
    if cur in (10, 11): cy += 3
    if cur in (13, 14): cy += 15
    if cur == 12: cy += 18
    self.write(px +cx, py +cy, tx.get('cursor_minimap'), col)
    return True
  # end of draw_battlefield_minimap()
  
  # draw_current_field_units(): drawing the soldiers in given field in alternative style of battlefield viewing
  def draw_current_field_units(self, position, list_of_gangs_of_given_field, terrain):
    cursor, list_all, list_home, list_away, terr = position, [], [], [], terrain
    for one in list_of_gangs_of_given_field: list_all.append(one)

    # background...
    plains = '..,\'"`°°°°°º·····×»«ⁿⁿ' + 100* ' '
    forest  = 'αßπσμτΦΘΩδ∞φε√∩' + 40* ' '
    swamp = '░░░▒≈≈≈≈' + 20* ' '
    base   = ".'··.'··.'··.'··" + 20* ' '
    home_base = [gg.RED, gg.VIOLET, gg.VIOLET, gg.GRAY, gg.GRAY]
    away_base = [gg.LBLUE, gg.BLUE, gg.BLUE, gg.GRAY, gg.GRAY]
    forest_color = [gg.GREEN, gg.VIOLET, gg.GREEN, gg.GREEN, gg.RED]
    plain_color = [gg.WHITE, gg.WHITE, gg.WHITE, gg.WHITE, gg.WHITE]
    swamp_color = [gg.GRAY, gg.BLUE, gg.GRAY, gg.GRAY, gg.BLUE]
    if terr == gg.FOREST: pattern, color = forest, forest_color
    if terr == gg.RIVER:  pattern, color = swamp , swamp_color
    if terr == gg.PLAIN:  pattern, color = plains, plain_color
    if terr == gg.BASE_H: pattern, color = base  , home_base
    if terr == gg.BASE_A: pattern, color = base  , away_base
    self.draw_field(1, 1, 23, 58, pattern, color)
    
    # the main area
    self.draw_field(6, 1, 18, 41, ' ', color[0])
    for x in range(7, 24):
      for y in range(1, 41):
        if (x+y)%2 == 1: self.write(x, y, ['·'], color[0])
    self.draw_battlefield_minimap(1, 36, cursor, gg.YELLOW)
    self.write(7, 36, ['· ·'], color[0]) # detail in upper-left corner
    self.write(23, 40, [' '], color[0])  # detail in lower-left corner

    # soldiers
    for one in list_all:
      if one.get_owner() == gg.HOME: list_home.append(one)
      if one.get_owner() == gg.AWAY: list_away.append(one)
    if len(list_home) > 4 or len(list_away) > 4: self.draw_field_units_special(cursor, list_home, list_away)
    else: self.draw_field_units(cursor, list_home, list_away)      
    return True
  # end of draw_current_field_units()

  # draw_field_units_special(): slightly alternative version for two starting fields of a game where six, not four soldiers of each side is allowed  
  def draw_field_units_special(self, actual_cursor, homelist, awaylist):
    cursor, list_home, list_away = actual_cursor, homelist, awaylist
    home_positions, away_positions = (0, 1, 2, 6, 7, 8), (3, 4, 5, 9, 10, 11)
    for i in range(len(list_home)):
      index = home_positions[i]
      px, py = 7+ 9* (index//6), 1+ 10* (index%6)
      self.draw_gang('normal', list_home[i], px, py)
    for i in range(len(list_away)):
      index = away_positions[i]
      px, py = 7+ 9* (index//6), 1+ 10* (index%6)
      if i in (2, 5): py -= 1
      self.draw_gang('normal', list_away[i], px, py)
    return True
  # end of draw_field_units_special()

  # draw_field_units(): draws the units in given field in minimap version of the battlefield
  def draw_field_units(self, actual_cursor, homelist, awaylist):
    cursor, list_home, list_away = actual_cursor, homelist, awaylist
    home_positions, away_positions = (0, 1, 4, 5), (2, 3, 6, 7)
    for i in range(len(list_home)):
      index = home_positions[i]
      px, py = 7+ 9* (index//4), 1+ 10* (index%4)
      self.draw_gang('normal', list_home[i], px, py)
    for i in range(len(list_away)):
      index = away_positions[i]
      px, py = 7+ 9* (index//4), 3+ 10* (index%4)
      self.draw_gang('normal', list_away[i], px, py)      
    return True
  # end of draw_field_units()
  
  # draw_boxes(): draw several icons in line or column; used by draw_gang()
  def draw_boxes(self, designated_style, open_start, open_end, how_many, position_x, position_y, texturename, colorr):
    style, open_s, open_e, n, x, y, txt, color = designated_style, open_start, open_end, how_many, position_x, position_y, texturename, colorr
    txt_start, txt_hor, txt_ver, txt_hor_end, txt_ver_end = self.get_texture(txt), self.get_texture(txt + '_hor'), self.get_texture(txt + '_ver'), self.get_texture(txt + '_hor_end'), self.get_texture(txt + '_ver_end')
    vertical_size, horizontal_size = len(txt_start) -1, len(txt_start[0]) -1
    if not n: return True
    if n == 1: self.write(x, y, txt_start, color); return True
    for i in range(n):
      if style == 'horizontal':
        if i == n-1:
          if open_e: self.write(x, y+ i* horizontal_size, txt_hor, color)
          else:      self.write(x, y+ i* horizontal_size, txt_hor_end, color)
        elif i == 0:
          if open_s: self.write(x, y+ i* horizontal_size, txt_hor,     color) # open start switch
          else:      self.write(x, y+ i* horizontal_size, txt_start,   color)
        else:                      self.write(x, y+ i* horizontal_size, txt_hor,     color)
      if style == 'vertical':
        if i == n-1:
          if open_e: self.write(x+ i* vertical_size, y, txt_ver, color)
          else:      self.write(x+ i* vertical_size, y, txt_ver_end, color)
        elif i == 0:
          if open_s: self.write(x+ i* vertical_size, y, txt_ver,     color) 
          else:      self.write(x+ i* vertical_size, y, txt_start,   color)
        else:                      self.write(x+ i* vertical_size, y, txt_ver,     color)
    return True
  # end of draw_boxes()  
  
  # draw_gang(): several ways (depending on 'style') of how to draw a gang
  def draw_gang(self, style, whatgang, posx, posy, gang_color = ''):
    px, py, tx, gang, stl, signal, gangcolor = posx, posy, self.textures, whatgang, style, self.signal, gang_color
    gcl = signal.get_players_colors()
    att, deff, sht, mov_curr, mov_full, name, subtype, hp, life = gang.get_attack(), gang.get_defense(), gang.get_shooting(), gang.get_current_movement(), gang.get_movement(), gang.get_name(), gang.get_subtype(), (gang.get_hp() +9) //10, (gang.get_life() +9) //10
    box_keyword = 'boxfat' if mov_curr else 'box' # narrow box for already moved unit
    if gang.get_owner() == gg.HOME:
      color = gcl[0] if gang.get_hp_life_ratio() >= 0.75 else gcl[1] # other color for wounded unit
    if gang.get_owner() == gg.AWAY:
      color = gcl[2] if gang.get_hp_life_ratio() >= 0.75 else gcl[3]
    
    if stl == 'normal':
      self.write(px, py, tx.get(box_keyword, 8, 8), color)
      self.write(px +3, py +1, [' a:', ' d:', ' m:', 'hp:'], color)
      self.write(px +3, py +5, [str(att)], color)
      self.write(px +4, py +5, [str(deff)], color)
      self.write(px +5, py +5, [str(mov_curr)], color)
      self.write(px +6, py +5, [str(hp)], color)
      if sht:
        self.write(px +2, py +2, ['s:'], color)
        self.write(px +2, py +5, [str(sht)], color)
      self.write(px +1, py +1, [subtype[:6]], gg.GRAY)
      self.write(px, py +1, [' ' +name[:4]+ ' '], gg.WHITE)
      
    if stl == 'tiny':
      self.write(px, py, tx.get(box_keyword, 3, 3), color)
      p, r = self.get_the_power_of_gang(gang) // 100, gang.get_hp_life_ratio()
      st = str(p) if p < 10 else chr(p+ ord('A') -10)
      self.write(px +1, py +1, [st], gg.WHITE) # relative strength of gang in the middle of icon
      if r < 0.25: self.write(px +2, py +2, ['¼'], color)
      if r < 0.50: self.write(px +2, py +2, ['½'], color)
      
    if stl == 'huge':
      self.write(px, py, tx.get(box_keyword, 19, 35), color)
      if sht:
        self.write(px +2, py +2, ['s:'], color)
        self.write(px +2, py +5, [str(sht)], color)
      self.write(px, py +31 - len(subtype), [' ' + subtype + ' '], color)
      self.write(px, py  +2, [' ' +name+ ' '], color)
      
      self.draw_boxes('horizontal', False, False, att,  6, 30, 'li_box', gg.bgBLUE)
      self.draw_boxes('horizontal', False, False, deff, 8, 30, 'li_box', gg.bgGREEN)
      if sht:
        self.draw_boxes('horizontal', False, False, sht, 4, 30, 'li_box', gg.bgLBLUE)
        self.parse('0525x text sht:')
      self.parse('0925x text def:')
      self.parse('0725x text att:')
      self.parse('2024x text move')
      self.parse('2053x text life')
      clrr = gg.bgYELLOW if mov_curr else gg.YELLOW
      switch = False
      if mov_full > 7: mov_full = 7; switch = True
      self.draw_boxes('vertical', False, False, mov_full, 18 - mov_full, 25, 'li_box', clrr)
      if switch: self.write(10, 25, ['+++'], gg.RED)
      
      self.draw_life(life, 18, 53, gg.RED)
      self.draw_life(hp, 18, 53, gg.bgRED)
      llist = self.get_card_abilities(gang.get_abilities(), gang.get_color_char())
      shift = 0
      if len(llist) <= 2: shift = 2
      if len(llist) <= 4: llist = self.hlp.insert_empty_lines(llist, 1)
      self.write(11 +shift, 31, llist, gg.WHITE)
    return True
  # end of draw_gang()
  
  # draw_life(): special sub method for drawing the life of a gang as it can take more than one column
  def draw_life(self, amount, position_x, position_y, colorrr):
    n, x, y, color  = amount, position_x, position_y, colorrr
    for backcolumn in range(n//8):
      self.draw_boxes('vertical', False, False,   8, x -8,   y -3* backcolumn, 'li_box', color)
    self.draw_boxes  ('vertical', False, False, n%8, x -n%8, y -3* (n//8),     'li_box', color)
    return True

  # draw_minisoldiers(): draw the icons of gangs on the main view battlefield
  def draw_minisoldiers(self, allgangs):
    alg = []
    for one in allgangs: alg.append(one)
    for field in range(15):
      home, away = [], []
      for one in alg:
        if field == one.get_position():
          if one.get_owner() == gg.HOME: home.append(one)
          if one.get_owner() == gg.AWAY: away.append(one)
      if field < 9: x, y = 8* (field //3), 17+ 8* (field %3)
      if field in ( 9, 12): x = 8; switch = True
      if field in (10, 13): x = 4
      if field in (11, 14): x = 12
      if field == 9: y = 1
      if field in (10, 11): y = 9
      if field in (13, 14): y = 41
      if field == 12: y = 49
      self.draw_minisoldiers_one_field(x +1, y +1, home, away)
    return True
  # end of draw_minisoldiers()
  
  # draw_minisoldiers_one_field(): draw method for single field
  def draw_minisoldiers_one_field(self, position_x, position_y, homelist, awaylist):
    lenh, lena, x, y, home, away, tx = len(homelist), len(awaylist), position_x, position_y, homelist, awaylist, self.textures
    hcouple, acouple = self.get_two_biggest(home), self.get_two_biggest(away)
    hc1, hc2, ac1, ac2 = hcouple[0], hcouple[1], acouple[0], acouple[1]
    if hc1: self.draw_gang('tiny', hc1, x   , y   )
    if hc2: self.draw_gang('tiny', hc2, x +4, y   )
    if ac1: self.draw_gang('tiny', ac1, x   , y +4)
    if ac2: self.draw_gang('tiny', ac2, x +4, y +4)
    if lenh == 3: self.write(x +3, y, ['▌ ▐'], gg.RED)
    if lenh > 3:  self.write(x +3, y, ['███'], gg.RED)
    if lena == 3: self.write(x +3, y +4, ['▌ ▐'], gg.LBLUE)
    if lena > 3:  self.write(x +3, y +4, ['███'], gg.LBLUE)
    return True
  # end of draw_minisoldiers_one_field()
  
  # get_two_biggest(): chooses the two strongest gangs to display
  def get_two_biggest(self, llist):
    l, ll = [o for o in llist], len(llist)
    if not ll: return [False, False]
    elif ll == 1: return [l[0], False]
    else: a = self.get_one_biggest(l); l.remove(a)
    return [a, self.get_one_biggest(l)]
  # end of get_two_biggest()    

  # get_one_biggest(): returns the strongest gang from list
  def get_one_biggest(self, llist):
    a, l, maxx, index = 0, llist, 0, 0
    for one in l:
      x = self.get_the_power_of_gang(one)
      if x > maxx: maxx = x; a = index
      index += 1
    return l[a]
  # end of get_one_biggest()
    
  #def get_the_power_of_gang(self, one): return 99* one.get_attack() + 99* one.get_defense() + 99* one.get_shooting() + one.get_life() + one.get_hp() //10
  def get_the_power_of_gang(self, one): return one.get_relative_value()

  # draw_chosen_path(): drawing the very special version of cursor in case the game is in "move the units" phase
  def draw_chosen_path(self, desired_path, all_pubs, style):
    path, pubs, styl = [o for o in desired_path], [o for o in all_pubs], style
    self.parse('COLOR ' +self.hlp.colorchar(self.signal.get_current_player_color()))

    for i in range(len(path) -1):
      a, b = path[i], path[i+1]
      if a>b: aa = a; a = b; b = aa
      filee = '.m' if styl == 'minimap' else '.n'
      filee += str(a) + str(b)
      self.parse(filee)
    
    if styl != 'minimap':
      for i in range(len(pubs)):
        sttr = 'pub_final' if i == len(pubs) -1 else 'pub'
        p = pubs[i]
        if p < 9: x = 8* (p//3) +3; y = 19+ 8* (p%3)
        if p in (10, 11): y = 11
        if p ==  9: y = 3
        if p in (13, 14): y = 43
        if p == 12: y = 51
        if p in (9, 12): x = 11
        if p in (10, 13): x = 7
        if p in (11, 14): x = 15
        self.write(x, y, self.get_texture(sttr), gg.NONECOLOR)
      
    if styl == 'minimap':
      for i in range(len(pubs)):
        p = pubs[i]
        if p < 9: x = 2* (p//3 +1); y = 43+ 3* (p%3)
        if p in (10, 11): y = 40
        if p ==  9: y = 37
        if p in (13, 14): y = 52
        if p == 12: y = 55
        if p in (9, 12): x = 4
        if p in (10, 13): x = 3
        if p in (11, 14): x = 5
        self.write(x, y, ['██'], gg.NONECOLOR)
      
      
    return True
  # end of draw_chosen_path()

  # get_card_abilities(): returns array of strings, each string equal to one ability
  def get_card_abilities(self, abilities, color):
    print(color); gg.getch
    ca, capt, cc = abilities, [], color[0]
    for i in range(len(ca)):
        if not ca[i]: continue
        if i == gg.WORKER:      capt.append('worker')       if ca[i] == 1   else capt.append('engineer')
        if i == gg.NATIVE:
          if cc in ('r', 'g'):  capt.append('hillbilly') if ca[i] == 1 else capt.append('redneck')
          if cc == 'b':         capt.append('swimmer')      if ca[i] == 1 else capt.append('fish')
          if cc == 'x':         capt.append('stalker')      if ca[i] == 1 else capt.append('gollum')
          if cc == 'w':         capt.append('rider')        if ca[i] == 1 else capt.append('postman')
        if i == gg.FIRSTSTRIKE: capt.append('firststrike')  if ca[i] == 1 else capt.append('monk')
        if i == gg.SLOWSTRIKE:  capt.append('slowstrike')   if ca[i] == 1 else capt.append('retarded')
        if i == gg.FLYING:      capt.append('flying')       if ca[i] == 1 else capt.append('ace')
        if i == gg.HASTE:       capt.append('haste')        if ca[i] == 1 else capt.append('frantic')
        if i == gg.VIGILANCE:   capt.append('defender')     if ca[i] == 1 else capt.append('vigilance')
        if i == gg.TRAMPLE:     capt.append('trample')      if ca[i] == 1 else capt.append('crusher')
        if i == gg.WALLCRUSHER: capt.append('wallcrusher')  if ca[i] == 1 else capt.append('aladdin')
        if i == gg.PROVOKE:     capt.append('provoke')      if ca[i] == 1 else capt.append('peacekeeper')
        if i == gg.FLANKING:    capt.append('flanking')     if ca[i] == 1 else capt.append('chariot')
        if i == gg.IMMUNE:      capt.append('immune')       if ca[i] == 1 else capt.append('hexproof')
        if i == gg.FEAR:        capt.append('fear')         if ca[i] == 1 else capt.append('panic')
        if i == gg.POISONOUS:   capt.append('carrier')      if ca[i] == 1 else capt.append('poisonous')
        if i == gg.SNIPER:      capt.append('marksman')     if ca[i] == 1 else capt.append('sniper')
        if i == gg.HEALER:      capt.append('healer')       if ca[i] == 1 else capt.append('shaman')
        if i == gg.DECOY:       capt.append('decoy')        if ca[i] == 1 else capt.append('hannibal')
        if i == gg.THROWN:      capt.append('thrower')      if ca[i] == 1 else capt.append('aimer')
        if i == gg.CASTER:      capt.append('caster')       if ca[i] == 1 else capt.append('wizard')
        if i == gg.SCOUT:       capt.append('scout')        if ca[i] == 1 else capt.append('ranger')
        if i == gg.FLEE:        capt.append('coward')       if ca[i] == 1 else capt.append('rat')
        if i == gg.RAMPART:     capt.append('visionary')    if ca[i] == 1 else capt.append('prophet')
        if i == gg.SPY:         capt.append('spy')          if ca[i] == 1 else capt.append('greema')
        if i == gg.MENTAT:      capt.append('mentat')       if ca[i] == 1 else capt.append('piter')
        if i == gg.BUILDER:     capt.append('smith')        if ca[i] == 1 else capt.append('builder')
        if i == gg.ILL:         capt.append('ill')          if ca[i] == 1 else capt.append('poisoned')
        if i == gg.LEADER:      capt.append('leader')       if ca[i] == 1 else capt.append('sergeant')
        if i == gg.COMMANDER:   capt.append('commander')    if ca[i] == 1 else capt.append('general')
    return capt
  # end of get_card_abilities()
  
  # invitation(): the current welcome screen (the second after start; the first is easy enough to be processed by file)
  def invitation(self):
    l1 = '`1234567890-='
    l2 = 'QWERTYUIOP[]'
    l3 = 'ASDFGHJKL;\'\\'
    l4 = 'ZXCVBNM<>?'
    for i in range(13):
      color = gg.GRAY
      if i in(1, 7): color = gg.GREEN
      if i in(2, 8): color = gg.YELLOW
      if i in(3, 9): color = gg.LBLUE
      self.write(2, 1+ i*5, self.get_texture('box', 3, 4), color)
      self.write(3, 2+ i*5, [l1[i]], color)
    for i in range(12):
      color = gg.GRAY
      if i in(0, 6): color = gg.GREEN
      if i in(2, 8): color = gg.YELLOW
      if i in(1, 7): color = gg.RED
      self.write(5, 7+ i*5, self.get_texture('box', 3, 4), color)
      self.write(6, 8+ i*5, [l2[i]], color)
    for i in range(12):
      color = gg.GRAY
      if i in (0, 1, 2, 6, 7, 8): color = gg.RED
      if i in(3, 9): color = gg.LBLUE
      self.write(8, 8+ i*5, self.get_texture('box', 3, 4), color)
      self.write(9, 9+ i*5, [l3[i]], color)
    for i in range(10):
      color = gg.GRAY
      self.write(11, 9+ i*5, self.get_texture('box', 3, 4), color)
      self.write(12,10+ i*5, [l4[i]], color)
    self.parse('.invitation')
    return True
  
  # clean(): destructor
  def clean(self):
    self.textures.clean(); del self.textures
    self.comm.clean(); del self.comm
    self.animation.clean(); del self.animation
    self.hlp.clean(); del self.hlp
    return True
# end of class Screen
    
  
"""    
    
∩ ≡ ÷ ≈ ° · · √ ⌠⌡ ⌐¬     
 ┴┬ ├┤ ┼  ─│ └┘┌┐  ═║    
 ½ ¼ × » «  ░ ▒ ▓  
¢ £ ¥ ª º ⁿ ²
α ß Γ π Σ σ μ τ Φ Θ Ω δ ∞ φ ε
█ ▄▀ ▌▐ ■

"""
