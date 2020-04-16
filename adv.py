from room import Room
from player import Player
from world import World
from utils import Queue
from utils import Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# Start at given starting room
# pick random unexplored direction, and do a DFT until we hit a dead end
# when we hit a dead end, we back-track/call BFS to find the first room with a ? for an exit

##### Plan #####
# initialize stack
# place starting_room in stack
# initialize traversal dictionary, where keys are rooms and value is array of possible exits
# traversal = {player.starting_room_id: {n:?, s:?, w:?, e:?}}

# while stack is not empty:
## add room in stack to path using - room = stack.pop() - (remember: room is the object with all the methods and properties)
## if current_room not in traversal, then add it
## get player.current_room.exits. This is an array
## loop over the exits array, and for each exit, get rooms (get neighbors)
## update traversal[player.current_room_id] = {n: 2, s:4, w:3, e:5}
## add neighbors to copy of stack

##########


# keeps going from room 0 to room 1 in a loop


def room_traversal(starting_room):
    stack = Stack()
    stack.push([starting_room])
    traversal = {}
    while stack.size() > 0:
        path = stack.pop()
        # print("path", path)
        current_room = path[-1]
        print("current_room", current_room)
        if current_room not in traversal:
            traversal[current_room.id] = {}
            # print("traversal", traversal)
            exits = player.current_room.get_exits()
            # print(f"exits for room {current_room.id}: {exits}")
            for exit in exits:
                room = player.current_room.get_room_in_direction(exit)
                # print("room from exit", room)
                if room is not None:
                    traversal[current_room.id] = {exit: room.id}
                    print("traversal after adding exits", traversal)
                    new_path = list(path)
                    new_path.append(room)
                    stack.push(new_path)
                else:
                    traversal[current_room.id] = {exit: "?"}
            player.travel(random.choice(exits))
    return traversal


t = room_traversal(world.starting_room)
print(t)

traversal_path = []


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited"
    )
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
