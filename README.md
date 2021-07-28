# Brick Breaker

To run the game - open a terminal and run "python main.py" command. (use python3 instead of python in linux).

In this game, the user needs to destroy all the breakable bricks with the help of ball and paddle.
The user would be given 3 lives. A life is lost when ball touches the bottom wall.
There are 4 types of bricks - 3 Breakable and the last one is unbreakable.

Breakable bricks - Number of hit required to break, points gained by destroying it
1. Green color - 1, 10
2. Blue color - 2, 30
3. Red color - 3, 50

Unbreakable bricks can be broken only when you have the power up - through ball(100 points if destroyed)

Power ups - 
There are 6 types of power ups which can be gained by catching them with the paddle. They appear randomly when a brick is broken.
Power up lasts for 8 seconds

1. Exapnd paddle - 
	symbol - yellow "="
	effect - increases length of paddle by 2 units
2. Shrink Paddle - 
	symbol - red "="
	effect - decreases length of paddle by 2 units
3. Ball multiplier - 
	symbol - yellow "O"
	effect - for every existing ball, it creates a new ball
4. Fast Ball -
	symbol - red "O"
	effect - increases the velocity of the ball in vertical direction.
5. Through Ball
	symbol - green "O"
	effect - destroys everything in its way(except the walls)
6. Grab Paddle
	symbol - green "="
	effect - catch the ball and release it whenever you want.
 
Controls - 
keys 'a' and 'd' for moving the paddle left and right respectively
space bar - for releasing the ball caught on paddle

Additional Instructions for Assignment 3 - 
Levels - There are 3 levels - 2 normal and 1 boss level
When you destroy all the breakable bricks, the level ends.
Skipping level - press 'l'

Falling Bricks - In each level after certain time, when ball touches the paddle, all the bricks starts coming down by 1 row.
When the lowest brick is on the level of paddle then game ends.

Power up 2.0 - Now the powerups dont fall vertically but they are projected with velocity of the ball which destroyed the respective brick. Gravity effect observed in every 3 frames.

Rainbow Bricks - These bricks have different colors in different frames until the ball makes first contact with it. When ball hits this wall, it gets a certain color (depending on when the ball hit) and it becomes a destroyable brick.

Shooting paddle - Yellow color ("^") indicates this power up. On taking this, paddle structure changes from 
"=======" to"|=====|" where "|" indicates cannon. Red colored "^" indicates lasers which will be released from the cannons.

Boss enemy - "(((=)))" is the UFO.
It has a health of 10. When its health reaches below 7, when ball touches the paddle, bricks will spawn(1st spawn) and simimiliarly second spawn is when its health falls below 4.
