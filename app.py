
from operator import ipow
from flask import Flask, render_template, url_for, request, redirect,flash

from flask_sqlalchemy import SQLAlchemy

from dbconfig import connection

from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)

csrf = CSRFProtect()

csrf.init_app(app)

app.config['SECRET_KEY'] = 'okbro'

app.config['SQLALCHEMY_DATABASE_URI'] = connection

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Model
class NoteList(db.Model):
    __tablename__ ='notes'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    note_name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self,author,note_name,date_created,content):
        self.author = author
        self.note_name = note_name
        self.date_created = date_created
        self.content = content


@app.route('/')
def index():
    data = NoteList.query.all()
    return render_template('pages/main.html', data=data)

 
@app.route('/note/create',methods=['POST','GET'])
def create():
    if request.method == 'POST':
        author = request.form.get('author') #lấy ra trong request cái thằng có name là author
        note_name = request.form.get('note_name')
        date_created = request.form.get('date_created')
        content = request.form.get('content')
        new_note = NoteList(author=author, note_name=note_name, date_created=date_created, content=content)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('index')) 
    else:
        return render_template('pages/create.html')    

@app.route('/note/delete/<id>',methods=['GET','POST'])
def delete(id):
        delete_data = NoteList.query.filter_by(id=id).first()
        db.session.delete(delete_data)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/note/edit/<id>',methods=['GET'])
def edit(id):
    edit_data = NoteList.query.filter_by(id=id).first()
    return render_template('pages/edit.html',edit_data=edit_data)

@app.route('/note/update',methods=['POST'])
def update():
    update_data = NoteList.query.get(request.form.get('id'))  
    update_data.author = request.form.get('author')
    update_data.note_name = request.form.get('note_name')
    update_data.date_created = request.form.get('date_created')
    update_data.content = request.form.get('content')
    
    db.session.commit()
    flash('Update thành công Note')
    return redirect(url_for('index'))
            

#Mô hình của Flask là mô hình MVC    