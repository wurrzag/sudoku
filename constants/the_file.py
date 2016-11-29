ANIMATION_SPEED = 0.07 # pause in seconds in between animation frames

#two players plus none of them
NONE = 0
HOME = 1
AWAY = 2

#two special-positions for gangs which didn't come to play because of player had too many soldiers at his starting sector. must be >15 (there are 15 fields in game and <0 means dead)
IN_QUEUE_BORDER = 20
IN_HOME_QUEUE   = 99
IN_AWAY_QUEUE   = 100

# the passability of field factors
IMPASSABLE_ENEMY  = 10**4       # sector contains enemy
IMPASSABLE_ENGAGE = 10**8       # there is a fight in a sector
IMPASSABLE_ALLY   = 10**12      # sector contains four allies (the limit; cannot finish move here no matter what)
TRAVEL_DAYS       = 10**3       # how many turns the whole travel takes as a secondary argument, but unlike all the previous, it's always nonzero and can't be ignored at any conditions
MOVEMENT_LEFT     = -2*(10**2)  # the least important value is a movement points left the creature have after departing the final sector
BIGGER_THAN_ALL   = 10**15

# keyboard commands
ZERO = 0
ENTE = 1
UP   = 2
DOWN = 3
LEFT = 4
RIGH = 5
KEY1 = 6
KEY2 = 7
KEY3 = 8
HELP = 9
ESC  = 10
BACK = 11
SEL  = 12
CT_C = 20
ALL  = 30
FIRST_BORDER = 50

DONT_RESET_SCREEN = 70
DONT_DRAW_SCREEN  = 71
DONT_PAUSE        = 72
SECOND_BORDER = 100

# colors
NONECOLOR = 0
WHITE = 1
GRAY = 2
RED = 3
GREEN = 4
YELLOW = 5 
BLUE = 6
VIOLET = 7
LBLUE = 8
bgRED = 9
bgGREEN = 10
bgYELLOW = 11
bgBLUE = 12
bgVIOLET = 13
bgLBLUE = 14
bgGRAY = 15
bgWHITE = 16
BLACK = 20

# terrain types
BASE_H = 1
BASE_A = 2
PLAIN = 3
FOREST = 5
MOUNTAIN = 5
RIVER = 4
SWAMP = 4

# card types
NONE = 0
SQUAD = 1
SOLDIER = 1
CREATURE = 1
WALL = 2
BUILDING = 3
INTERRUPT = 4
INSTANT = 5
SORCERY = 6
ARMOR = 7
WEAPON = 8
SPELL = 9
HERO = 10


# list of abilities the creature type of card can have
# next constants are used in a way abilities[WORKER], so they must start with 0 and continue by one. Needless to say, NUMBER_OF_ABILITIES have to be the real number of abilities (biggest of them +1), otherwise the program will crash sooner or later
WORKER      = 0
NATIVE      = 1
FIRSTSTRIKE = 2
SLOWSTRIKE  = 3
FLYING      = 4
HASTE       = 5
VIGILANCE   = 6
TRAMPLE     = 7

WALLCRUSHER  = 8
PROVOKE      = 9
FLANKING     = 10
IMMUNE       = 11
FEAR         = 12
POISONOUS    = 13
SNIPER       = 14
HEALER       = 15
DECOY        = 16

THROWN     = 17
CASTER     = 18
SCOUT      = 19
FLEE       = 20
RAMPART    = 21
SPY        = 22
MENTAT     = 23
BUILDER    = 24
ILL        = 25
LEADER     = 26
COMMANDER  = 27

NUMBER_OF_ABILITIES = 28


# next constants are used in a way mana[mBLUE], so they must start with 0 and continue by one. Needless to say, NUMBER_OF_MANASYMBOLS have to be the real number of abilities (biggest of them +1), otherwise the program will crash sooner or later
mRED = 0
mGREEN = 1
mBLUE = 2
mBLACK = 3
mWHITE = 4

NUMBER_OF_MANASYMBOLS = 5


# area of effect of special effects
NONE          = 0
SELF          = 1
CHOSEN_FRIEND = 2
ALL_FRIENDS   = 3
ENGAGED_ENEMY = 4
CHOSEN_ENEMY  = 5
ALL_ENEMIES   = 6
SPECIAL       = 7
BEGIN         = 100
END           = 200



#****************************************************************
#
#               CUT'N'PASTE FROM NET --- START
#
#from __future__ import generators
class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()
#
#               CUT'N'PASTE FROM NET --- FINISH
#
#******************************************************************
