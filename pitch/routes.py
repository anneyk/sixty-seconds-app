import os
import secrets
from flask import abort, render_template, request, url_for, flash, redirect
from pitch import app, db, mail
from pitch.forms import PitchForm, RegistrationForm, LoginForm, UpdateForm, CommentForm, RequestResetForm, ResetPasswordForm
from pitch.models import User, Pitch, Comment
from flask_login import login_user, current_user,login_required, logout_user 
from flask_mail import Message






# Views
@app.route('/', methods=['GET','POST'])
def index():

    '''
    View root page function that returns the index page and its data
    '''
    
   
    comments = Comment.query.all()
    pitches = Pitch.query.all()
    user = User.query.all()
    users = list(reversed(user))
    limit = 20
    business = Pitch.query.filter_by(category = 'Business').all()
    finance= Pitch.query.filter_by(category = 'Finance').all()
    relationships= Pitch.query.filter_by(category = 'Relationships').all()
    wellbeing = Pitch.query.filter_by(category = 'Well-Being').all()
    
    return render_template('index.html', pitches = pitches,limit=limit, business=business, finance=finance, relationships=relationships, wellbeing=wellbeing, users=users, comments=comments)

def new_func():
    comments = Comment.query.all()

@app.route('/about')
def about():
    
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form= RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form= LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        password = User.query.filter_by(password=form.password.data).first()
        if user and password:
            login_user(user, remember=form.remember.data)
            flash('Login Successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check your username or password!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        
    
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Updated Successfully!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/pitch/new', methods=['GET', 'POST'])
@login_required
def new_pitch():
    form = PitchForm()
    
    if form.validate_on_submit():
        pitch = Pitch(title=form.title.data, category=form.category.data , content=form.content.data,  author=current_user )
        db.session.add(pitch)
        db.session.commit()
        flash('Pitch Created Successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create_pitch.html', title='New Pitch', form=form, legend='New-Pitch')

@app.route('/pitch/<int:pitch_id>')
@login_required
def pitch(pitch_id):
    pitch = Pitch.query.get_or_404(pitch_id)
    return render_template('pitch.html', pitch=pitch)
    
    
@app.route('/pitch/<int:pitch_id>/update',methods=['GET', 'POST'])
@login_required
def update_pitch(pitch_id):
    pitch = Pitch.query.get_or_404(pitch_id)
    if pitch.author != current_user:
        abort(403)
        
    form = PitchForm()
    if form.validate_on_submit():
        pitch.title = form.title.data
        pitch.content = form.content.data
        db.session.commit()
        flash('Pitch Updated', 'success')
        return redirect(url_for('pitch', pitch_id=pitch.id))
    elif request.method == "GET":
        form.title.data = pitch.title
        form.content.data = pitch.content
    return render_template('create_pitch.html', form=form, legend='Update Post')
    

@app.route('/pitch/<int:pitch_id>/delete',methods=['POST'])
@login_required
def delete_pitch(pitch_id):
    pitch = Pitch.query.get_or_404(pitch_id)
    if pitch.author != current_user:
        abort(403)
    db.session.delete(pitch)
    db.session.commit()
    flash('Pitch Deleted', 'success')
    return redirect(url_for('index'))

@app.route('/pitch/<int:pitch_id>/comment',methods=['GET', 'POST'])
@login_required
def comment_pitch(pitch_id):
    
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = Comment(userdata=form.userdata.data)
        pitch_id= Comment(pitch_id=pitch_id)
        db.session.add(comment,pitch_id)
        db.session.commit()
        flash('Comment added!', 'success')
        return redirect(url_for('index'))
    return render_template('comment.html', title='New comment', form=form, legend='Add a comment')

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request', sender='minutepitcher@gmail.com', recipients=[user.email])
    
    msg.body = f''' To Reset Your Password,visit the following link:
    
    { url_for('reset_token', token=token, _external=True) } 
    
    If you did not make this request, ignore this mail and no changes will be made
    
    '''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An Email has been sent with instructions on how to reset your password. Check Your Spam as well', 'info')
    
    return render_template('reset_request.html', title='Request Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid token or it has expired', 'warning')
        return redirect(url_for('reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        db.session.commit()
        flash('Password Reset Successfully, You can now login to access account features!', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_token.html', title='Request Password', form=form)

