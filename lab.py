"""6.009 Lab 10: Snek Is You Video Game"""

import doctest
from pydoc import text
from tabnanny import check
from turtle import back
from Game import Game

# NO ADDITIONAL IMPORTS!

# All words mentioned in lab. You can add words to these sets,
# but only these are guaranteed to have graphics.
SNEK = "SNEK"
FLAG = "FLAG"
ROCK = "ROCK"
WALL = "WALL"
COMPUTER = "COMPUTER"
BUG = "BUG"
NOUNS = {SNEK, FLAG, ROCK, WALL, COMPUTER, BUG}

YOU = "YOU"
WIN = "WIN"
STOP = "STOP"
PUSH = "PUSH"
DEFEAT = "DEFEAT"
PULL = "PULL"
PROPERTIES = {YOU, WIN, STOP, PUSH, DEFEAT, PULL}

AND = "AND"
IS = "IS"
MODIFIERS = {AND, IS}
WORDS = NOUNS | PROPERTIES | MODIFIERS

# Maps a keyboard direction to a (delta_row, delta_column) vector.
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
direction_vector = {
    UP: (-1, 0),
    DOWN: (+1, 0),
    LEFT: (0, -1),
    RIGHT: (0, +1),
}


def new_game(level_description):
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
    return Game(level_description)


def loc_in_bounds(game: Game, loc):
    row, col = loc
    return 0 <= row < game.height and 0 <= col < game.width


def stop_object_at_loc(game: Game, loc):
    if STOP not in game.property_to_object_map:
        return False
    for noun in game.property_to_object_map[STOP]:
        object = noun if noun in WORDS else noun.lower()
        locs = game.noun_to_locs_map[object]
        if loc in locs:
            return noun
    return False


def push_object_at_loc(game: Game, loc):
    if PUSH in game.property_to_object_map:
        for noun in game.property_to_object_map[PUSH]:
            object = noun if noun in WORDS else noun.lower()
            if object not in game.noun_to_locs_map:
                continue
            locs = game.noun_to_locs_map[object]
            if loc in locs:
                return noun
    return False


def move_push_object(game: Game, old_loc, new_loc, moving_objects):
    text_object_moved = False
    for noun in game.property_to_object_map[PUSH]:
        object = noun if noun in WORDS else noun.lower()
        if object not in game.noun_to_locs_map:
            continue

        locs = game.noun_to_locs_map[object]
        if old_loc in locs:
            # remove old_loc
            # locs[new_loc] = locs[old_loc]
            # add in new_loc
            # locs.pop(old_loc)
            move = (object, old_loc, new_loc, locs[old_loc])
            if move not in moving_objects:
                moving_objects.add(move)
        if old_loc in game.word_locs:
            text_object = game.word_locs[old_loc]
            game.word_locs.pop(old_loc)
            game.word_locs[new_loc] = text_object
            text_object_moved = True
        elif old_loc in game.modifier_locs:
            text_object = game.modifier_locs[old_loc]
            game.modifier_locs.pop(old_loc)
            game.modifier_locs[new_loc] = text_object
            text_object_moved = True

    return text_object_moved


def check_if_object_need_to_be_pulled(game, loc, direction):
    row, col = loc
    delta_row, delta_col = direction_vector[direction]
    opp_delta_row, opp_delta_col = -delta_row, -delta_col
    back_loc = (row + opp_delta_row, col + opp_delta_col)
    if PULL in game.property_to_object_map:
        for noun in game.property_to_object_map[PULL]:
            object = noun if noun in WORDS else noun.lower()
            locs = game.noun_to_locs_map[object]
            if back_loc in locs:
                return True
    return False


def pull_objects_in_back(
    game: Game, loc, direction, parse_rules_flag, pushed_object_locs, moving_objects
):
    pulled_object_locs = set()

    def helper(game, loc, direction):
        if check_if_object_need_to_be_pulled(game, loc, direction):
            if stop_object_at_loc(game, loc):
                return
            # otherwise, move and then check the back location again
            row, col = loc
            delta_row, delta_col = direction_vector[direction]
            opp_delta_row, opp_delta_col = -delta_row, -delta_col
            back_loc = (row + opp_delta_row, col + opp_delta_col)
            for noun in game.property_to_object_map[PULL]:
                object = noun if noun in WORDS else noun.lower()
                locs = game.noun_to_locs_map[object]
                if (
                    can_move(
                        game,
                        direction,
                        loc,
                        pulled_object_locs,
                        parse_rules_flag,
                        pushed_object_locs,
                        moving_objects,
                    )
                    and back_loc in locs
                ):
                    # remove old_loc
                    pulled_object_locs.add(back_loc)
                    # locs[loc] = locs[back_loc] + locs.get(loc, 0)
                    # # add in new_loc
                    # locs.pop(back_loc)
                    move = (noun, back_loc, loc, locs[back_loc])
                    if move not in moving_objects:
                        moving_objects.add(move)
                    print(f"PULLED {object} from {back_loc} to {loc}")
            helper(game, back_loc, direction)

    helper(game, loc, direction)
    return pulled_object_locs


