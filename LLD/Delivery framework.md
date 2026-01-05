
#### Requirements

Identifying the exact requirements are crucial for the task. Asking the right set of questions is key to that. Metal model for that can be around the following:

- Primary capabilities - what the system must do?
- Scope - What is within the scope and what is not? Like (UI, networking, databases not within scope)
- Error handling - How should the system react if some error occurs like wrong input
- Rules of completion - what is the criteria of success for the system 

Example - 
```
Tic Tac Toe 

Requirements:
1. Two players alternate placing X and O on a 3x3 grid.
2. A player wins by completing a row, column, or diagonal.
3. The game ends in a draw if all nine cells are filled with no winner.
4. Invalid moves should be rejected (placing on an occupied cell, acting after the game is over).
5. The system should provide a way to query current game state and reset the game.

Out of Scope:
- UI/rendering layer
- AI opponent or move suggestions
- Networked multiplayer
- Variable board sizes (NxN grids)
- Undo/redo functionality
```

#### Entities and Relationships

Next step is to name the entities, the relationships between them(has-a, contains, Is-a, uses). For Tic Tac Toe, your whiteboard might show:

```
Entities:
- Game
- Board
- Player

Relationships:
- Game -> Board
- Game -> Player (2x)
```

#### Class State and Behaviour

The next step is to define the state and behaviour of entities. Identify what state your entity is going to manage and how your entity going to behave to manage other entities, how the class is going to behave. 

One principle to follow object manage their own state and expose behaviour without needing to call getters to make decisions. 

Tying it all together, by the time you leave this section of the interview you've outlined the state and behavior for all of the classes in your system, like:

```
class Game:
  - board: Board
  - playerX: Player
  - playerO: Player
  - currentPlayer: Player
  - state: GameState (IN_PROGRESS, WON, DRAW)
  - winner: Player? (null if no winner)

  + makeMove(player, row, col) -> bool
  + getCurrentPlayer() -> Player
  + getGameState() -> GameState
  + getWinner() -> Player?
  + getBoard() -> Board
```

#### Design Principles

**KISS - Keep it simple and stupid**
Build the simple solutions. The simplest solution that works is usually the right one. When you're designing a class or choosing between patterns, pick the straightforward approach

**DRY - Don't repeat yourself**
Don't repeat your code , avoid adding same logic in multiple places. Try to create functions, decorators, wrappers and re-use them

**YAGNI - You are not gonna need it**
Build what you need now, keep the scope to extend. Don't build for something you might need in the future. Scope for the future, build whats needed. 

**Separation of Concerns**
Different code blocks, classes should be handle for their responsibilities and shouldn't be mixed. This introduces unnecessary bloatware and make things complex.
For example - In a game of TicTacToe, display , input and logic should be mixed together; each type of action should have their own handler. 

**Law of demeter**
A method should only talk to its immediate member and not all members its immediate member is associated with. This creates a chain and any changes in the implementation of the chains break the code.

`order.getCustomer().getAddress().getZipCode()`, that's violating the Law of Demeter.