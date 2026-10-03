# import the Flask class
from flask import Flask, render_template, request, redirect, url_for, session
# import the mysql connector
import mysql.connector as mysql
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
from cryptography.fernet import Fernet

# create the object for flask class with __name__
app = Flask(__name__)

# create the secret key when we use the session we need this
app.secret_key="mykey"

# create the connection
con = mysql.connect(
    host="localhost",
    user="root",
    password="1234",
    database = "flask_fp7_2026"
)

# create the cursor
cur = con.cursor()

# home template view
@app.route("/")
def home():
    return render_template("home.html")

# about template view
@app.route("/about")
def about():
    return render_template("about.html")

# signup template view
@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method=='POST':
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        password=request.form['password']
        #using generat_password_hash()
        # password = generate_password_hash(password)
        # using bcrypt
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        mobileno = request.form['mobileno']
        location = request.form['location']
        zipcode = request.form['zipcode']
        query = """ 
        insert into employee (firstname, lastname, email, password, mobileno, location, zipcode)
        values(%s,%s,%s,%s,%s,%s,%s)
        """
        values = (firstname, lastname, email, password, mobileno, location, zipcode)
        cur.execute(query, values)
        con.commit()
        return redirect(url_for('login'))
    return render_template("signup.html")

# login template view
@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password =request.form['password']
        query = """
        SELECT * FROM employee
        WHERE email = %s AND password = %s
        """
        values= (email, password)
        cur.execute(query, values)
        result = cur.fetchone()
        if result:
            session['user']=result[3]
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login'))
    return render_template("login.html")

# data template view
@app.route("/data", methods = ['GET', 'POST'])
def data():
    if "user" in session:
        cur.execute("select * from employee")
        result = cur.fetchall()
        return render_template("data.html",result=result)
    else:
        return redirect(url_for('login'))

# dashboard template view
@app.route("/dashboard", methods = ['GET', 'POST'])
def dashboard():
    return render_template("dashboard.html")



# update the data
@app.route("/update/<int:id>",methods = ['GET', 'POST'])
def update(id):
    if request.method=='POST':
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        password=request.form['password']
        mobileno = request.form['mobileno']
        location = request.form['location']
        zipcode = request.form['zipcode']
        query = """ 
        update employee set firstname=%s, lastname=%s, email=%s, password=%s, mobileno=%s, location=%s, zipcode=%s where id=%s"""
    
        values = (firstname, lastname, email, password, mobileno, location, zipcode, id)
        cur.execute(query, values)
        con.commit()
        return redirect(url_for('data'))

    query = """ select * from employee where id=%s"""
    values = (id,)
    cur.execute(query, values)
    result = cur.fetchone()
    return render_template('update.html', result = result)






# delete the data
@app.route("/delete/<int:id>")
def delete(id):
    query = """ delete from employee where id=%s"""
    values = (id,)
    cur.execute(query, values)
    con.commit()
    return redirect(url_for('data'))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

# hasing using werkzeug.security
@app.route("/hashing")
def hashing():
    data="1234567"
    # conver the data into hash form
    result = generate_password_hash(data)
    # validate the given data with hashed data are same or not
    # using check_password_hash(12345, result)
    return f'{check_password_hash(result, "1234567")}'

#hasing using bcrypt
@app.route("/hashing2")
def hashing2():
    data="123456"
    data=data.encode()
    #convert the data into hasing form using generate_password_hash()
    result=bcrypt.hashpw(data,bcrypt.gensalt())
    # return result
    #validate the given data with hashed are same or not using check_password_hash()
    return f'{bcrypt.checkpw("123456".encode(), result)}'


#hasing using bcrypt
@app.route("/hashing3")
def hashing3():
    data="123456"
    data=data.encode()
    # genertate the key
    key = Fernet.generate_key()
    # create the object to the Fernet class
    cipher = Fernet(key)
    # # perform the encryption
    result= cipher.encrypt(data)
    # return result

    # perform the decryption
    result= cipher.decrypt(result)
    return result


















# Run the server
if __name__ == "__main__":
    app.run(debug=True)

"""
debug=True
When we make changes, Flask automatically restarts
the server.
"""