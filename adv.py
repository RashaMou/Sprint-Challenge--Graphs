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
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

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


def bfs():
    visited_bfs = set()
    q = Queue()
    room = player.current_room

    q.enqueue([room.id])

    while q.size() > 0:
        # deque the list path of unexplored rooms
        path = q.dequeue()
        # room = last item in path (gives us room.id)
        room = path[-1]
        # Check if room is in our visted BFS set
        if room not in visited_bfs:
            # Add to bfs set if not
            visited_bfs.add(room)
            # For all the keys in our visited_rooms[current_room]
            print("room to check", room, "path", path)
            for direction in visited[room].keys():  # e, w, s, etc
                # look for visited_room[room][direction] == ? (we assume room is already in visited dict, b/c first thing we did in main loop is add it)
                # our search target
                if (visited[room][direction] == '?'):
                    # return path of room ids
                    return path
                # If given room for visited_rooms[curr room][direction] isn't in our visited set:
                elif (visited[room][direction] not in visited_bfs):
                    # copy our path of rooms & add that connected room (from our visited_room[current room][direction])
                    # add it to queue to  be added to visited & check for unexplored rooms
                    copy_path = path.copy()
                    copy_path.append(visited[room][direction])
                    q.enqueue(copy_path)
    return path

# def bfs(current_room):
#     # if there are no more unvisited adjacent rooms, we do a BFS
#     queue = Queue()
#     queue.enqueue([current_room])
#     # create a set of traversed vertices
#     visited_bfs = set()
#     temp_traversal_path = traversal_path.copy()
#     # while queue is not empty:
#     while queue.size() > 0:
#         # dequeue/pop first vertex
#         queue_path = queue.dequeue()
#         # if not visited
#         if queue_path[-1] not in visited_bfs:
#             # mark as visited_bfs
#             visited_bfs.add(queue_path[-1])
#             # check if room has unexplored exit
#             if "?" in visited[player.current_room.id].values():
#                 for key, val in visited[player.current_room.id].items():
#                     if val == "?":
#                         return key
#             else:
#                 # enqueue all neighbors
#                 for option in player.current_room.get_exits():
#                     new_queue_path = list(queue_path)
#                     new_queue_path.append(
#                         player.current_room.get_room_in_direction(option))
#                     queue.enqueue(new_queue_path)
#                 if opposites.get(temp_traversal_path[-1]):
#                     player.travel(opposites[temp_traversal_path[-1]])
#                     traversal_path.append(
#                         opposites[temp_traversal_path[-1]])
#                 # for option in queue_path[-1].get_exits():
#                 #     new_queue_path = list(queue_path)
#                 #     new_queue_path.append(
#                 #         queue_path[-1].get_room_in_direction(option))
#                 #     queue.enqueue(new_queue_path)
#                 # if opposites.get(temp_traversal_path[-1]):
#                 #     player.travel(opposites[temp_traversal_path[-1]])
#                 #     traversal_path.append(
#                 #         opposites[temp_traversal_path[-1]])
#             temp_traversal_path.pop()


def add_to_visited(room):
    exits = room.get_exits()
    visited[room.id] = {}
    for exit in exits:
        visited[room.id].update({exit: "?"})
    return visited


def adjacent_unexplored_exits(room):
    unexplored_exits = []
    exits = room.get_exits()
    print('exits for room', room.id, ':', exits, '\n')
    for exit in exits:
        print('exit', exit, 'room', player.current_room.id)
        print('visited for room', visited[player.current_room.id])
        if visited[player.current_room.id][exit] == '?':
            unexplored_exits.append(exit)
    return unexplored_exits


def travel(direction):
    # append direction to traversal path
    traversal_path.append(direction)
    # get room we just traveled to
    next_room = player.current_room.get_room_in_direction(direction)
    # update current room's direction's with next room
    visited[player.current_room.id][direction] = next_room.id
    # if next room is not in visited, then add it and update its direction with opposite
    if (next_room.id not in visited):
        add_to_visited(next_room)
    visited[next_room.id][opposites[direction]] = player.current_room.id
    player.travel(direction)


###### Start with depth-first traversal ######

# continue moving while our visited list is less than the total number of rooms
while (len(visited) < len(room_graph)):
    # if current room is not in visited, then add it
    if player.current_room.id not in visited:
        add_to_visited(player.current_room)
    # find all the unexplored exits in curr room & store it in list we can randomly choose to travel to
    unexplored_exits = adjacent_unexplored_exits(player.current_room)

    # if there are unexplored exits, then assign a random direction to travel, and call travel method
    if len(unexplored_exits) > 0:
        next_direction = random.choice(unexplored_exits)
        travel(next_direction)
    # if there are no unexplored exits, then call bfs to find nearest room with unexplored exit
    else:
        backtrack_path = bfs()
        for unexplored_room in backtrack_path:
            for direction in visited[player.current_room.id]:
                if (direction in visited[player.current_room.id]):
                    # if unexplored room from path bfs is connected to our current room, travel there & log entries:
                    if (visited[player.current_room.id][direction] == unexplored_room and player.current_room.id != unexplored_room):
                        travel(direction)


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
