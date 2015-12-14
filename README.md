# flag_catching
Final project for EE 106A Fall 2015

# How to Run

## Preparation

1. Set up the hardware according to [this page](http://ee106a-fa15-team01.github.io/flag_catching/#hardware-constructions).
2. Launch the camera, and make sure that all the objects on the playground can be seen in `rviz` and the ARTags on them are recognized.
3. Turn on the Zumys and run `odroid_machine` to connect to them.

## Run Attacker Node

    python zumy_goal.py zumy_name origin_artag boundary_artag flag_artag zumy_artag [defender_artag ...]

For example,

    python zumy_goal.py zumy1c 1 2 3 4 5 6

runs a node that controls the zumy1c with ARTag 4 on it. The origin ARTag is 1, the boundary ARTag is 2 and the flag ARTag is 3.
There are two defending Zumys, the ARTags on them are 5 and 6.

The node will display `Press Enter to do path planning` on the terminal.

## Run Defender Node

    python zumy_catch.py zumy_name origin_artag boundary_artag attacker_artag zumy_artag [other_defender_artag ...]

You can run multiple defender nodes (with different arguments) to control several Zumys.

## Start the Game

Press Enter in every terminal showing `Press Enter to do path planning`, then the Zumys will start moving.

After game is over, the Zumys stop and you can rearrange the playing area. Press Enter in every terminal again to restart the game.

## View Game Status

You can open the image file `out.png` with an image viewer that can automatically reload when the image is changed.
That way you will see the game status in real time.

# Trouble shooting

In case a Zumy does not move:

* If the terminal is showing coordinates `(x, y)` or `rotating (x, y)`, then it might be that the Zumy has lost the connection to the computer.
Restart the Zumy and restart `odroid_machine` for it.
* If the terminal is showing a number `xx`, then check whether the ARTag `xx` can be seen in `rviz`.
