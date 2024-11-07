from flask import Blueprint, render_template, redirect, session, url_for, request, flash, jsonify
from json_functions import read_data, write_data

friends_bp = Blueprint('friends',__name__,url_prefix='/friends')

@friends_bp.route('/main',methods = ['GET'])
def friends():
    if 'user_id' not in session:
        redirect(url_for('login'))
    users_data = read_data()
    user = next((user for user in users_data['users'] if user['user_id'] == session['user_id']), None)
    if user:
        recommended_ids = user['recommended_friends']
        recommended_friends = [
            next((u for u in users_data['users'] if u['user_id'] == rid), None)
            for rid in recommended_ids
        ]
        friend_ids = user['friends']
        real_friends = [
            next((f for f in users_data['users'] if f['user_id'] == fid),None)
            for fid in friend_ids
        ]
        print(recommended_friends)
        return render_template('friends.html', friends=recommended_friends, real_friends = real_friends, user = user)
    return "User not found", 404

@friends_bp.route('/add_friend', methods=['POST'])
def add_friend():
    user_id = session['user_id']
    friend_id = request.json.get('friend_id')

    users_data = read_data()
    user = next((u for u in users_data['users'] if u['user_id'] == user_id), None)
    friend = next((u for u in users_data['users'] if u['user_id'] == friend_id), None)

    if user and friend:

        if friend_id not in user['friend_requests']['sent'] and user_id not in friend['friend_requests']['received']:
            user['friend_requests']['sent'].append(friend_id)
            friend['friend_requests']['received'].append(user_id)
        # Remove from recommended friends
        if friend_id in user['recommended_friends']:
            user['recommended_friends'].remove(friend_id)

        # Save updated JSON data
        write_data(users_data)
        return jsonify({"success": True}), 200

    return jsonify({"error": "User or friend not found"}), 404