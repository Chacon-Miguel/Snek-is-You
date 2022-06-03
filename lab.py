"""6.009 Lab 10: Snek Is You Video Game"""

import doctest
from operator import ge
from turtle import back, position
from typing import overload
from unicodedata import name
from attr import frozen

from setuptools import find_packages

from prev_lab import pull_chain

# NO ADDITIONAL IMPORTS!

# All words mentioned in lab. You can add words to these sets,
# but only these are guaranteed to have graphics.
NOUNS = {"SNEK", "FLAG", "ROCK", "WALL", "COMPUTER", "BUG"}
PROPERTIES = {"YOU", "WIN", "STOP", "PUSH", "DEFEAT", "PULL"}
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
    def __init__(self, objs = {}, props = {}, board = {}, board_dims = [0, 0]):
        self.objs = objs
        self.props = props
        self.dims = board_dims
        self.board = board
    
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
    
class Object:
    def __init__(self, name, properties = set(), positions = {}):
        self.name = name
        self.properties = properties
        self.positions = positions

    def has_property(self, property):
        if property in self.properties:
            return True
        return False
    
    def name(self):
        return self.name

    


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
        'YOU': {'snek'}, 
        'STOP': {'wall'}, 
        'PUSH': {'rock'},
        'PULL': {'computer'},
        'DEFEAT': {'bug'},
        'WIN': {'flag'}
        }
    
    # will hold the rest of the words for now
    board_dims = [len(lev_des), len(lev_des[0])] # rows, cols
    board = {(y, x):{} for y in range(board_dims[0]) for x in range(board_dims[1])}
    # for every row...
    for y in range(len(lev_des)):
        # for every column...
        for x in range(len(lev_des[0])):
            # for every item in that position...
            for i in range(len(lev_des[y][x])):
                # check if its a text object 
                if lev_des[y][x][i] in WORDS: #NOUNS or PROPERTIES or {'IS', 'AND'}:
                    if lev_des[y][x][i] in objs:
                        objs[ lev_des[y][x][i] ][(y, x)] = objs[ lev_des[y][x][i] ].get( (y, x), 0 ) + 1
                        # ALL TEXT OBJECTS NEED TO HAVE THE PROPERTY PUSH
                    # if lev_des[y][x][i] in props["PUSH"]:
                    props['PUSH'].add(lev_des[y][x][i])


                # dealing with lowercase word (i.e. a graphical object)
                elif lev_des[y][x][i].upper() in NOUNS:
                    if lev_des[y][x][i] in objs:
                        objs[ lev_des[y][x][i] ][(y, x)] = objs[ lev_des[y][x][i] ].get( (y, x), 0 ) + 1
                # regardless, add it to the board
                board[(y, x)][lev_des[y][x][i]] = board[(y, x)].get(lev_des[y][x][i], 0) + 1

    return Game(objs, props, board, board_dims)


