import csv
import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, URL
from csv import writer

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location URL', validators=[DataRequired(), URL()])
    open = StringField('Open Time', validators=[DataRequired()])
    close = StringField('Close Time', validators=[DataRequired()])
    coffee = SelectField('Coffee Rating', choices=['✘', '☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'],
                         validators=[DataRequired()])
    wifi = SelectField('Wifi Rating', choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'],
                       validators=[DataRequired()])
    power = SelectField('Power Outlet Rating', choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'],
                        validators=[DataRequired()])
    submit = SubmitField(label='Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    new_entry = []
    if form.validate_on_submit():
        new_entry.append(form.cafe.data)
        new_entry.append(form.location.data)
        new_entry.append(form.open.data)
        new_entry.append(form.close.data)
        new_entry.append(form.coffee.data)
        new_entry.append(form.wifi.data)
        new_entry.append(form.power.data)
        with open("cafe-data.csv", mode="a", encoding="utf8", newline='') as data_file:
            writer_object = writer(data_file)
            writer_object.writerow(new_entry)
            data_file.close()
        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        length = len(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows, length=length)


if __name__ == '__main__':
    app.run(debug=True)
