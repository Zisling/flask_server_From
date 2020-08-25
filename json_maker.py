from flask import jsonify


def confirm_json(login_status, first_name, last_name, email, confirm=True):
    return jsonify({
        'action': 'confirm',
        'login_status': login_status,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'confirm': confirm,
    })


def post_json(confirm=True):
    return jsonify({
        'action': 'post',
        'confirm': confirm,
    })


def login_json(login_status, first_name, last_name, email, confirm=True):
    return jsonify({
        'action': 'login',
        'login_status': login_status,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'confirm': confirm,
    })


def logout_json(login_status, email, confirm=True):
    return jsonify({
        'action': 'logout',
        'login_status': login_status,
        'email': email,
        'confirm': confirm,
    })


def signup_json(login_status, first_name, last_name, email, confirm=True):
    return jsonify({
        'action': 'signup',
        'login_status': login_status,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'confirm': confirm,
    })


def is_logged_in_json(login_status, confirm=True):
    return jsonify({
        'action': 'is_logged_in',
        'login_status': login_status,
        'confirm': confirm,
    })
