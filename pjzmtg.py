import sys
from core import game

# if you want to have the possibility of debug screen available, look for "elif key == '___Info_screen':" string in core/state.py and study the comment lines there
#
# you can have the possibility to get to debug screen anywhere within program (except Table) but you need to set it separatelly for every room(screen) you want to jump there from; mentioned comment lines are describing the process
# previous (line) is made in classes/parser.py; easiest way is to make copy of "if key == '___Game':" line for returning the program to original point later and modify the 'gg.ENTE' value there to '___Info_screen'; that way you get info screen anytime you press enter on main screen ('___Game') (use 'gg.BACK' for backspace)
# but even if you execute the procedure described by previous line, you still need to modify the "elif key == '___Info_screen':" section mentioned in first line to switch or rewrite what the screen will include and what will not
#
# if you wanna use conventional print for debug, include ';gg.getch()' (ie pause) at the end of print line if you don't wanna scroll the screen to see the print

def mloop():
         gm = game.Manager(); gm.run()  
         gm.clean(); del gm; sys.modules[__name__].__dict__.clear()
         return True
mloop()


'''

                             THE ORIGINAL CONCEPT

·                                                                             ·
·                      █▀▀▀▀▀▀▀▀▀▀▀█       █▀▀▀▀▀▀▀▀▀▀▀█  /    █▀▀▀▀▀▀▀▀▀▀▀█  ·
·                      ▌   cl_gm   ▐       ▌battlefield▐ <════ ▌   cl_bf   ▐  ·
·                      █▄▄▄▄▄▄▄▄▄▄▄█       █▄▄▄▄▄▄▄▄▄▄▄█  \    █▄▄▄▄▄▄▄▄▄▄▄█  ·
·                            v                   v                            ·
·                            ║                   ║                            ·
·                            ║                   ║                            ·
·                           \║/                 \║/                           ·
·                            v                   v                            ·
·                      █▀▀▀▀▀▀▀▀▀▀▀█  /    █▀▀▀▀▀▀▀▀▀▀▀█                      ·
·                      ▌   game    ▐ <════ ▌   state   ▐                      ·
·                      █▄▄▄▄▄▄▄▄▄▄▄█  \    █▄▄▄▄▄▄▄▄▄▄▄█                      ·
·                            ^                                                ·
·                           /║\                                               ·
·                            ║                                                ·
·                            ║                                                ·
·                            ^                                                ·
·  █▀▀▀▀▀▀▀▀▀▀▀█    \  █▀▀▀▀▀▀▀▀▀▀▀█  /    █▀▀▀▀▀▀▀▀▀▀▀█                      ·
·  ▌  console  ▐ ════> ▌  screen   ▐ <════ ▌ textures  ▐                      ·
·  █▄▄▄▄▄▄▄▄▄▄▄█    /  █▄▄▄▄▄▄▄▄▄▄▄█  \    █▄▄▄▄▄▄▄▄▄▄▄█                      ·
·                                                                             ·

cl_bf : data Classes
cl_gm : program Classes




                             THE STRUCTURE AS IT IS

·                                                                             ·
·                      █▀▀▀▀▀▀▀▀▀▀▀█       █▀▀▀▀▀▀▀▀▀▀▀█  /    █▀▀▀▀▀▀▀▀▀▀▀█  ·
·                      ▌   table   ▐       ▌battlefield▐ <════ ▌   cl_bf   ▐  ·
·                      █▄▄▄▄▄▄▄▄▄▄▄█       █▄▄▄▄▄▄▄▄▄▄▄█  \    █▄▄▄▄▄▄▄▄▄▄▄█  ·
·                            v                   v               Effect       ·
·                            ║                   ║               Signal       ·
·                            ║                   ║               Parser       ·
·                           \║/                 \║/                           ·
·                            v                   v                            ·
·  █▀▀▀▀▀▀▀▀▀▀▀█  /    █▀▀▀▀▀▀▀▀▀▀▀█  /    █▀▀▀▀▀▀▀▀▀▀▀█  /    █▀▀▀▀▀▀▀▀▀▀▀█  ·
·  ▌   main    ▐ <════ ▌   game    ▐ <════ ▌   state   ▐ <════ ▌   cl_gm   ▐  ·
·  █▄▄▄▄▄▄▄▄▄▄▄█  \    █▄▄▄▄▄▄▄▄▄▄▄█  \    █▄▄▄▄▄▄▄▄▄▄▄█  \    █▄▄▄▄▄▄▄▄▄▄▄█  ·
·                                                ^               Battlefield  ·
·                                               /║\              Player       ·
·                                                ║               Card         ·
·                                                ║                            ·
·                                                ^                            ·
·                      █▀▀▀▀▀▀▀▀▀▀▀█    \  █▀▀▀▀▀▀▀▀▀▀▀█  /    █▀▀▀▀▀▀▀▀▀▀▀█  ·
·                      ▌  console  ▐ ════> ▌  screen   ▐ <════ ▌ textures  ▐  · 
·                      █▄▄▄▄▄▄▄▄▄▄▄█    /  █▄▄▄▄▄▄▄▄▄▄▄█  \    █▄▄▄▄▄▄▄▄▄▄▄█  ·
·                                                              (and screens)  ·

cl_bf : data Classes
cl_gm : program Classes



./
│
├── pjzmtg.py (main)     ---- this file
│  
│       
│       
├── ./cgame/             ---- data structure classes (level 4)
│        │
│        │
│        ├── bf.py       ---- Battlefield() - the main data structure of a game; includes all the other
│        │
│        ├── card.py     ---- Card()        - multiinstance of the (for player) most important specific data structure
│        │
│        ├── cdr.py      ---- Card_list()   - manager of multiple Card()s. Serves as library, hand and grave for a player
│        │
│        ├── field.py    ---- Field()       - areal unit in this game. Battlefield() contains 15 of them
│        │
│        ├── gang.py     ---- Gang()        - structure loosely derived from Card(); card is visible in hand and Gang in the battlefield
│        │                                    the process of 'casting the Card'- ie remaking it to Gang is the main way user interference with game
│        │
│        ├── glist.py    ---- Gang_list()   - manager of multiple Gang()s. Serves as a list of all soldiers in the game
│        │
│        └── player.py   ---- Player()      - there are two players, both have several Card_lists() and few of classical rpg/tbs attributes
│       
│       
│       
│       
├── ./classes/           ---- program maintenance classes (level 3)
│        │
│        │
│        ├── effect.py   ---- Effect() - list of program interrupts, (level 1,2 classes inventory)
│        │
│        ├── parser.py   ---- Parser() - data processing class with no variables
│        │
│        ├── shelp.py    ---- Help()   - minor class available exclusivelly in Screen()
│        │
│        ├── signal.py   ---- Signal   - all common switches of the game (level 4 classes inventory, commonly used in level 1,2 too)
│        │
│        └── table.py    ---- Table()  - displaying some menu and returning (through Effect()) the result; have a link to Screen()
│       
│       
│       
├── ./constants/         ---- program constants
│        │
│        └── the_file.py ---- here they go
│       
│       
│       
│       
├── ./core/              ---- main loop and interface classes (level 1,2)
│        │
│        │
│        ├── anim.py     ---- Animation() - class for displaying a sequence of ascii pictures; have a link to Screen()
│        │
│        ├── game.py     ---- Manager()   - main loop (level 1)
│        │
│        ├── screen.py   ---- Screen()    - main 'graphics' of a game; in direct control of Console()
│        │
│        ├── state.py    ---- State()     - crossroad of a program (level 2); directs Battlefield() and Screen() and refreshed by Manager()
│        │
│        ├── text.py     ---- Textures()  - list of ascii textures, most of them used repetitevelly; directed by Screen()
│        │
│        └── table.py    ---- Table()     - displaying some menu and returning (through Effect()) the result.
│       
│       
│       
│       
├── ./data/              ---- definition and description of game elements (cards)
│        │
│        │
│        ├── abilities   ---- flavor text of all in-game abilities (characteristic of both Card() ang Gang())
│        │
│        ├── cards       ---- definition of all cards ie the very main text-based data for the game
│        │
│        └── config      ---- config file of a game
│       
│          (if other files are here, they are deletable backup)
│       
│       
│       
│       
├── ./decks/            ---- pre-defined and user-created decks (army for one specific game)
│        │
│        ├── default1   ---- one of two decks currently in use
│        └── default2   ----            ─── '' ───
│          (other files are useful modifications)
│       
│       
│
│       
├── ./myconsole/
│        │
│        └── terminal.py --- Console() - 2d array representing the screen able to draw itself
│
│
│
│
├── ./screens/          ---- background screens to use in screen.py
│        │
│        ├── start
│        ├── battlefield
│        └── ...
│
│
└── ./txt/              ---- similar to ./data/ ; more plain-text oriented
       │
       └──── (lot of files)



please note: all classes outside of ./cgame/ (plus Battlefield) are single instances

'''
