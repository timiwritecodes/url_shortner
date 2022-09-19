from url_shortner import app, db
from flask import render_template, request, flash, redirect, url_for
from random import choice
import string
from url_shortner.models import ShortUrls
from datetime import datetime


def generate_short_id(num_of_chars: int):
    """This function generates a short_id of specified number of characters."""
    return ''.join(choice(string.ascii_letters+string.digits) for i in range(num_of_chars))


@app.route('/', methods=['GET', 'POST'])
def page():
    if request.method == 'POST':
        url = request.form['url']
        short_id = request.form['custom_id']

        if short_id and ShortUrls.query.filter_by(short_id=short_id).first() is not None:
            flash('Please enter different custom id!')
            return redirect(url_for('page'))

        if not url:
            flash('The url is required')
            return redirect(url_for('page'))

        if not short_id:
            short_id = generate_short_id(8)

        new_link = ShortUrls(
            long_url=url, short_id=short_id, created_at=datetime.now())
        db.session.add(new_link)
        db.session.commit()
        short_url = request.host_url + short_id
        return render_template('page.html', custom_short_url=short_url)
    return render_template('page.html')


@app.route('/<short_id>')
def redirect_url(short_id):
    link = ShortUrls.query.filter_by(short_id=short_id).first()
    if link:
        return redirect(link.long_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('page'))

