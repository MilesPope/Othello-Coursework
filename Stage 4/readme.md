# What is Included in this File?
For each module/file, this document will include:
1.  Flow diagrams of the algorithms used.
2.  Explanations of how the code functions and what each module does.
3.  The reasoning behind the choices made – i.e. why each module works the way it does.

Helper functions have been ommitted from this document for the sake of brevity, as their logic is trivial.

---
# components.py
This module primarily contains functions that are used to initialise components of the game. Additionally, the module contains some fuctions that allow for CLI debugging (print_board), and a function that checks a move's legality.
## initialise_board
This function creates a new board for Othello as a 2D array, containing the first four tokens in the center of the board
### Parameters and Return Type
The only parameter of this function is the size of the board to be created. The size argument indicates the amount of rows, and how many cells are contained in each row. As such, this argument is taken to be an integer. 
The function returns a 2D array representing the board, with None entries representing unoccupied cells, and "Light" and "Dark" entries representing the owner of occupied cells. 

### Logic of the Function 
![Flowchart for initialise_board](/othello/Stage%204/images/initialise_board_flowchart.png)

### Decisions made and Reasoning 
When writing this function I chose to first initialise and empty board, and then add the starting tokens. Adding starting tokens could have been done with a conditional within the row by row creation for the board. I decided against this approach as separating board initialisation from token placement improved clarity and made the logic easier to process.

## legal_move
This function checks whether a given placement of a counter at a given set of coordinates by a given player counts as a legal move or not.
### Parameters and Return Type
The parameters of the function are the colour of the token being placed, the coordinates of the token and the board that is being checked.
It will return a boolean value that represents whether the move given is legal or not. 

### Logic of the Function
![flowchart for legal_move](/othello/Stage%204/images/legal_move_flowchart.png)

### Decisions made and Reasoning
The most logical abstraction I found for checking whether a given move was legal or not was to take the given coordinate and draw lines in each ordinal and cardinal direction. For each of these lines, we define a legal move to have the following criteria:
1. The line has at least one enemy peice following the coordinate
2. The line can be terminated by an allied peice
3. The are no empty cells between the coordinate and a terminating allied peice
If we find a single line that meets this criteria, then the move is legal and we return true. If we get through all possible lines without returning true, then the move is illegal. 
One alternate way this could have been acheived is for each line creating an array of tokens in the line until it reaches the end of the board, and then analysing this array. This approach was not chosen for implementation as this introduces another logical step of assembling the line, and additional variables. The appraoch implemented aims to minimise the amount of variables that are needed to be introduced as to keep the process as simple as possible. 

# game_engine.py
This module contains the core functionality for the game such as outflanking tokens, and defining the structure the game state is to be stored in (though this is explored later in 'Game State Persistance), and provide a simple game loop for intermediate manual testing through the command line interface.

## outflanked
This function handles the flipping of tokens that are made outflanked by a player's move.

### Parameters and Return Type
The parameters function are the board, and the colour and coordinates of the token being placed. 
It returns the updated board after the outflanked tokens are flipped to the colour of the player who made the move.

### Logic of the Function
This function uses the same logic as stated in legal_move with classification of a 'valid line'. As such, this logic is not restated here.

![flowchart for outflanked](/othello/Stage%204/images/outflanked_flowchart.png)

### Decisions made and Reasoning
I chose for this function to use the same logic as in legal_move as it had been proven to work in the implementation of legal_move. This function was mostly an extention of that function.
Another key decision I made when writing this function was not to place the token outflanking the other tokens. This was because this function would later be used in the ai_opponent module where it was necissary to calculate the amount of tokens flipped by a given move.

## simple_game_loop
This function serves as the means for intermediate manual testing through CLI. It allows for the game to be played using the functions in components.py as well as the other functions in game_engine.py. The user plays as both dark and light in the game.

### Parameters and Return Type
For this function it is not necissary to take any parameters or return anything as it is the implementation of the game. 

### Logic of the Function

The logic of the simple game loop is practically identical to the logic of Othello/Reversi. Using the functions already stated, it becomes simple to write a barebones version of the game for functionality in the CLI.

![flowchart for simple game loop](/othello/Stage%204/images/simple_game_loop_flowchart.png)

# app.py - the Flask Logic
This module contains the logic for the GUI implementation using the Flask library. These functions do not have parameters but do return information which is handled on the front-end HTML/JS code.

## index: app.route("/")
This is the function that is ran when the user opens or refreshes the web page. It contains the functionality to initialise the game and provide the information necissary for the GUI to function.

### Returned Information
This function returns the rendered template using the board.html file including information on who's turn it is, and the board.

### Logic of the Function
In regarding to the initialisation of the variables for the board, there are three main cases that need to be considered:
1. There is already a game state to be loaded from a JSON file
2. There is not already a game state to be loaded from a JSON file
3. A new game instance needs to be created
The game state has been created, we can then render the board.
![Flowchart for index](/othello/Stage%204/images/index_flowchart.png)

### Decisions made and Reasoning
The key decision that was made for the development of this function was to delete the game state if the previous game was finished in this function. This was done for as a simple way to implement a 'new game' button. Additionally, it streamlines the logic, as after deleting the game save we are in the same situation as when there was no saved game state to begin with, so there is no need for an additional case. 

## move: app.route("/move")
This function handles when the user makes a move. The AI then makes its move after this, and the mutated board is passed back.

### Returned Information
Regardless of what happens, a status, player, board, message and whether the game is finished or not is returned to the front end. 
- Status: whether the move succeeded or not
- Player: the current player
- Board: the board to be rendered on the GUI
- Message: Where applicable, the message to appear in the message box. This is used to give a reason when an illegal move is rejected. 
- Finished: whether the game has finished or not.

### Logic of the Function
![Flowchart for Move](/othello/Stage%204/images/move_flowchart.png)

### Decisions made and Reasoning
The majority of the logic was transfered and modified from the simple game loop, as the function of both were the same; to implement the functionality of the game.

# ai_opponent.py
This module contains the functionality for the AI opponent that plays the light pieces against the user. It is designed with the intention of giving a slight edge to the user. 
The key function of this module is choose_move, the rest being helper functions for it. 

## chose_move
This is the core of the AI opponent; what move it will choose to make.

### Parameters and Return Type
This function has the parameters of the amount of tokens flipped by the user's previous move, and a dictionary containing each legal move and the amount of tokens they flip. The function returns the coordinates of the move chosen.

### Logic of the Function
![Flowchart for ai_opponent](/othello/Stage%204/images/ai_opponent_flowchart.png)

### Decisions made and Reasoning
There were two main considerations when programming the AI opponent. Randomness, and what metric to use to give the human player an edge. The metric that was chosen was the number of tokens flipped, as this was the simplest to implement while giving the illusion of challenge (the AI should always perform worse than the user). In this implementation randomness was not implemented as it would have introduced a large level of complexity to the AI which would be difficult to trace and implement. 

# Game State Persistance
The persistance of game states is done through the use of JSON. I thought the most logically sound way to implement the means to store a game state in Python and be able to translate it to JSON was to do this through use of a class. 

## GameState Class
![GameState UML diagram](/othello/Stage%204/images/GameState_UML.png)
The functionality required from the GameState class was to be able to be easily translated to JSON, and also to be easily instantiated through JSON. This was provided by the to_dict and from_dict methods. Furthermore, the game state needed to store all the required information for the game to be resumed only from its attributes, which is possible by using the state of the board, the current player, and whether the game is finished or not.

# Testing
Automated testing was implemented through use of unittest. This choice was made to avoid external dependencies while still providing repeatable and structured testing of core game logic. 