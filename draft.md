# Draft notes

- [ ] add a mode in which tasks are bumped to another column based on answer

    - [X] move the task performing out into another file
        - [X] Please extract everything that performs the action into a separate python file.
        - [X] Extract the while loop from main as an own function "work".

    - [X] add a parameter --work for the old action
    - [X] add a new parameter --cleanup that will start the new action

    - [X] get all tasks from all lists
    - [ ] get a list of all lists that exist in the board
    - [ ] ask for all tasks
        - [ ] To which of the following lists does this task belong? 1. 2. 3... or d-> delete task
        - [ ] move task accordingly
