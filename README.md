# Moontime

Moontime is a period tracking application designed to help women monitor their menstrual cycles, treat themselves with utmost care and relaxation during menstruation, and track symptoms for better health management.

![Moontime Logo](/static/images/4274784.png)

## Features

- **User Authentication**: Users can sign up for an account and log in securely to access their personalized dashboard.
- **Period Tracking**: Users can log their menstrual periods, including start date, end date, and symptoms.
- **Data Analysis**: The application provides insights into the user's menstrual cycle, including cycle length analysis and health recommendations.
- **Dashboard**: Personalized dashboard to view period data, cycle length trends, and analysis results.

## Technologies Used

- **Flask**: Flask is used as the web application framework to handle HTTP requests and responses.
- **MySQL**: MySQL is used as the database management system to store user data and period tracking information.
- **Flask-MySQLdb**: Flask-MySQLdb is used to integrate MySQL with Flask for database connectivity.
- **HTML/CSS**: HTML and CSS are used for frontend development to create user interfaces and styles.
- **Python**: Python is used as the primary programming language for backend logic and data processing.

## Screenshots

### Home Page
![Home Page](/static/images/home.png)

### Signup Page
![Signup Page](/static/images/signup.png)

### Dashboard
![Dashboard](/static/images/board.png)

### Calendar
![Calendar](/static/images/calendar.png)

## Installation

To run Moontime locally, follow these steps:

1. Clone the repository: `git clone https://github.com/nayandiniii/moontime.git`
2. Navigate to the project directory: `cd moontime`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up MySQL database: Create a MySQL database named `moontime` and configure the database connection in `app.py`
5. Run the application: `python app.py`

