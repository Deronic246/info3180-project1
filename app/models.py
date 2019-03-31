from . import db


class UserProfile(db.Model):
    myid = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    gender = db.Column(db.String(80))
    email = db.Column(db.String(255), unique=True)
    location = db.Column(db.String(255))
    bib = db.Column(db.String(255))
    image = db.Column(db.String(255))
    date_joined=db.Column(db.String(255))
    
    def __init__(self, first_name, last_name, gender, email, location, bib, image, date_joined):
        self.fname = first_name
        self.lname = last_name
        self.gender = gender
        self.email = email
        self.location = location
        self.bib = bib
        self.image = image
        self.date_joined = date_joined

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '%s %s' % (self.fname, self.lname)
