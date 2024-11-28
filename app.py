from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  
app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=True)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) ->str:
        return f"{self.sno}-{self.title}"
@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        # Create a new Todo item
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    # Fetch all Todo items to display on the page
    allTodo = Todo.query.all()
    print(allTodo)

    return render_template('index.html', allTodo=allTodo)

# @app.route("/update")
# def update():


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    
    if todo is None:
        # Optionally, add a flash message or handle the case where no record is found
        flash('Todo not found!', 'error')
        return redirect('/')  # or a custom error page
    
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')



if __name__=="__main__":
    app.run(debug=True)