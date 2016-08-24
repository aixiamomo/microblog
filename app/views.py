# -*- coding: utf-8 -*-
from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Aixia'}
    posts = [
        {
            'author': {'nickname': 'momo'},
            'body': 'Beautiful night in Songjiang!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': u'夜凉如水'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)
