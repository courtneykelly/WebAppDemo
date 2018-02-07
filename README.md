# WebAppDemo

Lean In meeting web application demo.

I've modeled this tutorial from the following link: [Creating a Web App with Python, Flask, and MySQL](https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972). Please visit for more details.

## Step 1: Setting Up Flask

Install flash using the `pip` package manager.
```bash
pip install flask
```

Create a file called `app.py` and import that the `flask` module and create a Flask app. Create a home route `/` and a corresponding route handler. Finally at the bottom of the program, check is the executed file `__name__` is the main program `__main__`, then run the flask app. File should display as follows:
```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def main():
    return "Welcome!"

if __name__ == "__main__":
    app.run()
```

Save and execute the `app.py` file:
```bash
python app.py
```

Go to your browser and navigate to [http://localhost:5000/](http://localhost:5000/) and you should see the welcome message.

## Step 2: Setting Up the Home Page

I've already set up the html files per the structure we discussed in part 1 in the `/templates` directory. The home `/` route usually corresponds to `index.html` file. We now need to import `render_template` from the flask module, which we'll use to render all template files. So instead of returning `"Welcome!"` for our `/` request handler, we can return the rendered `index.html` template.

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
```

Save and rerun [http://localhost:5000/](http://localhost:5000/). You should see the following:

![home page](home.png)

## Step 3: Setting Up the Sign Up page

Similar to the home page we want to create sign up page linked to the 'Sign Up' button on the home page. We create a `/showSignUp` route and corresponding request handler that returns the rendered `signup.html` file from `/templates`. We accomplish this through the `href="showSignUp"` in the corresponding `button` html element. This has been done for you. So our `app.py` file should now look like:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

if __name__ == "__main__":
    app.run()
```

Save and rerun [http://localhost:5000/](http://localhost:5000/). You should see the following:

![sign up page](signup.png)

## Step 4: Setting Up the MySQL Database

We'll be using `MySQL` for the back end. So log into MySQL from the command line, or if you prefer a GUI like MySQL work bench that's fine too. Please download and install `mysql`. If you have [HomeBrew](https://brew.sh/) package manager for macOS it's easy:
```bash
brew install mysql
```

After installation, we'll need to create a MySQL database and user as follows: 
1. At the command line, log in to MySQL as the root user:
```bash
mysql -u root -p
```
Type the MySQL root password, and then press Enter. If you do not need a password then simple do:
```bash
mysql -u root
```


2. To create a database user, type the following command. Replace `username` with the user you want to create, and replace `password` with the user's password:
```bash
GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost' IDENTIFIED BY 'password';
```
We will need this username and password for later in `app.py`.


3. Type `\q` to exit the mysql program.


4. To log in to MySQL as the user you just created, type the following command. Replace username with the name of the user you created in step 3:
```bash
mysql -u username -p
```
Type the user's password, and then press Enter.


5. Now let's create the database:
```SQL
CREATE DATABASE LeanIn;
```


6. To work with the new database, type the following command:
```sql
USE dbname;
```


7. Now let's create a table for our users:
```sql
CREATE TABLE users 
	(	user_id bigint not null auto_increment,
		user_name varchar(45),
		user_username varchar(45),
		user_password varvhar(45),
		primary key (user_id) );
```


8. Now let's see if we created the table:
```sql
show tables;
```


9. Now let's verify the attributes of the user table are correct:
```sql 
desc users
```

Great, now our database is in business.

## Step 5: Implement the Sign Up Method

Next, we need a server-side method for the UI to interact with the MySQL database. So edit `app.py` and create a new method called `signUp` and also add a route `/signUp`. We'll be using [jQuery AJAX](http://api.jquery.com/jquery.ajax/) to post our signup data to the signUp method, so we'll specify the method in the route definition. In this method we're going to need to read the values from the the post request, so import `request` from flask. We're also going to return `json` data, so import that as well:
```python 
from flask import Flask, render_template, json, request
```
Now we're going to implement the method: read the posted values with `request`, verify that the inputs are valid, and return a `json` packet with a simple message indicating success or failure. The route and method should look as follows:
```python
@app.route('/signUp',methods=['POST'])
def signUp():
 
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
 
    # validate the received values
    if _name and _email and _password:
        return json.dumps({'message':'All fields good!!'})
    else:
        return json.dumps({'error':'Enter the required fields'})
```

## Step 6: Create a Sign Up request 

We'll be using [jQuery](http://jquery.com/) AJAX to send the signup request to the Python method. [Download](http://jquery.com/download/) and place jQuery inside `/static/js` and add a link to it from the signup page. Once jQuery has been included, we'll add a jQuery POST request when the user clicks the Sign Up button.

So, let's attach the signup button click event as shown:

```js
$(function() {
    $('#btnSignUp').click(function() {
 
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
```

This has all been done for you and is located in the `/static/js/signup.js` file. Save all the changes and restart the server. From the Sign Up page, fill in the details and click Sign Up. Check the browser console and you should have the below message:
```json
{"message": "All fields good !!"}
```

## Step 7: Connecting the Sign Up request to the MySQL Database

Now that we have the request methodology set up we can go ahead and connect to the database and log our new data. To connect flask to MySQL, we'll be using [Flask-MySQL](https://flask-mysql.readthedocs.io/en/latest/#) extension of flask. Install as follows:
```bash
pip install flask-mysql
```
and go ahead and add the following import line to your `app.py` file:
```python 
from flask.ext.mysql import MySQL
```

Now we need to add the MySQL configurations we created in step 4:
```python
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'username'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'LeanIn'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
```

In our `signUp()` method after we've validated the received values, we're going to want to enter them into the SQL database. We can go ahead and delete:  and connect to the database, insert our new values, check for errors, and finally, disconnect from the database as follows:
```python
# validate the received values
if _name and _email and _password:
    
    # Connect to Database
    conn = mysql.connect()
    cursor = conn.cursor()

    # Format SQL
    sql = 'INSERT INTO users (user_name, user_username, user_password) VALUES ("{}", "{}", "{}")'.format(_name,_email,_password)
    
    # Execute SQL
    cursor.execute(sql)
    data = cursor.fetchall()

    # log success or failure to the console
    if len(data) is 0:
        conn.commit()
        return json.dumps({'message':'User created successfully !'})
    else:
        return json.dumps({'error':str(data[0])})

    # disconnect from database
    cursor.close() 
    conn.close()
```

Save the changes and restart the server. Go to the signup page and enter the name, email address and password and click the Sign Up button. On successful user creation, you'll be able to see a message in your browser console.

```json
{"message": "User created successfully !"}
```

## Finishing Up

In conclusion, your final `app.py` file should look like:

```python
from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'username'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'LeanIn'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
     return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
    try:
        if request.method == 'POST':
            _name = request.form['inputName']
            _email = request.form['inputEmail']
            _password = request.form['inputPassword']

            # validate the received values
            if _name and _email and _password:
                
                # Connect to Database
                conn = mysql.connect()
                cursor = conn.cursor()

                # Format SQL
                sql = 'INSERT INTO users (user_name, user_username, user_password) VALUES ("{}", "{}", "{}")'.format(_name,_email,_password)
                
                # Execute SQL
                cursor.execute(sql)
                data = cursor.fetchall()

                # log success or failure to the console
                if len(data) is 0:
                    conn.commit()
                    return json.dumps({'message':'User created successfully !'})
                else:
                    return json.dumps({'error':str(data[0])})

                # disconnect from database
                cursor.close() 
                conn.close()

            else:
                return json.dumps({'html':'Enter the required fields'})

    except Exception as e:
        return json.dumps({'error':str(e)})
        

if __name__ == "__main__":
    app.run(port=5002)

```