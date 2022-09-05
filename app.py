from flask import Flask,session,render_template,request,redirect,g, url_for
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)

data_store ={'name':"password"}

@app.route("/",methods=['GET','POST'])
def index():
    if request.method =="POST":
        session.pop("user",None)
        if request.form['username'] in  data_store.keys()and request.form['password'] in data_store[request.form['username']]:
            session['user']=request.form['username']
            return redirect(url_for("protected"))
    return render_template('index.html')        

@app.route('/proteced')
def protected():
    if g.user:
        return render_template("protected.html",user=session)
    return redirect(url_for('index'))

@app.route('/new')
def new():
    if g.user:
        return render_template("oneMore.html")
    return redirect(url_for(index))        

@app.before_request
def before_request():
    g.user = None
    if "user" in session:
        g.user = session['user'] 

@app.route('/dropsession')
def dropseesion():
    session.pop('user',None)    
    return render_template('index.html')    

@app.route('/singups')
def singups():
    return render_template('index')



@app.route('/singup',methods=['GET','POST'])
def singup():
     if request.method =="POST":
        name = request.form['username'] 
        password = request.form['password'] 
        data_store[name]=password
        return redirect(url_for('index'))
     return render_template('singup.html')




if __name__ =='__main__':
    app.run(debug=True)
