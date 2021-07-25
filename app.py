from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)







class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    company_name = db.Column(db.String(50))
    items_donated = db.Column(db.Integer)

    def __repr__(self):
        return f"Username: {self.username} Password: {self.password}"

class FoodBank(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    items_needed = db.Column(db.String(500))
    street_adress = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.Integer)

    def __repr__(self):
        return f"Name: {self.name} Password: {self.items_needed}"
    

current_user = User()

@app.route("/")
def home():
    global current_user
    print(current_user)
    print("The above is coming from the index page")
    
    return render_template('index.html', user = current_user.first_name)



@app.route("/login", methods = ['GET', 'POST'])
def login():
    global current_user
    if request.method == 'POST':
        account_username = request.form['username_log']
        account_password = request.form['password_log']
        
        user = User.query.filter_by(username = account_username).first()
        if user:
            if account_password == user.password:
                current_user = user
                print(current_user)
                return redirect('/')
            else:
                return "error"
        else:
            return "user doesn't exist"


    
    return render_template('login.html')



@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        f_name = request.form['first_name']
        l_name = request.form['last_name']
        comp = request.form['comp_name']
        account_username = request.form['username']
        account_password = request.form['password']
        new_account = User(first_name = f_name, last_name = l_name, company_name = comp, 
        username = account_username, password = account_password)

        try:
            db.session.add(new_account)
            db.session.commit()
            current_user = new_account
            return redirect('/')
        except:
            return 'There was an issue adding your account to the database'
    else:
        return render_template('signup.html')



@app.route('/accounts')
def view_accounts():
    accounts = User.query.order_by(User.id).all()
    return render_template('accounts.html', accounts = accounts)



if __name__ == "__main__":
    app.run(debug=True)