#-*- coding=utf-8 -*-
from . import app, db
from .models import *
from flask import render_template, make_response, redirect, request, url_for, flash, session, jsonify, g, current_app


@app.before_request
def before_request():
    global ip
    try:
        ip = request.headers['X-Forwarded-For'].split(',')[0]
    except:
        ip = request.remote_addr

@app.route('/')
def index():
    page=request.args.get('page',1, type=int)
    pagination = Post.query.order_by(Post.inserttime.desc()).paginate(page, per_page=50, error_out=False)
    posts=pagination.items
    return render_template('index.html',pagination=pagination,posts=posts,endpoint='.index')

@app.route('/p/<pid>')
def show_post(pid):
    post=Post.query.filter_by(pid=pid).first()
    post.add_views(pid)
    return render_template('show_post.html',post=post)