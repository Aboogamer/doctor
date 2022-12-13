from flask import Flask, request, redirect, render_template, send_file


app = Flask(__name__)

# A dictionary to store user information
users = {}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the email from the form
        email = request.form['email']

        # Check if the email is registered
        if email in users:
            # Redirect the user to the /show-info page
            return redirect('/show-info?email={}'.format(email))
        else:
            # Redirect the user to the /register page
            return redirect('/register')
    else:
        # Render the home page template
        return render_template('home.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Get a list of all registered users
    user_emails = users.keys()

    # Render the admin page template, passing the list of user emails to it
    return render_template('admin.html', user_emails=user_emails)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the user's information from the form
        email = request.form['email']
        name = request.form['name']
        birthday = request.form['birthday']
        age = request.form['age']
        date = request.form['date']
        reason = request.form['reason']


        # Store the user's information in the users dictionary
        users[email] = {
            'name': name,
            'birthday': birthday,
            'age': age,
            'date of visit': date,
            'reason': reason,
            'medical note': None

        }

        # Redirect the user to the /show-info page
        print(users)
        return redirect('/show-info?email={}'.format(email))

    else:
        # Render the register page template
        return render_template('register.html')

@app.route('/view_file/<file_name>')
def view_file(file_name):
    try:
        return send_file(file_name, attachment_filename=file_name)
    except Exception as e:
        return str(e)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the file from the request
    file = request.files['file']

    # Check if the file is present
    if file.filename == '':
        return 'No file selected'

    # Save the file to the current directory
    file.save(file.filename)
    return render_template('file.html')


@app.route('/show-info', methods=['GET', 'POST'])
def show_info():

    email = request.args.get('email')

    if request.method == 'POST':


        # Get the updated user information from the form
        name = request.form['name']
        birthday = request.form['birthday']
        age = request.form['age']
        date2 = request.form['date']
        reason2 = request.form['reason']
        file = request.files['file']
        file.save(file.filename)
        # Update the user's information in the users dictionary
        users[email] = {
            'name': name,
            'birthday': birthday,
            'age': age,
            'date of visit': date2,
            'reason': reason2,

        }

    if email in users:
         # Get the user's information from the users dictionary
        user = users[email]

        # Render the show-info page template and pass the user's information to it
        return render_template('show-info.html', user=user)

    # If the email does not exist, render an error page
    else:
        return render_template('error.html')


if __name__ == '__main__':
    app.run()