def can_move(
    game: Game,
    direction,
    loc,
    pulled_object_locs,
    parse_rules_flag,
    pushed_object_locs,
    moving_objects,
):
    if not loc_in_bounds(game, loc):
        return False
    # if object has push and stop property, push takes priority
    push_obj_loc = push_object_at_loc(game, loc)
    if push_obj_loc:
        # if push object in front, check if that push object
        # can move forward
        delta_row, delta_col = direction_vector[direction]
        row, col = loc
        new_loc = (row + delta_row, col + delta_col)
        stop_at_curr_loc = stop_object_at_loc(game, loc)
        if (stop_object_at_loc(game, new_loc) and stop_at_curr_loc != push_obj_loc) or (
            stop_object_at_loc(game, loc) and stop_at_curr_loc != push_obj_loc
        ):
            return False
        move = (
            push_obj_loc,
            loc,
            new_loc,
            game.noun_to_locs_map[push_obj_loc].get(loc, -1),
        )

        if move in moving_objects:
            return True

        if can_move(
            game,
            direction,
            new_loc,
            pulled_object_locs,
            parse_rules_flag,
            pushed_object_locs,
            moving_objects,
        ):
            if loc not in pushed_object_locs:
                need_to_reparse_rules = move_push_object(
                    game, loc, new_loc, moving_objects
                )
                print(f"PUSHED {push_obj_loc} from {loc} to {new_loc}")
                print()
                # add new location so that if object in front
                # still needs to move, does not push object again
                pushed_object_locs.add(new_loc)
                parse_rules_flag[0] = need_to_reparse_rules
                pulled_object_locs |= pull_objects_in_back(
                    game,
                    loc,
                    direction,
                    parse_rules_flag,
                    pushed_object_locs,
                    moving_objects,
                )
            return True
        return False
    if stop_object_at_loc(game, loc):
        return False
    return True


def defeat_object_at_loc(game: Game, loc):
    if DEFEAT not in game.property_to_object_map:
        return False
    for noun in game.property_to_object_map[DEFEAT]:
        object = noun if noun in WORDS else noun.lower()
        if object not in game.noun_to_locs_map:
            continue
        if loc in game.noun_to_locs_map[object]:
            return True
    return False


def handle_defeat_cells(game: Game, locs):
    result = {}
    for loc, amt in locs.items():
        if not defeat_object_at_loc(game, loc):
            result[loc] = amt
    return result


def you_and_win_object_in_same_cell(game: Game, loc):
    for noun in game.property_to_object_map[WIN]:
        object = noun if noun in WORDS else noun.lower()
        if object not in game.noun_to_locs_map:
            continue
        locs = game.noun_to_locs_map[object]
        if loc in locs:
            return True
    return False


def check_if_player_won(game: Game):
    for noun in game.property_to_object_map[YOU]:
        object = noun if noun in WORDS else noun.lower()
        if object not in game.noun_to_locs_map:
            continue

        locs = game.noun_to_locs_map[object]
        for loc in locs:
            if you_and_win_object_in_same_cell(game, loc):
                return True
    return False


# def add_change(moving_objects, noun, old_loc, new_loc, amt):
#     if noun not in moving_objects:
#         moving_objects[noun] =


def step_game(game: Game, direction):
    """
    Given a game representation (as returned from new_game), modify that game
    representation in-place according to one step of the game.  The user's
    input is given by direction, which is one of the following:
    {'up', 'down', 'left', 'right'}.

    step_game should return a Boolean: True if the game has been won after
    updating the state, and False otherwise.
    """
    print()
    print("BEGIN STEP")
    delta_row, delta_col = direction_vector[direction]
    # pointers to flags so that operations are not repeated or we know to reparse text objects
    pulled_object_locs = set()
    pushed_object_locs = set()
    parse_rules_flag = [False]
    # mark all changes in this array and then apply all of them at the end
    # holds items like the following tuple:
    # (noun, old_loc, new_loc, amt)
    moving_objects = set()
    for noun in game.property_to_object_map[YOU]:
        object = noun if noun in WORDS else noun.lower()
        if object not in game.noun_to_locs_map:
            continue

        locs = game.noun_to_locs_map[object]
        # new_locs = {}

        # maybe instead first mark all of the objects that are going to move
        # if not moving, then simply add to the copy

        for loc, amt in locs.items():
            row, col = loc
            new_loc = (row + delta_row, col + delta_col)
            if can_move(
                game,
                direction,
                new_loc,
                pulled_object_locs,
                parse_rules_flag,
                pushed_object_locs,
                moving_objects,
            ):
                move = (noun, loc, new_loc, amt)
                if move not in moving_objects:
                    moving_objects.add(move)

                    # check if an object needs to be pulled
                    row, col = loc
                    delta_row, delta_col = direction_vector[direction]
                    opp_delta_row, opp_delta_col = -delta_row, -delta_col
                    back_loc = (row + opp_delta_row, col + opp_delta_col)
                    if back_loc not in pulled_object_locs:
                        pull_objects_in_back(
                            game,
                            loc,
                            direction,
                            parse_rules_flag,
                            pushed_object_locs,
                            moving_objects,
                        )

            # else:
            #     new_locs[loc] = amt
    # apply all changes
    for noun, old_loc, new_loc, amt in moving_objects:
        locs = game.noun_to_locs_map[noun]
        locs[old_loc] -= amt
        if locs[old_loc] == 0:
            locs.pop(old_loc)
        locs[new_loc] = locs.get(new_loc, 0) + amt

    # reparse rules if needed
    if parse_rules_flag[0]:
        game.parse_rules()
    # now remove any you objects who are in same cell as defeat objects
    for noun in game.property_to_object_map[YOU]:
        object = noun if noun in WORDS else noun.lower()
        if object not in game.noun_to_locs_map:
            continue

        locs = game.noun_to_locs_map[object]
        game.noun_to_locs_map[noun] = handle_defeat_cells(game, locs)
    result = check_if_player_won(game)
    print(game)
    print()
    print("END STEP")
    return result


def dump_game(game: Game):
    """
    Given a game representation (as returned from new_game), convert it back
    into a level description that would be a suitable input to new_game.

    This function is used by the GUI and tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    board = [[[] for _ in range(game.width)] for _ in range(game.height)]
    for noun, locs in game.noun_to_locs_map.items():
        for (row, col), amt in locs.items():
            for _ in range(amt):
                board[row][col].append(noun)
    return board
