import os
from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/loans_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Users {self.phone_number}>'

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if(request.method == 'POST'):
        fullname = request.form['fullname']
        phone_number = request.form['phone_number']
        password = request.form['password']
        user = Users( fullname = fullname, phone_number = phone_number, password = password )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    user = Users.query.get_or_404(id)

    if(request.method) == 'POST':
        fullname = request.form['fullname']
        phone_number = request.form['phone_number']
        password = request.form['password']

        user.fullname = fullname
        user.phone_number = phone_number
        user.password = password

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('edit.html', user=user)

@app.post('/<int:id>/delete/')
def delete(id):
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/')
def index():
    users = Users.query.all()
    #users = Users.query.filter_by(fullname='Ben Ndiwa').all()
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000)