def get_new_pos(curr_pos, direction):
    y = curr_pos[0] + direction_vector[direction][0]
    x =  curr_pos[1] + direction_vector[direction][1]
    return (y, x)



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
        # for object, amount in game.board[curr_pos].items():
        #     # if any object has the stop property, you can't move
        #     # so return False
        #     # if 'STOP' in game.objs[object]['props']:
        #     #     return False
        #     if object in game.props['STOP']:
        #         return False
        
        # for every object that's in the new position...
        for object, amount in game.board[new_pos].items():
            # if any object has the stop property, you can't move
            # so return False
            # if 'STOP' in game.objs[object]['props']:
            #     return False
            if object in game.props['STOP']:
                return False
        for object, amount in game.board[new_pos].items():

            # if there's an object with the PUSH property in new position
            # check to see if it can moved. Otherwise, return False 
            # elif 'PUSH' in game.objs[object]['props']:
            #     c
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

    changes = []
    # have list of positions that need to be checked. Start with new position
    queue = [[obj, curr_pos, amount] for obj in game.props['YOU'] for curr_pos, amount in game.objs[obj].items() ]
    visited = set()
    # for every object with you property...
    while len(queue) != 0:
        obj, curr_pos, camount = queue.pop(0)
        if camount != 0 and can_move(game, curr_pos, direction):
            # if you can move, then get the new position and the back position
            new_pos = get_new_pos(curr_pos, direction)
            prev_pos = get_new_pos(curr_pos, opp_direction[direction])

            changes.append([obj, curr_pos, new_pos, camount])

            # for every object in the new position...
            for object, namount in game.board[new_pos].items():
                # if object that the player controls...
                if obj in game.props['YOU'] or obj in game.props['PULL']:
                    # if push object, enqueue. Don't have to worry about not
                    # being able to move if there's a chain since can_move() checks
                    # for that
                    if object in game.props['PUSH'] and (object, new_pos) not in visited:
                        queue.append([object, new_pos, namount])
                    else:
                        changes.append([obj, curr_pos, curr_pos, camount])
                
                elif obj in game.props['PUSH']:
                    if object in game.props['PUSH'] and (object, new_pos) not in visited:
                        queue.append([object, new_pos, namount])
                    else:
                        changes.append([obj, curr_pos, curr_pos, camount])
                visited.add((object, new_pos))


            if game.in_bounds(prev_pos):
                # for every object in the back position...
                for bobject, bamount in game.board[prev_pos].items():
                    # any moving object can pull an object, so we just need to check if there's
                    # behind the currently moving object
                    if bobject in game.props['PULL'] and (bobject, prev_pos) not in visited:
                        queue.append([bobject, prev_pos, bamount])
                    else:
                        changes.append([obj, curr_pos, curr_pos, camount])
                    # visited.add((bobject, prev_pos))
        changes.append([obj, curr_pos, curr_pos, camount])
                
    # now update the game by making all changes
    # old_amts = [] # [game.board[new_pos].get(obj, 0) for obj, curr_pos, new_pos, amount in changes]
    # for obj, curr_pos, new_pos, amount in changes:
    #     if can_move(game, new_pos, direction):
    #         old_amts.append(0)
    #     else:
    #         old_amts.append(game.board[new_pos].get(obj, 0))
    
    # new_objs = {key:{'props':{}, 'pos': {}} for key in game.objs.keys()}
    # for key, d in game.objs.items():
    #     new_objs[key]['props'] = d['props'].copy()
    #     new_objs[key]['pos'] = {k:v for k,v in d['pos'].items()}


    # make new dictionaries for YOU, PUSH, and PULL objects
    poss_new_pos_obj = game.props['YOU'] | game.props['PUSH'] | game.props['PULL']
    new_dicts = {obj:{} for obj in poss_new_pos_obj}

    for i in range(len(changes)): # range(len(changes)-1, -1, -1):
        for obj, curr_pos, new_pos, amount in changes:
            if can_move(game, new_pos, direction):
                # old_amts.append(0)
                # new_objs[obj][new_pos] = amount

                # if obj in game.props['YOU']:
                #     pass
                # elif obj in game.props['PUSH']:
                #     pass
                # else:
                #     pass
                new_amt = amount
            else:
                # old_amts.append(game.board[new_pos].get(obj, 0))
                # new_objs[obj][new_pos] = amount + new_objs[obj].get(new_pos, 0)
                new_amt = amount + game.objs[obj].get(new_pos, 0)
            # if obj in game.props['YOU']:
            #     new_dicts[obj][new_pos] = new_amt
            # elif obj in game.props['PUSH']:
            #     new_dicts[obj][new_pos] = new_amt
            # else:
            #     new_dicts[obj][new_pos] = new_amt
            # # update board
            # game.board[curr_pos][obj] = 0
            # game.board[new_pos][obj] = new_objs[obj][new_pos]
            new_dicts[obj][new_pos] = new_amt
    # change current objs dictionary to the new one
    for obj, Dict in new_dicts.items():
        game.objs[obj] = Dict
    print(game.objs)
    # board_dims = game.get_board_dims()
    # output = [ [ [] for x in range(game.get_board_dims()[1])] for y in range(game.get_board_dims()[0]) ]
    # board = {(y, x):{} for y in range(board_dims[0]) for x in range(board_dims[1])}

    # for obj, l in game.get_objs().items():
    #     for pos, amount in l['pos'].items():
    #         for i in range(amount):
    #             output[pos[0]][pos[1]].append(obj) 
    #             board[pos][obj] = board[pos].get(obj, 0) + 1





        # # DON'T FUCKING USE A CHANGING BOARD TO UPDATE SHIT U DUMB SHITTTTTTTTT
        # obj, curr_pos, new_pos, amount = changes[i]
        # # game.objs[obj]['pos'][curr_pos] -= amount
        # # if game.objs[obj]['pos'][curr_pos] == 0:
        # game.objs[obj]['pos'][curr_pos] -= amount
        # game.objs[obj]['pos'][new_pos] = old_amts[i] + amount

        # # if curr_pos in game.objs[obj]['pos'] and game.objs[obj]['pos'][curr_pos] == amount:
        # #     del game.objs[obj]['pos'][curr_pos]
        # # else :
        # #     game.objs[obj]['pos'][curr_pos] = game.objs[obj]['pos'].get(curr_pos, 0) + amount
        # # game.objs[obj]['pos'][new_pos] = old_amts[i] + amount

        # # game.objs[obj]['pos'][curr_pos] -= amount
        # # if game.objs[obj]['pos'][curr_pos] == 0:
        # #     del game.objs[obj]['pos'][curr_pos]
        # # game.objs[obj]['pos'][new_pos] = old_amts[i] + amount - game.objs[obj]['pos'].get(new_pos, 0)


        # # game.board[curr_pos][obj] -= amount
        # game.board[curr_pos][obj] = 0
        # game.board[new_pos][obj] = old_amts[i] + amount
        # # update board


        # # if obj in game.board[curr_pos] and game.board[curr_pos][obj] == amount:
        # #     del game.board[curr_pos][obj]
        # # else:
        # #     game.board[curr_pos][obj] -= amount
        # # game.board[new_pos][obj] = old_amts[i] + amount

        # # game.board[curr_pos][obj] -= amount
        # # if game.board[curr_pos][obj] == 0:
        # #     del game.board[curr_pos][obj]
        # # game.board[new_pos][obj] = old_amts[i] + amount - game.board[new_pos].get(obj, 0)


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
    # print(game.objs)
    # print()
    # print(game.props)
    board_dims = game.get_board_dims()
    output = [ [ [] for x in range(game.get_board_dims()[1])] for y in range(game.get_board_dims()[0]) ]
    board = {(y, x):{} for y in range(board_dims[0]) for x in range(board_dims[1])}

    for obj, l in game.get_objs().items():
        for pos, amount in l.items():
            for i in range(amount):
                output[pos[0]][pos[1]].append(obj) 
                board[pos][obj] = board[pos].get(obj, 0) + 1
    # for pos, obj_info in game.board.items():
    #     for obj, amount in obj_info.items():
    #         for i in range(amount):
    #             output[pos[0]][pos[1]].append(obj)
    # print(output)
    game.board = board
    return output
