from flask import Flask, render_template,request,url_for,session,redirect
from flask_sqlalchemy import SQLAlchemy

import MySQLdb.cursors

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root@localhost/codesangam' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'asdfghjkl'
db=SQLAlchemy(app)
class Users(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String,nullable=False)
    password=db.Column(db.String,nullable=False)
    email=db.Column(db.String,nullable=False)

msg=''
@app.route('/')
def home():
    if 'loggedin' in session:
        user_id = session['userid']
        user_name = session['name']
        user_email = session['email']

     # You can use these parameters in your logic or pass them to a template
        return render_template('index.html', user_id=user_id, user_name=user_name, user_email=user_email)
    else:
        return render_template('index.html')
        
@app.route('/guestmode')
def guestmode():
    return render_template('guestmode.html')
@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
       user_id = session['userid']
       user_name = session['name']
       user_email = session['email']

        # You can use these parameters in your logic or pass them to a template
       return render_template('dashboard.html', user_id=user_id, user_name=user_name, user_email=user_email)
    else:
        return render_template('index.html',msg='Please Login First')    
@app.route('/register',methods=['GET','POST'])
def credentials():
    if(request.method=='POST'):
        username=request.form.get('username')
        password=request.form.get('password')
        email=request.form.get('email') 
        # This code until here was to fetch the entries for the database
        # Then we will add the data to the database
        entry=Users(username=username,password=password,email=email)
        db.session.add(entry)
        db.session.commit()
        regist="Registered Successfully"
        return render_template('index.html',regist=regist)  # Redirect to the dashboard after successful registration


        # the entry is now added to the database
        # return redirect(url_for('/dashboard'))
    # Adjust the template name accordingly
    return render_template('register.html')     
@app.route('/login', methods =['GET', 'POST'])
def login():
    message = 'Login unsuccesfull'
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        
        # Using SQLAlchemy to query the database
        user = Users.query.filter_by(email=email, password=password).first()
        
        if user:
            session['loggedin'] = True
            session['userid'] = user.sno
            session['name'] = user.username
            session['email'] = user.email
            message = 'Logged in successfully!'
            return render_template('dashboard.html', message=message)
        else:
            message = 'Please enter correct email / password!'
    
    return render_template('index.html', message=message)
@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return render_template('index.html', message='Logged out successfully')
    
@app.route('/homelogin')
def homelogin():
    if 'loggedin' in session:
        user_id = session['userid']
        user_name = session['name']
        user_email = session['email']

        # You can use these parameters in your logic or pass them to a template
        return render_template('homelogin.html', user_id=user_id, user_name=user_name, user_email=user_email)
    else:
        return render_template('index.html')
@app.route('/about')
def about():
    return render_template('About.html')
if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run(debug=False,host='0.0.0.0')
