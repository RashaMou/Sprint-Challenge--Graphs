## init:

x- get current room

x- add to visited
x- should look like this: {0: {n: ?, s:?, e:?, w:?}}

x- initialize stack
x- add to stack: (direction = None, previous_room = None)

## start traversal in DFT mode

x- room_info = pop -> (direction, previous)
x- current_room = current_room.id
x- previous room = room_info[1]
x- direction = room_info[0]
x- get the exits of the current room

- get the current room exits from our visited

- check if current room is in visited
- if not then add to visited
- helper function:
-     add to visited
-     should look like this: {current room: {exits...:?}}

- this should fail on the first iteration because there is no previous room:
- if previous room is not None:
- this is where we update our previous room
- visited[previous_room][direction] = current_room

- this should fail on the first iteration because there is no direction:
- update current_room exits if we have a direction (if direction is not None)
- visited[current_room][reverse_direction] = previous_room

- loop over unvisited exits / or maybe all exists?
- move in that direction
- update traversal path with direction
- update the stack -> (direction, current_room (which will become previous room))

- if there are no exits that are unvisited:
- we enter into BFT mode - probably a helper function
- bft will traverse over visited graph
- the destination is a room with question marks
- building a path to DFT traverse after finding the destination

# PLAN 2

What needs to get done:

- Output a traversal path of shortest number of directions that visits every room (total moves should be <2000)
- Must be able to go backwards if hit room with dead end
- Helper functions to find the exits in the room & the rooms they connect to

  A plan:

- Use BFS to find shortest path to the next room where the exits = "?" (should start seeing those in graph for unexplored room as stated in readme)
- Create a visited dict that stores our room's id as key & another dict as its value
  - Value dict should have all the possible exits as keys & value should be the new rooms conected
  - Use helper function talked about above to do this for us, using 'get_exits' to return possible exits
- Create a while loop that breaks when the len of visited rooms > len of room_graphs (only want to visit each room once, so once we're at final room, we want it to end)

  - Check if the current room id is a key in our visited dict
  - Use helper function to add the room to dict (`get_exits method from room class`)
  - If not, then iterate through each exit in the current room & store the exits that are unexplored('?' inside an empty list (room_exits))

  - If the len of our unexplored exits (room_exits) for curr room is 0:
    -use our BFS to return the next path of rooms from our QUEUE that have unexplored exits - Loop through the room_ids from our returned path coming from BFS - for all the exits in our current room, verify the room ids in the path exist for current room - if so append that exit direction to our traversal_path - Add in the new room id, using get_room_in_direction - Add in the new room id as a key, if its not yet logged in visited dict - Add in the current room, as the room value for the opposite direction - Travel to the exit direction using player.travel
  - Else if the length of our unexplored exits (room_exits) is > 0 (we have unexplored exits for current room)
    - Execute travel & log room entries function on the given direction & room
