# To Do List App
This is a basic list app. 

I make a lot of lists in Google docs in order to stay on track with the things I want to get done. Being what it is, it has a lot of limitations.
This project will hopefully solve that problem for me.

## Installation

In your environment, navigate to the extracted files folder, and you can install List_App using pip:

python -m venv venv

\venv\Scripts\activate

pip install -e .

## Usage

After installation, you can run the app from the command line:

list_app

Once everything is running, you can use the text boxes to start adding things to the task list.

Inputs:
-task name
-due date
-tag

All three inputs are strings. The tag will help describe the task you want to accomplish. Every unique tag will have its own list for organizational purposes.

Simply populate the text boxes and add to the list with the 'Add New Task' button. 

For removal, simply check the boxes, you want to remove and click the 'Remove Completed Tasks' button
