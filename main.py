from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    

    def __init__(self, title, body):
        self.title = title
        self.body = body
        


@app.route('/blog')
def blog():
    

    
    if not request.args.get('id'):
        blogs = Blog.query.all()
        return render_template('blog.html',blogs=blogs)

    else:
        id = request.args.get('id')
        blogs = Blog.query.filter_by(id=id).all()
        return render_template('one_blog.html',blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():    
    
    title_error = ''
    body_error = ''

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if title == '':
            title_error = 'Enter a Title'
            title = title
        
            
        if body == '':
            body_error = 'Enter some Text' 
            body = body
        
        
            
        if not title_error and not body_error:      
            new_blog = Blog(title,body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog')
        else:
            return render_template('newpost.html', title=title, body=body, title_error=title_error, body_error=body_error)    
    else:
        return render_template('newpost.html')    




@app.route('/blog?id=')
def one_blog():
    title = request.args.get('title')
    body = request.args.get('body')


    return render_template('one_blog.html')



@app.route('/', methods=['POST', 'GET'])
def index():
    
    return render_template('blog.html')  








if __name__ == '__main__':
    app.run()        
        