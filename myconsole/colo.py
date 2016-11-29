from constants import the_file as gg

WHITE =  '\033[40m\033[0;37m'
GRAY =   '\033[40m\033[1;30m'
RED =    '\033[40m\033[1;31m'
GREEN =  '\033[40m\033[1;32m'
YELLOW = '\033[40m\033[1;33m'
BLUE =   '\033[40m\033[1;34m'
VIOLET = '\033[40m\033[1;35m'
LBLUE =  '\033[40m\033[1;36m'
bgRED =    '\033[1;41m\033[35m'
bgGREEN =  '\033[1;42m\033[33m'
bgYELLOW = '\033[1;43m\033[32m'
bgBLUE =   '\033[1;44m\033[36m'
bgVIOLET = '\033[1;45m\033[31m'
bgLBLUE =  '\033[1;46m\033[34m'
bgGRAY =   '\033[1;47m\033[30m'

def r(x = gg.WHITE):
  if x == gg.WHITE: return WHITE
  if x == gg.GRAY: return GRAY
  if x == gg.RED: return RED
  if x == gg.GREEN: return GREEN
  if x == gg.YELLOW: return YELLOW
  if x == gg.BLUE: return BLUE
  if x == gg.VIOLET: return VIOLET
  if x == gg.LBLUE: return LBLUE
  if x == gg.bgRED: return bgRED
  if x == gg.bgGREEN: return bgGREEN
  if x == gg.bgYELLOW: return bgYELLOW
  if x == gg.bgBLUE: return bgBLUE
  if x == gg.bgVIOLET: return bgVIOLET
  if x == gg.bgLBLUE: return bgLBLUE
  if x == gg.bgGRAY: return bgGRAY
  return WHITE


'''
print('\033[1;30mGray like Ghost\033[1;m')
print('\033[1;31mRed like Radish\033[1;m')
print('\033[1;32mGreen like Grass\033[1;m')
print('\033[1;33mYellow like Yolk\033[1;m')
print('\033[1;34mBlue like Blood\033[1;m')
print('\033[1;35mMagenta like Mimosa\033[1;m')
print('\033[1;36mCyan like Caribbean\033[1;m')
print('\033[1;37mWhite like Whipped Cream\033[1;m')
print('\033[1;38mCrimson like Chianti\033[1;m')
print('\033[1;41mHighlighted Red like Radish\033[1;m')
print('\033[1;42mHighlighted Green like Grass\033[1;m')
print('\033[1;43mHighlighted Brown like Bear\033[1;m')
print('\033[1;44mHighlighted Blue like Blood\033[1;m')
print('\033[1;45mHighlighted Magenta like Mimosa\033[1;m')
print('\033[1;46mHighlighted Cyan like Caribbean\033[1;m')
print('\033[1;47mHighlighted Gray like Ghost\033[1;m')
print('\033[1;48mHighlighted Crimson like Chianti\033[1;m')


print('\033[1;33maaaaa\033[1;m\033[1;46mfff     l\033[1;mjoh')
print(8* '123456789 ')
'''