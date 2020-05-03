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
# add room in stack to path using - room = stack.pop() - (remember: room is the object with all the methods and properties)
# if current_room not in traversal, then add it
# get player.current_room.exits. This is an array
# loop over the exits array, and for each exit, get rooms (get neighbors)
# update traversal[player.current_room_id] = {n: 2, s:4, w:3, e:5}
# add neighbors to copy of stack

# current room, prev room, direction we went to, direction you came from

##########


traversal_path = []
visited = {}


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
    if room.get_room_in_direction("n") is not None and room.get_room_in_direction("n").id not in visited:
        return "n"
    elif room.get_room_in_direction("s") is not None and room.get_room_in_direction("s").id not in visited:
        return "s"
    elif room.get_room_in_direction("e") is not None and room.get_room_in_direction("e").id not in visited:
        return "e"
    elif room.get_room_in_direction("w") is not None and room.get_room_in_direction("w").id not in visited:
        return "w"
    else:
        return None


def add_to_visited(room):
    exits = room.get_exits()
    visited[room.id] = {}
    for exit in exits:
        visited[room.id].update({exit: "?"})
    return visited

# after player travels, we update the value of the direction traveled in visited[current_room] dictionary


def update_visited(room, direction):
    visited[room.id][direction] = room.get_room_in_direction(
        direction)

# after we add a room to visited dictionary, we update the value of the opposite direction traveled in visited[current_room] dictionary
# e.g if we just went north from room 1 to room 2, after we add room 2 to visited we update visited[room_2][s] = room_1


def update_opposite_room_in_visited(room):
    opposites = {"n": "s", "s": "n", "e": "w", "w": "e"}
    opposite_direction = opposites[traversal_path[-1]]
    visited[room.id][opposite_direction] = room.get_room_in_direction(
        opposite_direction)


def get_adjacent_rooms(room):
    adjacent_rooms = []
    exits = room.get_exits()  # array
    for exit in exits:
        adjacent_rooms.append(room.get_room_in_direction(exit))
    return adjacent_rooms


###### Start with depth-first traversal ######


# initialize the DF traversal:
stack = Stack()
stack.push([player.current_room])

# loop through the stack
while stack.size() > 0:
    path = stack.pop()  # gives us the last room in the stack
    print('path', path)
    # get next direction for current room
    next_direction = available_directions(player.current_room)
    # if next direction is None, then run DFT
    # we need to update the directions of the rooms we already traversed.
    current_room = player.current_room
    print('current_room', current_room.id)
    if current_room.id not in visited:
        # adds to visited with all directions set to ?
        add_to_visited(current_room)
        if current_room.id != 0:
            update_opposite_room_in_visited(current_room)
        print('visited', visited)

        # put all adjacent rooms in the stack
        adjacent_rooms = get_adjacent_rooms(current_room)
        if len(adjacent_rooms) > 0:
            for room in adjacent_rooms:
                if room.id not in visited:
                    new_path = list(path)
                    new_path.append(room)
                    stack.push(new_path)
        # travel, append to traversal path, update visited graph with new direction
        print('next direction before travel', next_direction)
        player.travel(next_direction)
        traversal_path.append(next_direction)
        update_visited(current_room, next_direction)

# else:
#     #! how to find the room with the nearest open slot??
#     print("nope")
#     # path_to_nearest_open_direction = bfs(player.current_room, open_room)
# if it IS in the visited graph, then we need to check to see what

print("traversal_path", traversal_path)
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
