# ED-FSSgame
This documentation will be broken down into 4 primary steps:
1) Download and Installation
2) Running the Code
3) Basic Tutorial
4) Troubleshooting
Please start at Section 1 and proceed from there.
Section 1: Download and Installation
Please download the “project” folder from the repo provided here to an
easily accessible location. Confirm that you have Python downloaded (the version used
in development was 3.11.9). However, 3.12.6 should also work assuming the libraries
are compatible. If you do not have Python downloaded please download it from here.
After successfully downloading, utilize Command Prompt or your Python IDE to pip
install the required libraries: those being tkinter, pillow, opencv-python, and numpy. As
an example, you can copy paste the following into Command Prompt:
`pip install numpy`
Once the required libraries are installed, confirm that you have stored the “project”
folder in a location known to you. After doing this, you should be all set up to go! Please
move onto the next step.
Section 2: Running the Code
There are now 2 options for how to precede and the choice is yours to make.
Option 1:
Utilize your IDE to open the “game.py” file and run it from there. This may be an
easy option; although it might potentially lead to issues with regard to the file path for
images.
Option 2:
Use Command Prompt and navigate to the “game.py” file. This is why it is
important to save the file to a location known to you. Open Command Prompt and use
the cd command to navigate to the “project” folder. Here you can copy paste and then
run the command:
`python game.py`
This should run the project with no issues!
Section 3: Basic Tutorial
At this point the main menu should be open. The program has a very simple set of
controls.

- Select a game mode.
- Choose a number of images.
- Optionally select a difficulty (for the AI race mode).
- Click the play button.

The objective in “score mode” is to place as many squares around the blue signals.
After completing your selected amount of images you will receive statistics and most
importantly your score!
The objective in “AI race mode” is to beat the AI in marking all the signals. In both cases
your score is calculated cumulatively across the number of images.
The controls are as follows:
- Arrow keys for movement
- Spacebar for placing a square
Section 4: Troubleshooting
The most common error is seeing a blank window after pressing play. This is caused by
the image path not being correct. If you chose to use your IDE then you may need to
add additional folders to the path. See below as an example:

This issue can also be resolved by launching via Command Prompt see Section 2
above.
Another issue that may occur is missing libraries. Please confirm that you installed all
the required libraries from Section 1. Additionally, this issue may be caused by the
version of Python you are using to run the program. If you suspect this is an issue,
please install and ensure you select Python 3.11.9 as an interpreter in your IDE.
If there are any other issues, within the code are commented debug statements which
will help with debugging (hopefully this step isn’t needed)! Occasionally there
will be an error thrown upon exiting the program. This can be safely ignored.


Please submit any issues/questions through github for the quickest response
