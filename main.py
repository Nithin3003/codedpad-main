from flask_pymongo import PyMongo
from flask import Flask,redirect,url_for,render_template,request,session,send_from_directory
import smtplib
# from werkzeug.security import generate_password_hash, check_password_hash
import csv 
from secrets import token_urlsafe
from pytz import timezone 
from datetime import datetime
import os
app= Flask(__name__) 

# offical hosted 1

os.environ["url"] = "mongodb+srv://msnithin84:Nithin@cluster0.wob2cfi.mongodb.net/coded"

app.config['MONGO_URI'] = os.environ.get('url')
app.config['SECRET_KEY'] = token_urlsafe(32)

mongo = PyMongo(app)
coded = mongo.db.codedpad



def curr_date():
    date = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    return str(date)[:-10] if date else ""


def fb(mydict):
    try:
        form_mail ='hack@gmail.com'
        my_mail = '30nithinms@gmail.com'
        password = 'mvjp jpbl dnvu xmlc'
        connection = smtplib.SMTP("smtp.gmail.com",587)
        connection.starttls()
        connection.login(my_mail,password)
        connection.sendmail( form_mail , to_addrs="30nithinms@gmail.com", msg=f'Subject:Feedback\n\n \tName : {mydict[ "name"]} \n \tEmailid : {mydict["email"]}\n\t Feedback :{mydict["feedback"]} \n\n\t  Thank You..\n\t {curr_date()}')
        connection.sendmail(form_mail , to_addrs=f"{mydict['email']}", msg=f'Subject:Codedpad\n\nMr/Ms {mydict[ "name"]}, thank you for your feedback on codedpad... from Nithin M S\n\t {curr_date()}')
        
        connection.close()
        return True,f"Thank You {mydict['name']}"
    except Exception as e:
        return False

# store_password= []

# store_csv('password1', 'hi')
def check_password(password):
    data = coded.find_one({'password' : password })
    return data if data else False


def check_newdata():
    data = coded.find_one({'password' : session['newpassword']})
    return data  if data else False


@app.route('/')
def home():
    return render_template("home.html" , date=curr_date())


@app.route('/ads.txt')
def ads():
    return send_from_directory("static", "ads.txt")



@app.route("/robots.txt")
def robots_dot_txt():
    return "User-agent: *\nDisallow: /"


@app.route("/display", methods=['POST', 'GET'])
def display_data():
    if request.method == 'POST':
        session['newpassword']= request.form['password']
        result = check_password(session['newpassword'])

        if result:
            return render_template('data.html', data=result['data'],passs= request.form['password'])
        else:
            # Handle invalid password case (e.g., display an error message)
            return  render_template('data.html', data="" ,passs= request.form['password'] )

    return redirect('/')



@app.route('/final', methods=['POST', 'GET'] )
def display_newdata():
    if request.method =='POST':
        value = request.form['data']
        old_data  =check_newdata()
        try:
            if old_data and session['newpassword'] == old_data['password']:  # if old data with/without changes
                coded.find_one_and_update({'password' :session['newpassword']}, { '$set':{ 'data': value}}) #session['newpassword'] = None

                return render_template('final.html' ,change = True)
        except Exception as e:
            return '<h1>Internal servar error</h1>'
                # newdata = coded.insert_one({'password' :session['newpassword'],'data': value  } )

        else:#new data / password 
            try:
                coded.insert_one({'time': curr_date() ,'password' :session['newpassword'],'data': value  } )
                # store_password.clear
                # session['newpassword'] = None
                return render_template('final.html' ,change = False)
            except Exception as e:
                return '<h1>Internal servar error</h1>'

    return 'get <a href="/"><button> Go back </button></a>'

@app.route('/feedback', methods=['POST'])
def feedback():
    if request.method=='POST':
        # return request.form
        result= fb(request.form)
        return render_template('feedback.html', change=result)
    return redirect('/')
    
@app.errorhandler(Exception)
def erroe(e):
    return '<h1>Internal servar error</h1>'


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)