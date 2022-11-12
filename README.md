# CS50_Final_Project: YourList

This is my final project for Harvard’s CS50 introduction to computer and the art of programming. 
It is a flaks web application in which you can save notes and customize your account.

Whith this web application you can:

1. Create a note with heading and body and the time is stamp is automatically generated from the new entry section. 
from here you can choose if your note is urgent or not. 
2. Choose a tag from (urgent, entry, done) so that notes are grouped in these distinct groups. Each tag's heading has an idicating color. urgent notes are red, entries are blue, and done has gray heading. In the main page, notes are grouped together based on their tag. urgent is the first, followed bt entry and then done. In each group notes are ordered based on their time stamp. The newer they are, the higher they stand. 
3. Change a note's tag from the main page. From here, under the more section, you can choose between the three tag. Notice that by selecting a new tag, the color around the heading changes.
4. Delete a note from the more section of the main page. Notice that you are prompted to enter password.
5. Receiving an email after registration, creating and deleting notes. 
6. Change email address from the account section. you have to enter both the exsiting and the new email addresses. After that you are prompted to enter your password.
7. Delete your account from the account section. Notice that you are prompted to enter password.

The static directory contains icon.png which is used in the upper section of each page, favicon.ico which is displayed in the tab, css directory that contains style.css, containing the css codes. 
The templates directory constains the many html files that are used for routung the flask application.
App.py is the main file that contains the python code, which is primaraly the routing.
Tables.db is the sqlite3 database that has three tables. users which stores user id, password hash, email. notes which stores user id, head, body, time stamp and tag. custumize which contains user id, font, size, background and foreground used in the css file.

Please check out my project, whic is hosted on pythonanywhere.com: http://yourlistsandnotesapp.pythonanywhere.com/

Here is a short video explaning my application: https://youtu.be/Is6WlKeyE4o