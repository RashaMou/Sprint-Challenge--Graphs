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
# map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
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
opposites = {"n": "s", "s": "n", "e": "w", "w": "e"}


def bfs(current_room):
    # if there are no more unvisited adjacent rooms, we do a BFS
    queue = Queue()
    queue.enqueue([current_room])
    # create a set of traversed vertices
    visited_bfs = set()
    temp_traversal_path = traversal_path.copy()
    # while queue is not empty:
    while queue.size() > 0:
        # dequeue/pop first vertex
        queue_path = queue.dequeue()
        # if not visited
        if queue_path[-1] not in visited_bfs:
            # mark as visited_bfs
            visited_bfs.add(queue_path[-1])
            # check if room has unexplored exit
            if available_directions(queue_path[-1]) is None:
                # enqueue all neighbors
                for option in queue_path[-1].get_exits():
                    new_queue_path = list(queue_path)
                    new_queue_path.append(
                        queue_path[-1].get_room_in_direction(option))
                    queue.enqueue(new_queue_path)
                    # we're not necessarily traveling to the opposite. Once we're at 5, we can either backtrack, or go
                    # forward. how do we know when to do each??
                    if "?" in visited[player.current_room.id].values():
                        for key, val in visited[player.current_room.id].items():
                            if val == "?":
                                return key
                    else:
                        player.travel(opposites[temp_traversal_path[-1]])
                        update_visited(player.current_room,
                                       opposites[temp_traversal_path[-1]])
                        traversal_path.append(
                            opposites[temp_traversal_path[-1]])
                # this is where we want to get to
                print('curr room', player.current_room.id)
                if "?" in visited[player.current_room.id].values():
                    for key, val in visited[player.current_room.id].items():
                        if val == "?":
                            return key
                temp_traversal_path.pop()
                # print('temp traversal path after pop', temp_traversal_path)
                # print('traversal path before append', traversal_path)
            else:
                print('available dirs', available_directions(queue_path[-1]))
                return available_directions(queue_path[-1])


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
        if room.get_room_in_direction(exit).id not in visited:
            visited[room.id].update({exit: "?"})
        else:
            if len(traversal_path) > 0:
                opposite_direction = opposites[traversal_path[-1]]
                visited[room.id][opposite_direction] = room.get_room_in_direction(
                    opposite_direction)
                visited[room.id].update(
                    {exit: room.get_room_in_direction(exit)})
    return visited

# after player travels, we update the value of the direction traveled in visited[current_room] dictionary


def update_visited(room, direction):
    if visited[room.id].get(direction) is not None:
        visited[room.id][direction] = room.get_room_in_direction(
            direction)

# after we add a room to visited dictionary, we update the value of the opposite direction traveled in visited[current_room] dictionary
# e.g if we just went north from room 1 to room 2, after we add room 2 to visited we update visited[room_2][s] = room_1


def get_adjacent_rooms(room):
    adjacent_rooms = []
    exits = room.get_exits()  # array
    print('exits for room', room.id, ':', exits, '\n')
    for exit in exits:
        adjacent_rooms.append(room.get_room_in_direction(exit))
    return adjacent_rooms


###### Start with depth-first traversal ######


# initialize the DF traversal:
stack = Stack()
stack.push([player.current_room])

# while len(visited.keys()) < len(room_graph.keys()):
# loop through the stack
while stack.size() > 0:
    path = stack.pop()  # gives us the last room in the stack
    # get next direction for current room
    current_room = player.current_room
    next_direction = available_directions(current_room)
    print('current_room:', current_room.id,
          'next_direction:', next_direction)
    if current_room.id not in visited:
        # adds to visited with all directions set to ?
        add_to_visited(current_room)
    if next_direction is None:
        if len(visited.keys()) < len(room_graph.keys()):
            next_direction = bfs(current_room)
            print('current room after bf', player.current_room.id)
            print('next direction after bf', next_direction)
        else:
            break
    print('visited', visited)

    # put all adjacent rooms in the stack
    adjacent_rooms = get_adjacent_rooms(player.current_room)
    if len(adjacent_rooms) > 0:
        for room in adjacent_rooms:
            if room.id not in visited:
                new_path = list(path)
                new_path.append(room)
                stack.push(new_path)
    # travel, append to traversal path, update visited graph with new direction
    update_visited(player.current_room, next_direction)
    player.travel(next_direction)
    traversal_path.append(next_direction)
    print('traversal path:', traversal_path)
    print('visited length', len(visited.keys()))


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
