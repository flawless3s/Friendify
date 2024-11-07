from flask import Blueprint, render_template, redirect, session, url_for, request, flash, jsonify
from json_functions import read_data, write_data

connections_bp = Blueprint('connections',__name__,url_prefix='/connections')


def get_user_details(user_id, all_users):
    user = next((user for user in all_users if user["user_id"] == user_id), None)
    if user:
        return {
            "user_id": user["user_id"],
            "username": user["username"],
            "profile_picture": user["profile_picture"]
        }
    return None

@connections_bp.route('/friend_requests',methods=['GET','POST'])
def requests():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    data = read_data()
    logged_in_user_id = session['user_id']  # Replace this with the actual logged-in user's ID dynamically
    
    # Find the logged-in user's data
    user_data = next((user for user in data["users"] if user["user_id"] == logged_in_user_id), None)
    
    if user_data:
        all_users = data["users"]
        
        # Retrieve details for sent friend requests
        sent_requests = [
            get_user_details(user_id, all_users) for user_id in user_data["friend_requests"].get("sent", [])
        ]
        
        # Retrieve details for received friend requests
        received_requests = [
            get_user_details(user_id, all_users) for user_id in user_data["friend_requests"].get("received", [])
        ]
        print(sent_requests)
        requests = {
            "sent": [req for req in sent_requests if req],
            "received": [req for req in received_requests if req]
        }
    else:
        requests = {
            "sent": [],
            "received": []
        }
    
    # Pass the requests structure to the template
    return render_template('connections.html', requests=requests,user=user_data)


@connections_bp.route('/accept_request/<int:user_id>/<int:requester_id>', methods=['POST','GET'])
def accept_request(user_id, requester_id):
    if request.method == 'POST':
        print("Hello")
        data = read_data()
        for user in data["users"]:
            if user["user_id"] == user_id:
                # Add requester to user's friends list
                user["friends"].append(requester_id)
                # Remove from received requests
                user["friend_requests"]["received"].remove(requester_id)
                break
        # Also add the user as a friend in the requester's friends list
        for user in data["users"]:
            if user["user_id"] == requester_id:
                user["friends"].append(user_id)
                user["friend_requests"]["sent"].remove(user_id)
                break
        write_data(data)
        return jsonify(success=True), 200

# Route to decline a friend request
@connections_bp.route('/decline_request/<int:user_id>/<int:requester_id>', methods=['POST'])
def decline_request(user_id, requester_id):
    data = read_data()
    for user in data["users"]:
        if user["user_id"] == user_id:
            # Remove from received requests
            user["friend_requests"]["received"].remove(requester_id)
            break
    write_data(data)
    return jsonify(success=True), 200