# Classmanager
Classmanager is a dynamic web application which allows **users** to manage a course effectively as an **instructor** or attend multiple classes as a **student**.
It is built using the Django framework and the Python language for the server side and HTML, CSS, JavaScript and Bootstrap for the client side.
This project is currently deployed to heroku and can be viewed [Here](https://coursemanager-project.herokuapp.com/)

## Operations
### Unauthenticated users
 - An unauthenticated user can only view the home page, and login/registration pages
 - On the registration page, the user can create a **user** account and get logged in
 - On the login page, the user can enter their username and password and get logged in if the combination is valid
 - If the user doesn't remember their combination, their password could be changed only if they remember the email and username used to create the account
### Users
 - Users can register for either a student or an instructor role depending on their needs and their accounts would be updated accordingly (Note that roles are final and cannot be change after initial assignment)
 - Users can click on their username in the navbar to view information about their profile
 - Lastly all users can change their first or last name if they are authenticated
### Instructors
 - Create a new course
 - View the course dashboard of each course which they created
 - Create announcements in their courses that all enrolled students can see
 - View all announcements in theie courses
 - Create assignments in their courses which all enrolled students see and submit
 -  View assignments and grade all submissions for each
 - Create attendances for enrolled students in a course weekly, and view them in chronological order
 - Final Grade enrolled students and view final grades for the course
 - Deactivate and/or Delete created courses
### Students
 - Join existing active courses
 - View course dashboard for each course which they joined
 - View assignments in a course and create submissions for them
 - View all submissions for assignments in a course, and corresponding grades
 - Leave a course which they are enrolled in
 - View final grade for each enrolled course when they become available
## Setup
 - Install the packages in requirements.txt using `pip install -r requirements.txt`
 - Create a file called `secret_settings.py` in the `./coursemanager/coursemanager/` directory and paste the text `SECRET_KEY = ''` inside it
 - Open a python shell (IDLE) and execute the following:
 `from django.core.management.utils import get_random_secret_key`
 `print(get_random_secret_key())`
 - Copy the output and paste between the `''` on the first line of `secret_settings.py` and save the file
 - If you want a fresh database, delete `db.sqlite3`
 - move to the `./coursemanager/` directory and run the commands:
	`python manage.py makemigrations classmanager`, `python manage.py migrate`, and `python manage.py runserver`
- If all goes well, your web server should be up and running on localhost
- To access the application, you open your browser and navigate to `localhost:8000`
(If you experience any errors, you could open an issue in the issues tab of this github repository)
Lastly, Thank You for viewing my project!
## Screenshots
![Application Home Page](https://i.imgur.com/8UxVaa2.png)
Application Home Page
![User Registration Page](https://i.imgur.com/hDCaG5u.png)
User Registration Page
![Student Role Registration Page](https://i.imgur.com/QUzdbM7.png)
Student Role Registration Page
![Student and Instructor view side by side](https://i.imgur.com/KZWZX4E.png)
Student and Instructor view side by side
![Student and Instructor view of Course dashboard side by side](https://i.imgur.com/8XJdlB3.png)
Student and Instructor view of Course dashboard side by side
## Testing
This project is 57% tested, this includes all models, forms and a few views. More tests would be added later on
 - To run tests, you must first complete setting up the application
 - Navigate to the `./coursemanager/` directory and run `python manage.py test classmanager.tests` to run all tests
 - To test specific things such as forms or models, you run `python manage.py test classmanager.tests.test_forms` or `python manage.py test classmanager.tests.test_models`
 - All test groups are contained in their respective files the `./coursemanager/classmanager/tests` directory
 - To view how much of the project is tested, you `coverage manage.py test classmanager.tests` followed by `coverage html`
 - Then you navigate to the `./coursemanager/htmlcov` directory and open up index.html to view it.
