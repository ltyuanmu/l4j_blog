#-*- coding=utf-8 -*-
import datetime
from flask import jsonify, redirect, render_template, request, session, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from . import admin
from .. import db
from ..models import *
from .forms import *
from .. import logger
from datetime import datetime
import json


def timenow(): return datetime.now()

# admin


@admin.before_request
def before_request():
    global ip
    try:
        ip = request.headers['X-Forwarded-For'].split(',')[0]
    except:
        ip = request.remote_addr


@admin.route('/', methods=['GET', 'POST'])
@login_required
def admin_index():
    return render_template('admin/index.html', position=u'控制台')


@admin.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'POST':
        title = request.form.get("title")
        context = request.form.get("editor1")
        description = context[:255]
        post = Post(title=title, context=context, description=description)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('admin.manage_posts'))
    return render_template('admin/edit_post.html', position=u'新增文章')


@admin.route('/manage-posts', methods=['GET', 'POST'])
@login_required
def manage_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.inserttime.desc()).paginate(
        page, per_page=50, error_out=False)
    posts = pagination.items
    return render_template('admin/manage_posts.html', position=u'管理文章', pagination=pagination, posts=posts, endpoint='admin.manage_posts')


@admin.route('/manage-post/delete-post/<int:pid>')
@login_required
def delete_post(pid):
    referer = request.headers['Referer']
    post = Post.query.get_or_404(pid)
    db.session.delete(post)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        flash(u'删除文章失败！', 'danger')
    else:
        flash(u'删除文章成功！', 'success')
    if request.args.get('delete_type') == 'admin':
        page = request.args.get('page', 1, type=int)
        return redirect(url_for('admin.delete_post',
                                page=page))

    return redirect(referer)


@admin.route('/manage-posts/delete-posts', methods=['GET', 'POST'])
@login_required
def delete_comments():
    if request.method == 'POST':
        data = request.form.to_dict()
        pids = list(eval(data['commentIds']))
        count = 0
        for pid in pids:
            post = Post.query.get_or_404(int(pid))
            count += 1
            db.session.delete(post)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'删除失败！', 'danger')
        else:
            flash(u'成功删除%s篇文章！' % count, 'success')
    page = request.args.get('page', 1, type=int)
    return redirect(url_for('admin.manage_posts', page=page))


@admin.route('/edit_post/<int:pid>', methods=['GET', 'POST'])
@login_required
def edit_post(pid):
    post = Post.query.get_or_404(pid)
    if request.method == 'POST':
        title = request.form.get("title")
        context = request.form.get("editor1")
        post.title = title
        post.context = context
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('admin.manage_posts'))
    page = request.args.get('page', 1, type=int)
    return render_template('admin/edit_post.html', position=u'编辑文章', post=post, page=page)
