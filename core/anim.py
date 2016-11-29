from constants import the_file as gg
from random import randint

# Animation: experimental but properly working class with skill of animate the ascii frames
class Animation:
  def __init__(self, terminal_instance, animation_speed):
    self.comm = terminal_instance
    self.pause = animation_speed
    self.all_textures = textures # after this class
    return None
  # end of __init__()
  
  # m(): main method
  def m(self, command, params = ''):
    comm, pause, t = self.comm, self.pause, self.all_textures
    if command == 'test':
      comm.write(10, 10, ['hello      '], gg.WHITE); comm.run('animation', pause)
      comm.write(10, 10, ['   hello   '], gg.WHITE); comm.run('animation', pause)
      comm.write(10, 10, ['      hello'], gg.WHITE); comm.run('animation', pause)

    # 'the wizard' as the main effect when the card is played      
    if command == 'cast card':
      n, color1, color2 = params[0], params[1], params[2]
      for i in range(n):
        comm.reset(); comm.write(10, 15, t['boom1'], color1); comm.run('animation', pause)
        comm.reset(); comm.write(10, 15, t['boom2'], color2); comm.run('animation', pause)
        comm.reset(); comm.write(10, 15, t['boom3'], color1); comm.run('animation', pause)
        comm.reset(); comm.write(10, 15, t['boom4'], color2); comm.run('animation', pause)
        comm.reset(); comm.write(10, 15, t['boom5'], color1); comm.run('animation', pause)
        comm.reset(); comm.write(10, 15, t['boom6'], color2); comm.run('animation', pause)
    
    # white noise as a first sub-effect when the card is played
    if command == 'white noise':
      n, ax, ay, zx, zy, colors, st = params[0], params[1], params[2], params[3], params[4], params[5], '░▒▓'

      for i in range(n):
          comm.reset()
          comm.write(ax -2, ay -2, self.boxfat(16, 30), colors[0])
          comm.write(ax -1, ay -1, self.box(14, 28), colors[1])
          comm.run()
          for x in range(ax, zx):
            for y in range(ay, zy):
              comm.write(x, y, [st[randint(0, 2)]], colors[0])
          comm.run('animation', pause)
    
    return True
  # end of m():

  def box(self, size, leng):
      pattern = []
      for line in range(size):
        if line == 0: pattern.append('┌' + (leng-2)* '─' + '┐')
        elif line == size -1: pattern.append('└' + (leng-2)* '─' + '┘')
        else: pattern.append('│' + (leng-2)* ' ' + '│')
      return pattern
  def boxfat(self, size, leng):
      pattern = []
      for line in range(size):
        if line == 0: pattern.append('█' + (leng-2)* '▀' + '█')
        elif line == size -1: pattern.append('█' + (leng-2)* '▄' + '█')
        else: pattern.append('▌' + (leng-2)* ' ' + '▐')
      return pattern

  # clean(): destructor
  def clean(self):
    return True
# end of class Animation


textures = {
  
'boom1': [
'                                                 ',
'                                                 ',
'                                                 ',
'                                                 ',
'                         *                       ',
'                         *                       ',
'                        ││ _                     ',
'              \\\\       │  │        //            ',
'               \\\\      │  │       //             ',
'                \\\\    /    │     //              ',
'                 \\\\  /     \\    //               ',
'                   ──       ───                  ',
'                                                 '
],
    
    
'boom2': [
'                                                 ',
'                                \\                ',
'                                                 ',
'                               \\  \\              ',
'               /        *            \\           ',
'               //        *        \\\\\\            ',
'             ///        ││ _       \\\\            ',
'              \\\\       │  │        //            ',
'               \\\\      │  │       //             ',
'                \\\\    /    │     //              ',
'                 \\\\  /     \\    //               ',
'                   ──       ───                  ',
'                                                 '
],
    
'boom3': [
'                                                 ',
'                                *                ',
'                                \\ * /            ',
'           *   *  *            *   \\  /          ',
'            // /         *       \\   *           ',
'            / * /        *        \\\\\\            ',
'              /         ││ _       \\\\            ',
'              \\\\       │  │        //            ',
'               \\\\      │  │       //             ',
'                \\\\    /  <<      //              ',
'                 \\\\  /     \\    //               ',
'                   ──       ───                  ',
'                                                 '
],
    
'boom4': [
'                                   |    /        ',
'       \\     |   /           \\  o                ',
'         \\         /            * o *     /      ',
'           o   o  o            o   *  *          ',
'             * *        *        *   o           ',
'            * o *        *        \\\\             ',
'              *         ││ _       \\\\            ',
'              \\\\       │  │        //            ',
'               \\\\      │  │       //             ',
'                \\\\    /  xx      //              ',
'                 \\\\  /     \\    //               ',
'                   ──       ───                  ',
'                                                 '
],
    
'boom5': [
'                                   ·    ·        ',
'       ·     ·   ·           ·                   ',
'         ·         ·            o   o     ·      ',
'                                   o  o          ',
'             o o        *        o               ',
'            o   o       *                        ',
'              o         ││ _       \\\\            ',
'              \\\\       │  │        //            ',
'               \\\\      │  │       //             ',
'                \\\\    /  <<      //              ',
'                 \\\\  /     \\    //               ',
'                   ──       ───                  ',
],
    
'boom6': [
'                                                 ',
'                                                 ',
'                                                 ',
'                                   ·             ',
'             · ·         *                       ',
'            ·   ·       *           ·            ',
'              ·         ││ _       ·   ·         ',
'              \\\\       │  │        //            ',
'               \\\\      │  │       //             ',
'                \\\\    /  <<      //              ',
'                 \\\\  /     \\    //               ',
'                   ──       ───                  ',
],
    
    
    
    
    
    
    
    
    

'heart2': [
'         ',
'  XX XX  ',
' |  V  | ',
' |     | ',
'  \   /  ',
'   \ /   ',
'    Y    ',
]}


"""    
    
∩ ≡ ÷ ≈ ° · · √ ⌠⌡ ⌐¬     
 ┴┬ ├┤ ┼  ─│ └┘┌┐  ═║    
 ½ ¼ × » «  ░ ▒ ▓  
¢ £ ¥ ª º ⁿ ²
α ß Γ π Σ σ μ τ Φ Θ Ω δ ∞ φ ε
█ ▄▀ ▌▐ ■

"""
