# Draft notes

- [ ] add a mode in which tasks are bumped to another column based on answer

    - [X] move the task performing out into another file
        - [X] Please extract everything that performs the action into a separate python file.
        - [X] Extract the while loop from main as an own function "work".

    - [X] add a parameter --work for the old action
    - [X] add a new parameter --cleanup that will start the new action

    - [X] get all tasks from all lists
    - [X] get a list of all lists that exist in the board
    - [X] go through all tasks in random order:
        - [X] for each task give the user a list of the lists and another option d in a menu. 
        - [X] for simplicity the list of the lists should be enumerated, so the user can select a specific list by just giving you a number
        - [X] The selection of a number means that the program should move the task into the specified list.
        - [X] Pressing d means, that the task can be deleted
        - [X] No input means that the loop should stop here

