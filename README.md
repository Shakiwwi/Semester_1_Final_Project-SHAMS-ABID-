YOU'RE IT! - by Shams Abid — README



1.Concept

YOU'RE IT!   a 2-player tag game where Blue(WASD) and Red(Arrows) move around an obstacle-filled arena. One player starts as "IT" (outlined yellow) and must chase and tag the other player.

The moment a tag happens, the round ends and both players reset to their starting positions, and the other player becomes IT for the next round. IT gets progressively faster the longer a round gets, so speed and positioning are both important.

The match runs for 6 rounds (each player starts as IT 3 times). Scoring is based on comparison: Each round, if the tag happens faster than the previous round, the tagger scores the point, if slower, the other player scores instead. After 6 rounds, higher score wins.

There is also a hidden shortcut near one edge of the map that lets a player briefly slip past the normal screen boundary to get around a wall — a small easter egg for players who explore the edges of the arena.



2. How to Run the Game

Requirements:

Python 3.12+
Pygame 2.6.1 (pip install pygame)

Steps:

Place tag.py, countdown_beep.wav, and go.wav in the same folder.
Open a terminal in that folder and run:
python joy.py
Press SPACE at the title screen to start. After the countdown, Blue starts as IT.



3. Additional Features and Classes Implemented

Features:
Two-player local tag gameplay with WASD / Arrow Key controls
Obstacle course with random cross-shaped walls, cubes, and corner obstacles that block movement
A hidden easter egg allows for a quick escape
IT's movement speed increases the longer a round runs, but resets each round
6-round match structure, alternating which player starts as IT
Comparative round-time scoring system 
Start screen, animated countdown with sound effects, in-game UI (timer, round counter, live score), and a winner screen

Classes:
Player — represents a player character. stores position, color, and control scheme (WASD or Arrow Keys). Handles movement with obstacle/boundary collision, drawing itself, and resetting to its starting position.
Obstacle — represents obstacles in the arena. Stores rectangles and color, and knows how to draw itself. The full set of obstacles (walls, cubes, and crosses of varying sizes) is built as a list.
Scoreboard — tracks scores and the keeps track of every finished round's time. Compares each new round's time against the previous round to decide who scores, and reports final winner.
RoundManager — tracks round number, which player starts each round as IT, who is currently IT, and the round's elapsed time. Handles starting next round (changing the starting IT player) and detecting when the match is over.
Tagging — coordinates a tag by checking whether the two players are currently colliding, and if so, records the round's result on the Scoreboard, resets both players' positions, and tells the RoundManager to start the next round.
SoundControl — loads and plays sound effects.
