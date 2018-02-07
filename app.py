from flask import Flask, render_template, request, json
from flask.ext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySQL Configurations
app.config['MYSQL_DATABASE_USER'] = 'circle_leader'
app.config['MYSQL_DATABASE_PASSWORD'] = 'leaninrocks'
app.config['MYSQL_DATABASE_DB'] = 'leanin'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/showSignUp")
def showSignUP():
	return render_template('signup.html')

@app.route("/signUp", methods=['POST'])
def signUp():

	# read posted values from UI
	_name = request.form['inputName']
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']

	# validate requested values
	if _name and _email and _password:
		
		# connect to the Database
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
			return json.dumps({'message': 'user created successfully'})
		else:
			return json.dumps({'error': str(data[0])})

		# disconnect from the database
		cursor.close()
		conn.close()

	else:
		return json.dumps({'error': 'enter required fields'})

if __name__ == "__main__":
	app.run()