from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "admin123"

# MySQL connection (XAMPP - default user is root, no password)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.Text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        new_fb = Feedback(
            name=request.form['name'],
            email=request.form['email'],
            message=request.form['message']
        )
        db.session.add(new_fb)
        db.session.commit()
        return render_template('thankyou.html')
    return render_template('feedback.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['admin'] = True
            return redirect('/dashboard')
        return render_template('admin_login.html', error="Invalid credentials")
    return render_template('admin_login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect('/admin')
    feedbacks = Feedback.query.all()
    return render_template('admin_dashboard.html', feedbacks=feedbacks)

@app.route('/delete/<int:id>')
def delete_feedback(id):
    if session.get('admin'):
        fb = Feedback.query.get(id)
        db.session.delete(fb)
        db.session.commit()
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')
@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)