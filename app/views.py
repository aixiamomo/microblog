# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm, db, oid
from .forms import LoginForm
from .models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
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
@oid.loginhandler  # 告诉flask-openid 这是登陆视图函数
def login():
    if g.user is not None and g.user.is_authenticated:  # 判断g.user是否被设置成一个认证用户
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])  # 触发用户使用Flask-OpenID认证
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])  # 失败，重新返回登陆页


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@oid.after_login  # tyr_login触发认证，认证成功调用注册了这个装饰器的函数
def after_login(resp):  # resp是从OpenID提供商返回的信息
    if resp.email is None or resp.email == '':
        flash('Invalid login. Please tyr again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:  # 新用户
        nickname = resp.nickname
        if nickname is None or nickname == '':
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop(remember_me, None)
    login_user(user, remember=remember_me)  # 标记这个用户为登陆
    return redirect(request.args.get('next') or url_for('index'))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test body #1'},
        {'author': user, 'body': 'Test body #1'}
    ]
    return render_template('user.html',
                           user=user,
                           posts=posts)

