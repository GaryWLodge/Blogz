from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:launchcode@localhost:8889/Blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

app.secret_key = 'fhshshhah746J6HHCb13'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner
        

class User(db.Model):  

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))   
    password = db.Column(db.String(120)) 
    blogs = db.relationship('Blog', backref='owner')  

    def __init__(self, username, password):
        self.username = username
        self.password = password 


@app.route('/blog')
def blog():
    
    users = User.query.all()
    
    if request.args.get('id'):
        id = request.args.get('id')
        blogs = Blog.query.filter_by(id=id).all()
        return render_template('one_blog.html',blogs=blogs, users=users)

    elif request.args.get('user'):
        user = request.args.get('user')
        owner = User.query.filter_by(username=user).first()
        blogs = Blog.query.filter_by(owner=owner).all()
        return render_template('blog.html',blogs=blogs, users=users)


    else:
        blogs = Blog.query.all()
        return render_template('blog.html',blogs=blogs,users=users)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():    
    
    title_error = ''
    body_error = ''
    id = request.args.get('id')
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
       
        if title == '':
            title_error = 'Enter a Title'
            
        
            
        if body == '':
            body_error = 'Enter some Text' 
            
        
        
            
        if not title_error and not body_error:  
            owner = User.query.filter_by(username=session['username']).first()    
            new_blog = Blog(title,body,owner)
            db.session.add(new_blog)
            db.session.commit()
            
            id = new_blog.id
            id = str(id)
            
            return redirect('/blog?id='+ id)
        else:
            return render_template('newpost.html', title=title, body=body, title_error=title_error, body_error=body_error)    
    else:
        return render_template('newpost.html')    



@app.route('/signup', methods=['POST', 'GET'])
def signup():

    username_error = ''
    password_error = ''
    ver_password_error = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ver_password = request.form['ver_password']

        existing_user = User.query.filter_by(username=username).first()

        if username == '' or len(username) < 3 or len(username) > 20 or ' ' in username:
            username_error = 'Enter a valid Username'
            username = username

        if password == '' or len(password) < 3 or len(password) > 20 or ' ' in password:
            password_error = 'Enter a valid Password'
            password = ''

        if ver_password == '' or len(ver_password) < 3 or len(ver_password) > 20 or ' ' in ver_password:
            ver_password_error = 'Enter a valid Password'
            ver_password = ''

        if ver_password != password:
            ver_password_error = 'Passwords do not match'
            ver_password = ''

        if existing_user:
            flash('Username already exist', 'error')


        if not existing_user and not username_error and not password_error and not ver_password_error:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit() 
            session['username'] = username
            return redirect('/newpost')
        else:
            
            return render_template('signup.html', username=username, password=password, ver_password=ver_password, 
    username_error=username_error, password_error=password_error, ver_password_error=ver_password_error, )

    
    
    return render_template('signup.html')  


@app.route('/login', methods=['POST', 'GET'])
def login():
    
    username_error = ''
    password_error = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        existing_user = User.query.filter_by(username=username).first()


        if username == '' or len(username) < 3 or len(username) > 20 or ' ' in username:
            username_error = 'Enter a valid Username'
            username = username

        if password == '' or len(password) < 3 or len(password) > 20 or ' ' in password:
            password_error = 'Enter a valid Password'
            password = ''

        if user and user.password != password or not existing_user:
            flash('User Password incorrect or user does not exist')


        if user and user.password == password and not username_error and not password_error:
            session['username'] = username
            flash('Logged In')

            return redirect('/newpost')
        else:
            return render_template('login.html', username=username, password=password, username_error=username_error, password_error=password_error)
        
            

    return render_template('login.html')   


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
    

@app.route('/logout')
def logout():

    del session['username']
    return redirect('/blog') 
    
       


@app.route('/', methods=['POST', 'GET'])
def index():

    #username = request.args.get('username')
    users = User.query.all()
    blogs = Blog.query.all()
    return render_template('index.html',users=users, blogs=blogs)
    
    








if __name__ == '__main__':
    app.run()        
        