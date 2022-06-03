"""6.009 Lab 10: Snek Is You Video Game"""

import doctest
from operator import ge
from turtle import back, position
from typing import overload
from unicodedata import name
# from attr import frozen

from setuptools import find_packages

from prev_lab import pull_chain

# NO ADDITIONAL IMPORTS!

# All words mentioned in lab. You can add words to these sets,
# but only these are guaranteed to have graphics.
NOUNS = {"SNEK", "FLAG", "ROCK", "WALL", "COMPUTER", "BUG"}
PROPERTIES = {"YOU", "WIN", "STOP", "PUSH", "DEFEAT", "PULL"}
MODIFIERS = {'AND', 'IS'}
WORDS = NOUNS | PROPERTIES | {"AND", "IS"}

# Maps a keyboard direction to a (delta_row, delta_column) vector.
direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}
opp_direction = {
    'up': 'down',
    'down': 'up',
    'left': 'right',
    'right': 'left'
}

class Game():
    def __init__(self, objs = {}, props = {}, words = {}, ids = {}, board_dims = [0, 0]):
        self.objs = objs
        self.props = props
        self.dims = board_dims
        self.words = words
        self.ids = ids
    
    def get_board_dims(self):
        return self.dims
    
    def in_bounds(self, pos):
        if 0 <= pos[0] < self.dims[0] and 0 <= pos[1] < self.dims[1]:
            return True
        return False
    
    def get_props(self):
        return self.props
    
    def get_objs(self):
        return self.objs

    def get_copy(self):
        objs = {k:v.copy() for k,v in self.objs.items()}
        props = {k:v for k,v in self.props.items()}

        return Game(objs, props, self.get_board_dims())
    
    def get_objs_at_pos(self, pos):
        output = []
        for obj, positions in self.objs.items():
            if pos in positions:
                output.append( (obj, self.objs[obj][pos]) )
        return output

