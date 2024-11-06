from flask import Blueprint, render_template, redirect, session, url_for, request, flash
from json_functions import read_data, write_data
from werkzeug.utils import secure_filename
import os

gallery_bp = Blueprint('gallery',__name__,url_prefix='/gallery')

UPLOAD_FOLDER = 'static/assets/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@gallery_bp.route("/your_posts",methods=['GET','POST'])
def your_posts():
    if 'user_id' not in session:
        return redirect(url_for("login"))
    
    data = read_data()

    current_user = next((user for user in data['users'] if user['user_id'] == session['user_id']),None)

    current_user_posts = []
    if current_user:
        for post in current_user['posts']:
            current_user_posts.append(post)
        
    return render_template("user_posts.html",posts = current_user_posts, user= current_user)

@gallery_bp.route("/new_post",methods=['GET','POST'])
def new_post():
    if 'user_id' not in session:
        return redirect(url_for("login"))
    data = read_data()
    current_user = next((user for user in data['users'] if user['user_id'] == session['user_id']),None)
    
    if request.method == 'POST':

        if 'image' not in request.files:
            flash('No image file part')
            return redirect(request.url)
        
        image = request.files['image']
        caption = request.form.get('caption')

        if image.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)

            image_url = url_for('static', filename=f'assets/img/{filename}')
            print(f"Caption: {caption}")
            print(f"Image saved to: {image_url}")
            
            user_index = (next((index for index, user in enumerate(data['users']) if user['user_id'] == session['user_id']), None))


            try:
                temp = user_index + 1
            except:
                pass
            if user_index or temp:
                new_post ={
                        "post_id": str(session['user_id'])+"0"+str(len(data['users'][user_index]['posts'])+1),
                        "caption": caption,
                        "image_url": image_url[7:],
                        "likes": 0
                    }
                
                data['users'][user_index]['posts'].append(new_post) 
                write_data(data)
                return redirect(url_for('gallery.your_posts'))
        else:
            flash('Invalid file type. Only images are allowed.')
            return redirect(request.url)
            

    return render_template('new_post.html', user = current_user )


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS