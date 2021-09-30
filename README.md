# BLACKJACK PLAYING AGENT WITH MACHINE LEARNING

Blackjack or twenty-one is a card game that gives the player a chance to have an advantage over the dealer. The objective of the game is having a higher total of card values than the dealer’s, while also having the total to be smaller or equal to the value 21. The player can use a “basic strategy” to even the odds with the dealer. When the player also takes the distribution of cards played in the prior hands into consideration, the player can have an advantage. In this project, a simulation for the blackjack, and players for the blackjack are implemented. The machine learning agent for playing the game is implemented, tested, and results are compared. The results indicated that machine learning player can successfully replace the players utilizing the counting system.

This git repository contains the engineering project report and the source code for the simulation and the machine learning player.

Files on the archive:

/ : This directory contains the source code for the blackjack simulator, an installation guide for additional libraries and the engineering project report.

/MachineLearningPlayer : This directory contains the source code and the model for the machine learning player.


Software Requirements:

    Operating System: Ubuntu GNU/Linux based operating systems
    Additional Libraries: python3, python3-pip, numpy, matplotlib, scikit-learn, scipy, pandas, pillow, seaborn, h5py, tensorflow, keras (installation guide for these libraries is included in /python3_pip_install_guide)

Hardware Reqirements:

    A x86 architecture CPU
    4 GB of RAM
    20-30 GB free space for libraries and the simulator output


The blackjack simulator is run with the following command:

    $ python3 BlackjackSimulatorMain.py

After the simulation runs are complete, if the player to be logged by the simulator (Hi-Lo in this case) is playing the game, a count_list_for_ml.csv is written to the disk.

The machine learning player is trained by running:

    $ python3 TrainML.py

in the MachineLearningPlayer directory to produce machinelearningplayer.h5 file.

Then the simulation can be run again to test the machine learning player with the command:

    $ python3 BlackjackSimulatorMain.py

Note: Additional settings can be changed in the Settings.py file.


