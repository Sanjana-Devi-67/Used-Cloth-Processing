from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_name = db.Column(db.String(100), nullable=False)
    cloth_type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_donated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    condition = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # redirects if user not logged in


# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------- ROUTES ----------
@app.route('/')
def home():
    return redirect(url_for('login'))  # or 'register' or 'dashboard' as you prefer

@app.route('/donations')
def donations():
    all_donations = Donation.query.all()
    return render_template('donations.html', donations=all_donations)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check first if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already taken", "error")
            return redirect(url_for('register'))

        # If not, hash password and add new user
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash('Registered successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # ✅ Make sure this line is there
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard', 'warning')
        return redirect(url_for('login'))

    items = Donation.query.all()  
    return render_template('dashboard.html', items=items)

@app.route('/update_status/<int:item_id>', methods=['POST'])
def update_status(item_id):
    item = Donation.query.get_or_404(item_id)

    if item.status == 'Pending':
        item.status = 'Received'
    elif item.status == 'Received':
        item.status = 'Processing'
    elif item.status == 'Processing':
        item.status = 'Distributed'

    db.session.commit()
    flash('Status updated successfully', 'info')
    return redirect(url_for('dashboard'))


def delete_item(item_id):
    if 'user_id' not in session:
        flash('Please log in', 'warning')
        return redirect(url_for('login'))

    item = ClothItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully', 'danger')
    return redirect(url_for('dashboard'))
@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        donor_name = request.form['donor_name']
        cloth_type = request.form['cloth_type']
        quantity = int(request.form['quantity'])
        condition = request.form['condition']

        new_donation = Donation(
            donor_name=donor_name,
            cloth_type=cloth_type,
            quantity=quantity,
            condition=condition,
            status='Pending'
        )
        db.session.add(new_donation)
        db.session.commit()
        flash('Donation submitted successfully!')
        return redirect(url_for('donations'))

    return render_template('donate.html')  # use a separate donate form template
@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = Donation.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('dashboard'))  # or wherever your donation list is

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))


# Create database tables
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
 