from flask import Flask,render_template,request
import hashlib
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cyber"    
    )

@app.route('/')
@app.route('/register',methods=['POST','GET'])
def register():
    msg = ""
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'email' in request.form and 'username' in request.form and 'password' in request.form and 'rpassword' in request.form and 'gender' in request.form:
        login = request.form
        fname=login['fname']
        lname=login['lname']
        email = login['email']
        username=login['username']
        password=login['password']
        rpassword=login['rpassword']
        gender=login['gender'];
        cursor = mydb.cursor()

        if password!=rpassword:
            msg = "Password does not match"
        else:
            salt = 'c#2}'
            saltedpass = password+salt
            encodepass = hashlib.md5(saltedpass.encode()).hexdigest()
            cursor.execute("insert into registration(fname,lname,email,username,password,gender) values(%s,%s,%s,%s,%s,%s)",(fname,lname,email,username,encodepass,gender))
            mydb.commit()
            msg = "Registered Succesfully"
    return render_template('register.html',msg=msg)

@app.route('/login',methods=['POST','GET'])
def login():
    msg= ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        login = request.form
        username=login['username']
        password=login['password']
        cursor = mydb.cursor()
        salt = 'c#2}'
        saltedpass = password+salt
        encodepass = hashlib.md5(saltedpass.encode()).hexdigest()

        cursor.execute("select * from registration where username=%s and password=%s",(username,encodepass))
        account = cursor.fetchone()

        if account:
            msg = "Sucessfully logged in!"
            return render_template('login.html',msg=msg)
        else:
            msg = 'Incorrect username/password'
    return render_template('login.html',msg=msg)

if __name__=="__main__":
    app.run(debug=True)
