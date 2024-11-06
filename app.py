from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from json_functions import read_data, write_data
from gallery import gallery_bp
from connections import connections_bp
from friends import friends_bp

app = Flask(__name__)

# Set a secret key for the session
app.secret_key = 'jhhgdg-5678'  # Replace with a strong random key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() 
        username = data['username']
        password = data['password']
        email = data['email']
        data_file = read_data()

        for user in data_file['users']:
            if user['username'] == username:
                return jsonify({'error': 'Username already taken'}), 400
            if user['email'] == email:
                return jsonify({'error': 'Email already registered'}), 400

        # Create new user data
        new_user = {
            "user_id": len(data_file["users"]) + 1,
            "username": username,
            "password": password,
            "email": email,
            "profile_picture": "",
            "friends": [],
            "friend_requests": {
                "sent": [],
                "received": []
            },
            "recommended_friends": [i['user_id'] for i in data_file['users']],
            "posts": []
        }

        data_file["users"].append(new_user)
        write_data(data_file)

        return jsonify({'success': True, 'message': 'You have registered successfully'})
    return render_template("Register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('name')
        password = request.form.get('password')
    
        data = read_data()

        for user in data['users']:
            if username == user['username'] and password == user['password']:
                session['user_id'] = user['user_id'] 
                session['username'] = username 
                return redirect(url_for("home"))
        else:
            return jsonify({"message": "Invalid Login Credentials"}), 401
    
    return render_template('Login.html')

@app.route("/dashboard", methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    # Load user data
    data = read_data()
    
    current_user = next((user for user in data['users'] if user['user_id'] == session['user_id']), None)
    friend_posts = []
    if current_user:
        for friend_id in current_user['friends']:
            friend = next((user for user in data['users'] if user['user_id'] == friend_id), None)
            if friend:
                for post in friend['posts']:
                    friend_posts.append({
                        "username": friend['username'],
                        "post": post
                    })

    return render_template("home.html", posts=friend_posts, user=current_user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

app.register_blueprint(gallery_bp)
app.register_blueprint(connections_bp)
app.register_blueprint(friends_bp)
if __name__ == "__main__":
    app.run(debug=1, port=1111)
