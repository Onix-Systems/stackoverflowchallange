#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, session
from tools import make_request, build_auth_url, make_post_auth_url, \
    make_get_user_request
from forms import UserIdForm

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'myverylongsecretkey'
app.config.from_object('config')


@app.route('/')
@app.route('/index.html')
def index():
    app.logger.debug("Home page")
    return render_template('index.html')


@app.route('/posts', methods=('GET', 'POST'))
def posts():
    form = UserIdForm()
    user_id = request.args.get('user_id')
    page = request.args.get('page', 1)
    if user_id is None and not form.validate_on_submit():
        return render_template('posts_form.html', form=form)

    if form.validate_on_submit():
        user_id = form.user_id.data

    error, data = make_request(app, user_id, page)

    if error:
        app.logger.debug(error)
        return render_template('posts_form.html', form=form, error=error)
    else:
        page_next = False
        page_prev = False
        if data['has_more']:
            page_next = int(page) + 1
        if int(page) > 1:
            page_prev = int(page) - 1
        return render_template('posts_list.html', data=data, user_id=user_id,
                               page=page, page_next=page_next,
                               page_prev=page_prev)


@app.route('/myposts')
def myposts():
    user_id = None
    if 'user_id' in session:
        user_id = session['user_id']

    if user_id is None:
        code = request.args.get('code')
        if code is None:
            url = build_auth_url(app)
            return redirect(url)
        if code is not None:
            error, access_token = make_post_auth_url(app, code)
            if error:
                app.logger.error(error)
            if access_token is not None:
                user_error, user_id = make_get_user_request(app, access_token)
                if user_error:
                    app.logger.error(user_error)
                session['user_id'] = user_id
                app.logger.debug(user_id)

    error, data = make_request(app, user_id)
    if error:
        app.logger.error(error)

    page_next = False
    page_prev = False
    if data['has_more']:
        page_next = 2

    return render_template('posts_list.html', data=data, user_id=user_id,
                           page=1, page_next=page_next, page_prev=page_prev)


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
