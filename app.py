import datetime
import os
import os.path as op
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_admin as admin
from flask_admin.contrib.sqla import ModelView

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'

# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# Models
class Calls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_number = db.Column(db.Unicode(64))
    to_number = db.Column(db.Unicode(64))
    duration = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

class Sms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_number = db.Column(db.Unicode(64))
    to_number = db.Column(db.Unicode(64))
    content = db.Column(db.UnicodeText)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

# Customized admin interface
class CustomView(ModelView):
    pass

class CallsAdmin(CustomView):
    column_searchable_list = ('from_number','to_number')
    column_filters = ('from_number', 'to_number')
    can_export = True
    export_types = ['csv', 'xlsx']
    can_view_details = True

class SmsAdmin(CustomView):
    column_searchable_list = ('from_number','to_number')
    column_filters = ('from_number', 'to_number')
    can_export = True
    export_types = ['csv', 'xlsx']
    can_view_details = True

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


# Create admin with custom base template
admin = admin.Admin(app, 'Plivo SMS', template_mode='bootstrap4')

# Add views
admin.add_view(SmsAdmin(Sms, db.session))
admin.add_view(CallsAdmin(Calls, db.session))


def build_sample_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    return


if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    app.run(debug=True)