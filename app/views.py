"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from .forms import SignUpForm, SendID
from .models import UserProfile
from werkzeug.utils import secure_filename
import os, datetime, json, psycopg2

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

def format_date_joined():
    now=datetime.datetime.now();
    date_joined=datetime.date(now.year, now.month, now.day)
    d= "Joined " + date_joined.strftime("%B %d, %Y")
    return d
    
@app.route('/profile', methods=["GET","POST"])
def profile():
    form=SignUpForm()
    if request.method == "POST" and form.validate_on_submit():
        check = UserProfile.query.filter_by(email = form.email.data).first()
        if not check:
            img_data = form.image.data
            filename = secure_filename(img_data.filename)
            img_data.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            join=format_date_joined()
            user = UserProfile(form.fname.data, form.lname.data, form.gender.data, form.email.data, form.location.data, form.bib.data, filename, join )
            db.session.add(user)
            db.session.commit()
            flash("Profile successfully created", category="success")
            return redirect(url_for('profiles'))
    flash("Profile creation fail", category="danger")
    return render_template("profile.html", form=form)
 
@app.route('/profiles', methods=["GET","POST"])    
def profiles():
    form=SendID
    if request.method == "POST":
        flash(form.myid)
        return redirect(url_for('home'))
    return render_template('profiles.html', a=getall(),d="", form=form)
    
def getall():
    conn = None
    conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'], sslmode='require') 
    cur = conn.cursor()
    cur.execute("SELECT myid,fname, lname, gender,location, image from user_profile")
    row=cur.fetchall()
    cur.close()
    if conn is not None:
        conn.close()
    return row
    
@app.route('/profile/<userid>', methods=["GET","POST"])
def show_user_profile(userid):
    form=""
    check= UserProfile.query.filter_by(myid = userid).first()
    if check:
        d = getperson(userid)
        return render_template("individual.html", d = getperson(userid))
    return render_template("profile.html",form=form)
    
def getperson(userid):
    myid=int(userid)
    
    conn = None
    conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI']) 
    cur = conn.cursor()
    i=userid
    cur.execute("select * from user_profile where myid= myid")
    row=cur.fetchall()
    cur.close()
    
    for rows in row:
        if rows[0]==myid:
            return rows
    return row
    
    


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
