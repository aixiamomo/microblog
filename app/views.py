# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect
from app import app, lm
from .forms import LoginForm
from .models import User


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
