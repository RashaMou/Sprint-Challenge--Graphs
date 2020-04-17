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
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
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

# current room, prev room, direction we went to, direction you came from

##########


# keeps going from room 0 to room 1 in a loop

traversal_path = []
visited_graph = {}


def bfs(current_room, target_room):
    # if there are no more unvisited adjacent rooms, we do a BFS
    qq = Queue()
    qq.enqueue([current_room])
    # create a set of traversed vertices
    visited = set()
    # while queue is not empty:
    while qq.size() > 0:
        # dequeue/pop first vertex
        qq_path = qq.dequeue()
        # if not visited
        if qq_path[-1] not in visited:
            # DO THE THING!!!!!!!
            if qq_path[-1] == target_room:
                return qq_path
            # mark as visited
            visited.add(qq_path[-1])
            # enqueue all neighbors
            for option in qq_path[-1].get_exits():
                new_qq_path = list(qq_path)
                new_qq_path.append(qq_path[-1].get_room_in_direction(option))
                qq.enqueue(new_qq_path)


def available_directions(room):
    if room.get_room_in_direction("n") is not None:
        return "n"
    elif room.get_room_in_direction("s") is not None:
        return "s"
    elif room.get_room_in_direction("e") is not None:
        return "e"
    elif room.get_room_in_direction("w") is not None:
        return "w"


def add_to_visited(room):
    visited.add(room.id)
    exits = room.get_exits()
    visited_graph[room.id] = {}
    for exit in exits:
        print(exit)
        visited_graph[room.id][exit] = room.get_room_in_direction(exit).id
    return visited_graph


def get_adjacent_unvisited_rooms(room):
    adjacent_rooms = []
    exits = room.get_exits()  # array
    for exit in exits:
        if room.get_room_in_direction(exit).id not in visited:
            adjacent_rooms.append(room.get_room_in_direction(exit))
    return adjacent_rooms


###### Start with depth-first traversal ######

# initialize the traversal:
stack = Stack()
stack.push([player.current_room])
visited = set()

# loop through the stack
while stack.size() > 0:
    path = stack.pop()  # gives us the last room in the stack
    player.current_room.id
    next_direction = available_directions(player.current_room)
    # next_direction = get_next_room(player.current_room, path[-1])
    # if last room in stack is not in visited, check what directions we have available:
    if path[-1].id not in visited:
        if next_direction != None:
            player.travel(next_direction)
            traversal_path.append(next_direction)
        # add to visited_graph and visited set
        add_to_visited(path[-1])
        print("visited_graph", visited_graph)
        print("visited", visited)
        # loop through all adjacent rooms.
        # if that room is not in visited, add it to the stack
        # if all of them ARE in visited, then call BFS to the nearest room with an unvisited adjacent room
        adjacent_rooms = get_adjacent_unvisited_rooms(player.current_room)
        if len(adjacent_rooms) > 0:
            for room in adjacent_rooms:
                new_path = list(path)
                new_path.append(room)
                stack.push(new_path)
        else:
            #! how to find the room with the nearest open slot??
            print("nope")
            # path_to_nearest_open_direction = bfs(player.current_room, open_room)


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
