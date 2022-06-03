"""6.009 Lab 10: Snek Is You Video Game"""

import doctest
from turtle import position
from typing import overload

from setuptools import find_packages

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

class Object():
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def get_position(self):
        return self.position
    
    def set_position(self, new_pos):
        if not isinstance(new_pos) == list:
            raise Exception
        else:
            self.position = new_pos

class Graphical(Object):
    def __init__(self, name, position, properties = set()):
        super.__init__(self, name, position)
        self.properties = properties
            
    def set_property(self, property):
        self.properties.add(property)
    
    def has_property(self, property):
        if property in self.properties:
            return True
        return False

class Text(Object):
    def __init__(self, name, position):
        super.__init__(self, name, position)
    


class Game():
    def __init__(self, objs = {}, props = {},  board_dims = [0, 0]):
        self.objs = objs
        self.props = props
        self.dims = board_dims
        # self.board = board
    
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
             'flag': {}
            }
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
                    else:
                        objs[ lev_des[y][x][i] ] = {(y, x): 1}
                        # ALL TEXT OBJECTS NEED TO HAVE THE PROPERTY PUSH
                    # if lev_des[y][x][i] in props["PUSH"]:
                    props['PUSH'].add(lev_des[y][x][i])


                # dealing with lowercase word (i.e. a graphical object)
                elif lev_des[y][x][i].upper() in NOUNS:
                    if lev_des[y][x][i] in objs:
                        objs[ lev_des[y][x][i] ][(y, x)] = objs[ lev_des[y][x][i] ].get( (y, x), 0 ) + 1
                    else:
                        objs[ lev_des[y][x][i] ] = {(y, x): 1}

    return Game(objs, props, board_dims)


def get_new_pos(curr_pos, direction):
    y = curr_pos[0] + direction_vector[direction][0]
    x =  curr_pos[1] + direction_vector[direction][1]
    return (y, x)

def can_move(game, curr_pos, direction):
    new_pos = get_new_pos(curr_pos, direction)
    prev_pos = get_new_pos(curr_pos, opp_direction[direction]) 
    if game.in_bounds(new_pos):
        # check if any STOP objects in new position
        for object in game.props['STOP']:
            if new_pos in game.objs[object] and curr_pos not in game.objs[object]:
                print(game.objs[object])
                return False #can_move(game, new_pos, direction)
        # check if any PUSH objects in front
        # for object in game. 
        for object in game.props['PUSH']:
            if new_pos in game.objs[object]:
                return can_move(game, new_pos, direction)
        
        # for object in game.props['PULL']:
        #     if get_new_pos(curr_pos, opp_direction[direction]) in game.objs[object]:
        #         return can_move(game, new_pos, direction)
        return True
    return False

def push_chain(game, curr_pos, obj, direction, from_pull = False):
    # can move SHOULD ensure that we're only dealing with objects with the push property
    new_pos = get_new_pos(curr_pos, direction)
    # move any push property objects, if needed
    for object in game.props['PUSH']:
        if new_pos in game.objs[object]:
            push_chain(game, new_pos, obj, direction)
    else:
        # if not from_pull:
        #     for p_object in game.props['PULL']:
        #         if get_new_pos(curr_pos, opp_direction[direction]) in game.objs[p_object] and \
        #             can_move(game, get_new_pos(curr_pos, opp_direction[direction]), direction):
        #             pull_chain(game, get_new_pos(curr_pos, opp_direction[direction]), p_object, direction, True)
        # else:
        # PUSH property objects can't overlap, so the amount will always be one
        game.objs[obj][new_pos] = 1
        del game.objs[obj][curr_pos]        


def pull_chain(game, curr_pos, obj, direction, from_push = False):
    for object in game.props['PULL']:
        new_pos = get_new_pos(curr_pos, direction)
        positions = []

        def recursive_helper(game, curr_pos, direction):
            if can_move(game, curr_pos, direction):
                positions.append(curr_pos)
                pos = get_new_pos(curr_pos, direction)
                if not from_push:
                    for p_object in game.props['PUSH']:
                        # if the player's new position is taken by an object that has the property push...
                        if pos in game.objs[p_object] and can_move(game, pos, direction):
                            push_chain(game, pos, p_object, direction, True)
                            break

                if get_new_pos(positions[-1], opp_direction[direction]) in game.objs[object]:
                    recursive_helper(game, get_new_pos(positions[-1], opp_direction[direction]), direction)
        
        recursive_helper(game, curr_pos, direction)
        print(game.objs[obj].get(new_pos, 0))
        print('positons begin')
        for pos in positions:
            print(pos, game.objs[obj].get(pos, 0))
        print('positions end')
        game.objs[obj][new_pos] = game.objs[obj][positions[-1]] + game.objs[obj].get(new_pos, 0)
        del game.objs[obj][positions[-1]]

        print(new_pos, game.objs[obj][new_pos])

