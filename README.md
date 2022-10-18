## Cinema Booking Application

A desktop application for the booking of cinema tickets.

# Requirements

1. [Python](https://www.python.org/downloads/) 3.10.7
2. [tkinter](https://docs.python.org/3/library/tkinter.html) v0.1.0
3. [Pillow](https://pypi.org/project/Pillow/) v9.2.0

# Installation

After cloning this repository and installing the correct version of python, you will need to create a virtual environment. The full documentation on python venvs is located [here](https://docs.python.org/3/library/venv.html). To create a virtual environment first cd into the root folder of this repo, then run this command `python3 -m venv venv` making sure that you are replacing `python3` with the correct executeable if you have multiple installed. To now enter the virtual environment you will run either `source venv/bin/activate` on unix bash shells or `venv\Scripts\activate.bat` on windows using cmd. Whenever you come back to the project you will need to re-enter the virtual environment, or else you will not be able to access python packages you have installed inside it.

Now you can install all the requirements by running `pip install -r requirements.txt`. If the requirements change at any point, you will need to re-run this command to update what you have installed.

To run the application, run `python run.py`.
