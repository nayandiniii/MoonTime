from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import datetime
from calendar import month_name

app = Flask(__name__)
app.secret_key = 'nsn7557'

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'nsn0407'
app.config['MYSQL_DB'] = 'moontime'

mysql = MySQL(app)

# Error handling for 404 Not Found
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# Error handling for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500
'''
def calculate_cycle_data(periods):
    cycle_data = {}
    for period in periods:
        start_date_str = str(period[0])  # Convert to string if not already
        end_date_str = str(period[1])    # Convert to string if not already
        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
            month = start_date.strftime('%B')
            cycle_length = (end_date - start_date).days
            if month in cycle_data:
                cycle_data[month].append(cycle_length)
            else:
                cycle_data[month] = [cycle_length]
        except ValueError:
            print("Error: Unable to parse date string:", start_date_str, "or", end_date_str)
    return cycle_data
'''
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        weight = request.form['weight']
        height = request.form['height']
        
        # Save data to MySQL
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password, age, weight, height) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, email, password, age, weight, height))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        
        if user:
            session['email'] = email
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        symptoms = request.form.getlist('symptoms')
        
        start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        cycle_length = (end_date_obj - start_date_obj).days
        
        month_name = start_date_obj.strftime('%B')
        year = start_date_obj.year
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", [session['email']])
        user_data = cur.fetchone()
        user_id = user_data[0]
        
        # Check if entry already exists for the given month and year
        cur.execute("SELECT * FROM period_data WHERE user_id = %s AND month_name = %s AND year = %s",
                    (user_id, month_name, year))
        existing_entry = cur.fetchone()
        
        if existing_entry:
            # Update existing entry
            cur.execute("UPDATE period_data SET start_date = %s, end_date = %s, symptoms = %s, cycle_length = %s WHERE id = %s",
                        (start_date, end_date, ','.join(symptoms), cycle_length, existing_entry[0]))
        else:
            # Insert new entry
            cur.execute("INSERT INTO period_data (user_id, start_date, end_date, symptoms, cycle_length, month_name, year) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (user_id, start_date, end_date, ','.join(symptoms), cycle_length, month_name, year))
        
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('dashboard'))
    
    return render_template('calendar.html')


# Route for dashboard page
@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))

    email = session['email']
    cur = mysql.connection.cursor()

    # Fetch user data based on email
    cur.execute("SELECT * FROM users WHERE email = %s", [email])
    user_data = cur.fetchone()

    if user_data is None:
        # User with the given email does not exist
        flash('User does not exist', 'error')
        return redirect(url_for('login'))

    # Fetch period data for the user
    user_id = user_data[0]  # Assuming user_id is the first column in the users table
    cur.execute("SELECT month_name, start_date, end_date, symptoms, cycle_length FROM period_data WHERE user_id = %s", [user_id])
    period_data = cur.fetchall()

   # Create a dictionary mapping month names to their indices
    month_indices = {name: idx for idx, name in enumerate(month_name) if name}

# Sort the period_data based on month names
    sorted_period_data = sorted(period_data, key=lambda x: month_indices.get(x[0], float('inf')))

# Extract data for the chart
    months = [data[0] for data in sorted_period_data]  # Extract months from period data
    cycle_lengths = [data[4] for data in sorted_period_data]  # Extract cycle lengths

    # Perform data analysis
    analysis_result = analyze_cycle(cycle_lengths)

    cur.close()

    return render_template('dashboard.html', user_data=user_data, period_data=period_data, months=months, cycle_lengths=cycle_lengths, analysis_result=analysis_result)

def analyze_cycle(cycle_lengths):
    threshold = 1  # Define a threshold for determining similarity
    
    if not cycle_lengths:
        return "No cycle data available"  # Handle case where cycle_lengths is empty
        
    avg_cycle_length = sum(cycle_lengths) / len(cycle_lengths)
    
    if all(abs(length - avg_cycle_length) <= threshold for length in cycle_lengths):
        return "Healthy cycle"
    else:
        return "Irregular cycle, try yoga, exercise, and include foods like pineapple, ginger, and cinnamon in your diet"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