def new_game(lev_des):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, where UPPERCASE
    strings represent word objects and lowercase strings represent regular
    objects (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['snek'], []],
        [['SNEK'], ['IS'], ['YOU']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.
    """
    # will hold both graphical and text object positions.
    objs = { 'snek': {}, 
             'wall': {},
             'rock': {},
             'computer': {},
             'bug': {},
             'flag': {},
             'IS': {},
             'YOU': {},
             'PULL': {},
             'PUSH': {},
             'AND': {},
             'WIN': {},
             'STOP': {},
             'DEFEAT': {},
             'SNEK': {},
             'WALL': {},
             'ROCK': {},
             'COMPUTER':{},
             'BUG': {},
             'FLAG': {}
            }
    # objs = {word:}
    props = {
        'YOU': set(), 
        'STOP': set(), 
        'PUSH': set(),
        'PULL': set(),
        'DEFEAT': set(),
        'WIN': set()
        }
    id = 0
    ids = { 'snek': {}, 
             'wall': {},
             'rock': {},
             'computer': {},
             'bug': {},
             'flag': {},
             'IS': {},
             'YOU': {},
             'PULL': {},
             'PUSH': {},
             'AND': {},
             'WIN': {},
             'STOP': {},
             'DEFEAT': {},
             'SNEK': {},
             'WALL': {},
             'ROCK': {},
             'COMPUTER':{},
             'BUG': {},
             'FLAG': {}
            }
    # will hold the rest of the words for now
    board_dims = [len(lev_des), len(lev_des[0])] # rows, cols
    words = dict()
    # for every row...
    for y in range(len(lev_des)):
        # for every column...
        for x in range(len(lev_des[0])):
            # for every item in that position...
            for i in range(len(lev_des[y][x])):
                item = lev_des[y][x][i]
                # check if its a text object 
                if item in WORDS: #NOUNS or PROPERTIES or {'IS', 'AND'}:
                    if item in objs:
                        objs[ item ][(y, x)] = objs[ item ].get( (y, x), 0 ) + 1
                        # ALL TEXT OBJECTS NEED TO HAVE THE PROPERTY PUSH
                    # if item in props["PUSH"]:
                    props['PUSH'].add(item)
                    words[(y,x)] = item

                # dealing with lowercase word (i.e. a graphical object)
                elif item.upper() in NOUNS:
                    if item in objs:
                        objs[ item ][(y, x)] = objs[ item ].get( (y, x), 0 ) + 1
    # give ids to objects
    for obj in game.objs.keys():
        for pos, amt in game.objs[obj]:
            
    # check wordsssssssssssssss
    for pos, word in words.items():
        if word in NOUNS:
            # check if rule is made vertically
            pos1 = get_new_pos(pos, 'down')
            pos2 = get_new_pos(pos1, 'down')
            if (pos1 in words and words[pos1] in MODIFIERS) and \
                (pos2 in words and words[pos2] in PROPERTIES):
                props[ words[pos2] ].add(word.lower())
            # check if rule is made horizontally
            pos1 = get_new_pos(pos, 'right')
            pos2 = get_new_pos(pos1, 'right')
            if (pos1 in words and words[pos1] in MODIFIERS) and \
                (pos2 in words and words[pos2] in PROPERTIES):
                props[ words[pos2] ].add(word.lower())
              
    print(props)
    print()
    print(objs)
    print()
    return Game(objs, props, words, board_dims)


def get_new_pos(curr_pos, direction):
    y = curr_pos[0] + direction_vector[direction][0]
    x =  curr_pos[1] + direction_vector[direction][1]
    return (y, x)

def check_new_rule(game, pos):
    pass


def get_objects_at_pos(game, pos):
    objects = []
    # go through all properties
    for property, set in game.props.items():
        # for every object that has this current property...
        for object in set:
            if pos in game.objs[object]:
                # add property and how many instances of that property are give position
                objects.append(property)
    
    return objects

def can_move(game, curr_pos, direction):
    new_pos = get_new_pos(curr_pos, direction)
    if game.in_bounds(new_pos):
        # for every object that's in the new position...
        for object, amount in game.get_objs_at_pos(new_pos):
            # if any object has the stop property, you can't move
            # so return False
            if object in game.props['STOP']:
                # unless an object has both stop and push property.
                # In which case, prioritize PUSH before STOP
                if object in game.props['PUSH']:
                    return True
                return False
        for object, amount in game.get_objs_at_pos(new_pos):
            # if there's an object with the PUSH property in new position
            # check to see if it can moved. Otherwise, return False 
            if object in game.props['PUSH']:
                return can_move(game, new_pos, direction)
        return True
    return False

def step_game(game, direction):
    """
    Given a game representation (as returned from new_game), modify that game
    representation in-place according to one step of the game.  The user's
    input is given by direction, which is one of the following:
    {'up', 'down', 'left', 'right'}.

    step_game should return a Boolean: True if the game has been won after
    updating the state, and False otherwise.
    """

    """"
    Let's talk about the snake as YOU object only for now. So before moving, 
    1. find the next and previous positions
    2. see if any objects are in either locations because they will be affected by our movement.
    3. 
    """
    result = False
    obj_changes = []
    prop_changes = []

    # have list of positions that need to be checked. Start with new position
    queue = [[obj, curr_pos, amount] for obj in game.props['YOU'] for curr_pos, amount in game.objs[obj].items() ]
    visited = set()
    # for every object with you property...
    while len(queue) != 0:
        obj, curr_pos, camount = queue.pop(0)
        # if obj in game.props['PUSH'] and obj in game.props['STOP']:

        if can_move(game, curr_pos, direction):
            # if you can move, then get the new position and the back position
            new_pos = get_new_pos(curr_pos, direction)
            prev_pos = get_new_pos(curr_pos, opp_direction[direction])

            # for every object in the new position...
            for object, namount in game.get_objs_at_pos(new_pos):
                # if object that the player controls...
                if obj in game.props['YOU'] or obj in game.props['PULL']:
                    # if push object, enqueue. Don't have to worry about not
                    # being able to move if there's a chain since can_move() checks
                    # for that
                    if object in game.props['PUSH'] and (object, new_pos) not in visited:
                        queue.append([object, new_pos, namount])
                    elif (obj in game.props['YOU'] and object in game.props['YOU']):
                        camount += namount
                    elif (obj in game.props['PULL'] and object in game.props['PULL']) and \
                        (object, new_pos) not in visited:
                        camount += namount
                elif obj in game.props['PUSH']:
                    if object in game.props['PUSH'] and (object, new_pos) not in visited:
                        queue.append([object, new_pos, namount])

            if game.in_bounds(prev_pos):
                # for every object in the back position...
                for bobject, bamount in game.get_objs_at_pos(prev_pos):
                    # any moving object can pull an object, so we just need to check if there's
                    # behind the currently moving object
                    if bobject in game.props['PULL'] and (bobject, prev_pos) not in visited:
                        queue.append([bobject, prev_pos, bamount])
            obj_changes.append([obj, curr_pos, new_pos, camount])
            visited.add( (obj, curr_pos) )

    # delete all old positions
    for i in range(len(obj_changes)):
        del game.objs[ obj_changes[i][0] ][ obj_changes[i][1] ]
        # update words if needed
        if obj_changes[i][0] in WORDS:
            del game.words[ obj_changes[i][1] ]

    for i in range(len(obj_changes)):
        game.objs[ obj_changes[i][0] ][ obj_changes[i][2] ] = obj_changes[i][3]
        # update words if needed
        if obj_changes[i][0] in WORDS:
            game.words[ obj_changes[i][2] ] = obj_changes[i][0]

    # check for new rules
    new_props = {key:set() for key in game.props.keys()}
    for pos, word in game.words.items():
        if word in NOUNS:
            # check if rule is made vertically
            pos1 = get_new_pos(pos, 'down')
            pos2 = get_new_pos(pos1, 'down')
            if (pos1 in game.words and game.words[pos1] in MODIFIERS) and \
                (pos2 in game.words and game.words[pos2] in PROPERTIES):
                new_props[ game.words[pos2] ].add(word.lower())
            # check if rule is made horizontally
            pos1 = get_new_pos(pos, 'right')
            pos2 = get_new_pos(pos1, 'right')
            if (pos1 in game.words and game.words[pos1] in MODIFIERS) and \
                (pos2 in game.words and game.words[pos2] in PROPERTIES):
                new_props[ game.words[pos2] ].add(word.lower())
        new_props['PUSH'].add(word)
    game.props = new_props


    # delete any YOU objects, if needed
    obj_changes = []
    for obj in game.props['YOU']:
        for position in game.objs[obj].keys():
            for object in game.props['DEFEAT']:
                if position in game.objs[object]:
                    obj_changes.append( (obj, position) )
    
    for obj, pos in obj_changes:
        del game.objs[obj][pos]
    
    # check if won
    for obj in game.props['YOU']:
        for position in game.objs[obj].keys():
            for object in game.props['WIN']:
                if position in game.objs[object]:
                    return True

    print(game.objs)
    print()
    print(game.props)
    print()
    print(game.words)

    return False


def dump_game(game):
    """
    Given a game representation (as returned from new_game), convert it back
    into a level description that would be a suitable input to new_game.

    This function is used by the GUI and tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    board_dims = game.get_board_dims()
    output = [ [ [] for x in range(board_dims[1])] for y in range(board_dims[0]) ]

    for obj, l in game.get_objs().items():
        for pos, amount in l.items():
            for i in range(amount):
                output[pos[0]][pos[1]].append(obj) 
                
    print(output)
    return output
