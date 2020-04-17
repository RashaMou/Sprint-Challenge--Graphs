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
