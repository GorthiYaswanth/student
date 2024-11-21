from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask('_name_')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Reddy%4096320@localhost:5433/amazon_app'

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usn = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    age = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(1000), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    parent_name = db.Column(db.String(100), nullable=False)
    parent_address = db.Column(db.String(1000), nullable=True)


with app.app_context():
    db.drop_all()
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    data = Todo.query.all()
    context = []
    for dt in data:
        dd = {"id": dt.id, "usn": dt.usn, "name": dt.name, "age": dt.age, "dob":dt.dob, "email":dt.email, "contact":dt.contact, "address":dt.address, "parent_name":dt.parent_name, "parent_address":dt.parent_address}
        context.append(dd)
    print(context)
    # print("data: {}".format(data))
    return render_template('todo.html', todo=context)


@app.route('/add-task')
def add_task():
    return render_template('add_task.html')


@app.route('/submit', methods=['POST'])
def create_user():
    usn = request.form['usn']
    name = request.form['name']
    age = request.form['age']
    dob = request.form['Date of Birth']
    email = request.form['email']
    contact = request.form['contact']
    address = request.form['address']
    parent_name = request.form['parent_name']
    parent_address = request.form['parent_address']
    print(f"usn is: {usn}, name is: {name}, age is: {age}, dob is: {dob}, email is:{email}, contact is: {contact}, address is: {address}, parent_name is:{parent_name}, parent_address is: {parent_address}")
    new_task = Todo(usn=usn, name=name, age=age, dob=dob, email=email, contact=contact, address=address, parent_name=parent_name, parent_address=parent_address)
    print("new_task: {}".format(new_task))
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('add_task'))


@app.route('/delete/<int:id>', methods=['GET', 'DELETE'])
def delete_user(id):
    task = Todo.query.get(id)
    print("task: {}".format(task))

    if not task:
        return jsonify({'message': 'task not found'}), 404
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'task deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while deleting the data {}'.format(e)}), 500


@app.route('/update_task/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    task = Todo.query.get_or_404(id)
    print(task.id)
    if not task:
        return jsonify({'message': 'task not found'}), 404

    if request.method == 'POST':
        task.usn = request.form['usn']
        task.name = request.form['name']
        task.age = request.form['age']
        task.dob = request.form['age']
        task.email = request.form['email']
        task.contact = request.form['contact']
        task.address = request.form['address']
        task.parent_name = request.form['parent_name']
        task.parent_address = request.form['parent_address']

        try:
            db.session.commit()
            return redirect(url_for('index'))

        except Exception as e:
            db.session.rollback()
            return "there is an issue while updating the record"
    return render_template('update.html', task=task)


if __name__== '__main__':
    app.run(host='127.0.0.1', port=5002,debug=True)