def step_game(game, direction):
    """
    Given a game representation (as returned from new_game), modify that game
    representation in-place according to one step of the game.  The user's
    input is given by direction, which is one of the following:
    {'up', 'down', 'left', 'right'}.

    step_game should return a Boolean: True if the game has been won after
    updating the state, and False otherwise.
    """
    # Move all YOU objects
    old_positions = {}
    new_positions = {}
    # for every object that can move...
    for obj in game.props['YOU']:
        old_positions[obj] = []
        new_positions[obj] = []

        for curr_pos, amount in game.objs[obj].items():
            # add direction vector to get new position
            new_pos = get_new_pos(curr_pos, direction)
            # if the new position is in bounds of the board...
            if game.in_bounds(new_pos):
                objects = []
                # check if any object with stop property is in front of snake
                # for every object that has the property STOP...
                for object in game.props['STOP']:
                    # if wall in front of snake, don't move
                    if new_pos in game.objs[object]:
                        return
                # check if there's an item in front that needs to be push, or if there's a chain of them
                # for every object that has the property PUSH...
                for object in game.props['PUSH']:
                    # if the player's new position is taken by an object that has the property push...
                    if new_pos in game.objs[object] and can_move(game, new_pos, direction):
                        push_chain(game, new_pos, object, direction)
                        return
                # else:
                # check if there's an item in front that needs to be pulled, or if there's a chain of them
                # if can_move(game, curr_pos, direction):
                for object in game.props['PULL']:
                    # opp_direction = (-direction_vector[direction][0], -direction_vector[direction][1])
                    # if there's an object that needs to be pulled...
                    if get_new_pos(curr_pos, opp_direction[direction]) in game.objs[object] and \
                        can_move(game, get_new_pos(curr_pos, opp_direction[direction]), direction):
                        # # for any pushable object...
                        # for a_object in game.props['PUSH']:
                        #     # if it's in front of our snake, then don't let the snake pull because the rock in front will do it
                        #     if new_pos in game.objs[a_object] and can_move(game, new_pos, direction) :
                        #         break
                        # else:
                        pull_chain(game, get_new_pos(curr_pos, opp_direction[direction]), object, direction)
                        # get_new_pos(curr_pos, opp_direction[direction])
                        return

            # # if no wall in front of snake, then you can move to new spot
            # if can_move(game, curr_pos, direction):
                # else:
                old_positions[obj].append(curr_pos)
                new_positions[obj].append([new_pos, amount])



# update all positions
    for obj, positions in old_positions.items():
        for pos in positions:
            del game.objs[obj][pos]
    for obj, l in new_positions.items():
        for pos, amount in l:
            game.objs[obj][pos] = game.objs[obj].get(pos, 0) + amount

    
    # # # evaluate DEFEAT after all other moves
    # for object in game.props['DEFEAT']:
    #     # for all moved objects...
    #     for obj, positions in new_positions.items():
    #         for pos in positions:
    #             # if the player controls them and on top of bug...
    #             if obj in game.props['YOU'] and pos in game.objs[object]:
    #                 game.objs[obj][pos] = game.objs[obj].get(pos, 1) -1
    #             # # for every object the player controls...
    #             # for pos, amt in game.objs[c_obj].items():
    #             #     # check if 
    #             #     if pos in game.objs[object]:
    #                     # game.objs[obj][pos] = amt -1
                

    
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
    output = [ [ [] for x in range(game.get_board_dims()[1])] for y in range(game.get_board_dims()[0]) ]
    for obj, l in game.get_objs().items():
        for pos, amount in l.items():
            for i in range(amount):
                output[pos[0]][pos[1]].append(obj) 
    
    return output
