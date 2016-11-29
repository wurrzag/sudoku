from constants import the_file as gg

# (text.py/)Manager: list of all the bigger ascii textures; the only method of this class can return one of them
class Textures:
  
  def __init__(self):
    self.all_textures = {
    'heart': [
    '         ',
    '  XX XX  ',
    ' |  V  | ',
    ' |     | ',
    '  \   /  ',
    '   \ /   ',
    '    Y    ',
    ],

    'button_1': [
    '  Q   U  ',
    '┌───────┐',
    '│  ─┬─  │',
    '│   │   │',
    '│   │   │',
    '│  ─┴─  │',
    '└───────┘'],
    'button_2': [
    '  E   O  ',
    '┌───────┐',
    '│ ─┬─┬─ │',
    '│  │ │  │',
    '│  │ │  │',
    '│ ─┴─┴─ │',
    '└───────┘'],
    'button_3': [
    '  F   ;  ',
    '┌───────┐',
    '│ ─┬┬┬─ │',
    '│  │││  │',
    '│  │││  │',
    '│ ─┴┴┴─ │',
    '└───────┘'
    ],

    'button_empty': [
    '         ',
    '┌───────┐',
    '│       │',
    '│       │',
    '│       │',
    '│       │',
    '└───────┘'
    ],

    'river_tile':[
    '≈',
    '≈'
    ],
    
    'swamp_pattern_1':[
    '░░▒',
    '▒▒▓',
    '░▒▒',
    '░▒░',
    '▒▒▒',
    '▓▒░',
    '▒▒░'
    ],
    'swamp_pattern_2':[
    '░▒░',
    '░▒░',
    '▒▒░',
    '░▓░',
    '░▒▒',
    '░▒░',
    '░░░'
    ],
    'swamp_pattern_3':[
    '▒▒░',
    '▓▒▒',
    '▒▒░',
    '░░░',
    '░▒░',
    '▒▒▒',
    '░▒▓'
    ],

    
    'mountain_big':[
    '    ',
    ' /\ ',
    '/  \\',
    '    '
    ],
    
    'mountain_small':[
    '/\\/\\'  
    ],

    'battlefield_minimap_small':[
    '    ┌─┬─┬─┐    ',
    '  ┌─┤ │ │ ├─┐  ',
    '┌─┤ ├─┼─┼─┤ ├─┐',
    '│ ├─┤ │ │ ├─┤ │',
    '└─┤ ├─┼─┼─┤ ├─┘',
    '  └─┤ │ │ ├─┘  ',
    '    └─┴─┴─┘    '
    ],
    
    'battlefield_minimap':[
    '      ┌──┬──┬──┐      ',
    '   ┌──┤  │  │  ├──┐   ',
    '┌──┤  ├──┼──┼──┤  ├──┐',
    '│  ├──┤  │  │  ├──┤  │',
    '└──┤  ├──┼──┼──┤  ├──┘',
    '   └──┤  │  │  ├──┘   ',
    '      └──┴──┴──┘      '
    ],
    
    'cursor_minimap_small':[
    '███',
    '█ █',
    '███',
    ],
    
    'cursor_minimap2':[
    '████',
    '█  █',
    '████',
    ],
    
    'cursor_minimap':[
    '▓▓▓▓',
    '▓▒▒▓',
    '▓▓▓▓',
    ],


    'life_box':[
    '┌──┐',
    '│∞∞│',
    '└──┘'
    ],
 
    'life_box_hor':[
    '┬──┬',
    '│∞∞│',
    '┴──┴'
    ],
 
    'life_box_ver':[
    '├──┤',
    '│∞∞│',
    '├──┤'
    ], 

    'life_box_hor_start':[
    '┌──┬',
    '│∞∞│',
    '└──┴'
    ],
 
    'life_box_ver_start':[
    '┌──┐',
    '│∞∞│',
    '├──┤'
    ], 

    'life_box_hor_end':[
    '┬──┐',
    '│∞∞│',
    '┴──┘'
    ],
 
    'life_box_ver_end':[
    '├──┤',
    '│∞∞│',
    '└──┘'
    ], 

    'lif_box':[
    '┌──┐',
    '└──┘'
    ],
 
    'lif_box_hor':[
    '┬──┬',
    '┴──┴'
    ],
 
    'lif_box_ver':[
    '├──┤',
    '├──┤'
    ], 

    'lif_box_hor_start':[
    '┌──┬',
    '└──┴'
    ],
 
    'lif_box_ver_start':[
    '┌──┐',
    '├──┤'
    ], 

    'lif_box_hor_end':[
    '┬──┐',
    '┴──┘'
    ],
 
    'lif_box_ver_end':[
    '├──┤',
    '└──┘'
    ], 

    'li_box':[
    '┌─┐',
    '└─┘'
    ],
 
    'li_box_hor':[
    '┬─┬',
    '┴─┴'
    ],
 
    'li_box_ver':[
    '├─┤',
    '├─┤'
    ], 

    'li_box_hor_start':[
    '┌─┬',
    '└─┴'
    ],
 
    'li_box_ver_start':[
    '┌─┐',
    '├─┤'
    ], 

    'li_box_hor_end':[
    '┬─┐',
    '┴─┘'
    ],
 
    'li_box_ver_end':[
    '├─┤',
    '└─┘'
    ], 

    'pub':[
    '█████',
    '█   █',
    '█████',
    ],
    
    'pub_final':[
    '▓▓▓▓▓',
    '▓▒▒▒▓',
    '▓▓▓▓▓',
    ],

    'empty_one':[
    '    ',
    '    ',
    '    ',
    '    '
    ],
 

    """    

    ∩ ≡ ÷ ≈ ° · · √ ⌠⌡ ⌐¬ 
    ┴┬ ├┤ ┼  ─│ └┘┌┐  ═║
    ½ ¼ × » «  ░ ▒ ▓  
    ¢ £ ¥ ª º ⁿ ²
    α ß Γ π Σ σ μ τ Φ Θ Ω δ ∞ φ ε
    █ ▄▀ ▌▐ ■

    """
   
    
    'last_one':[
    'end'  
    ]
    
    }
    return None
  # end of __init__()
  
  
  # get() - return the texture by keyword (it's name)
  def get(self, keyword, size = 0, leng = 0):
    pattern = []
    if not len(keyword): return ['']

    elif keyword == 'box':
      for line in range(size):
        if line == 0: pattern.append('┌' + (leng-2)* '─' + '┐')
        elif line == size -1: pattern.append('└' + (leng-2)* '─' + '┘')
        else: pattern.append('│' + (leng-2)* ' ' + '│')
      return pattern

    elif keyword == 'boxempty':
      for line in range(size):
        if line == 0: pattern.append(' ' + (leng-2)* ' ' + ' ')
        elif line == size -1: pattern.append(' ' + (leng-2)* ' ' + ' ')
        else: pattern.append(' ' + (leng-2)* ' ' + ' ')
      return pattern

    elif keyword == 'boxfat':
      for line in range(size):
        if line == 0: pattern.append('█' + (leng-2)* '▀' + '█')
        elif line == size -1: pattern.append('█' + (leng-2)* '▄' + '█')
        else: pattern.append('▌' + (leng-2)* ' ' + '▐')
      return pattern

    elif keyword == 'boxfat2':
      for line in range(size):
        if line == 0: pattern.append('█' + (leng-2)* '▀' + '█')
        elif line == size -1: pattern.append('█' + (leng-2)* '▄' + '█')
        else: pattern.append('█' + (leng-2)* ' ' + '█')
      return pattern
    
    elif keyword == 'h-line': return [size* '─']
    elif keyword == 'v-line': return size* ['│'] 
    elif keyword == 'h-2line': return [size* '═']
    elif keyword == 'v-2line': return size* ['║']
    elif keyword == 'h-3line': return [size* '█']
    elif keyword == 'v-3line': return size* ['█']
    
  
    
    else:
      try: return self.all_textures[keyword] 
      except KeyError: return['wrong', ' tex ', 'ture']
    return['very','nasty', 'error']
  # end of get()
  
  # clean() - destructor
  def clean(self):
    del self.all_textures
    return True
  
  
  #end of class Manager
  