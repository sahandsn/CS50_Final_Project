# CS50_Final_Project: YourList

This is my final project for Harvard’s CS50 introduction to computers and the art of programming. 
It is a flask web application in which you can save notes and customize your account.


Please check out my project, which is hosted on pythonanywhere.com: http://yourlistsandnotesapp.pythonanywhere.com/


With this web application you can:

1. Create a note with a heading and body and the time stamp is automatically generated from the new entry section. 
from here you can choose if your note is urgent or not. 
2. Choose a tag (urgent, entry, done) so that notes are grouped in these distinct groups. Each tag's heading has an indicating color. urgent notes are red, entries are blue, and done has a gray heading. On the main page, notes are grouped together based on their tag. urgent is the first, followed by entry, and then done. In each group, notes are ordered based on their time stamp. The newer they are, the higher they stand. 
3. Change a note's tag from the main page. From here, under the more section, you can choose between the three tags. Notice that by selecting a new tag, the color around the heading changes.
4. Delete a note from the more section of the main page. Notice that you are prompted to enter the password.
5. Receiving an email after registration, creating and deleting notes. 
6. Change the email address from the account section. you have to enter both the existing and the new email addresses. After that, you are prompted to enter your password.
7. Delete your account from the account section. Notice that you are prompted to enter the password.
8. Customize the font, size, and color combination of the background/foreground. This is perhaps the highlight feature of this application. You can change one, two, or all three elements. Once saved, you can safely log out of your account and log back in to see that your customization is in place. 
9. Error. There are many instances that the user may mistakenly or intentionally try to disobey the instructions. From confirming the password to customizing the app, all of the data is processed in the backend as well. If the incoming command or information is not expected the error function notifies the user about the violation and the action is not processed.
10. Register yourself. In this section, you have to choose a unique username and email address that had not been used before in this app. Your password and confirmation should match as well. Failing any one of these criteria prevents a new user from registering. After successful registration, the user is redirected to the main page.


The static directory contains icon.png which is used in the upper section of each page, favicon.ico which is displayed in the tab, CSS directory contains style.css, which contains the CSS codes. 
The templates directory contains the many HTML files used for routing the flask application.
App.py is the main file that contains the python code, which is primarily the routing.
Tables.db is the sqlite3 database that has three tables. users table which stores user id, password hash, and email. notes table which stores user id, head, body, time stamp, and tag. custumize table which contains user id, font, size, background, and foreground used in the CSS file.


# YouTube Video

CS50's instructions include uploading a short video demonstrating our final project.
Here is my video explaining the application: https://youtu.be/Is6WlKeyE4o


# About CS50

Introduction to the intellectual enterprises of computer science and the art of programming. This course teaches students how to think algorithmically and solve problems efficiently. Topics include abstraction, algorithms, data structures, encapsulation, resource management, security, software engineering, and web programming. Languages include C, Python, and SQL plus HTML, CSS, and JavaScript. Problem sets inspired by the arts, humanities, social sciences, and sciences. Course culminates in a final project. Designed for concentrators and non-concentrators alike, with or without prior programming experience. Two thirds of CS50 students have never taken CS before. Among the overarching goals of this course are to inspire students to explore unfamiliar waters, without fear of failure, create an intensive, shared experience, accessible to all students, and build community among students.

From https://cs50.harvard.edu/x/2022/