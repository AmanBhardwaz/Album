from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/<album_type>', methods=['GET', 'POST'])
def upload(album_type):
    # Validate album type
    valid_album_types = ['marriage', 'birthday', 'couple', 'love']
    if album_type not in valid_album_types:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        files = request.files.getlist('images')
        
        # Check if any files were selected
        if not files or all(not file.filename for file in files):
            flash('Please select at least one image file.')
            return render_template('upload.html', album_type=album_type)

        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], album_type)
        os.makedirs(folder_path, exist_ok=True)
        image_names = []

        for file in files[:5]:  # Limit to 5 images
            if file.filename:
                # Validate file type
                if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    continue
                
                path = os.path.join(folder_path, file.filename)
                try:
                    file.save(path)
                    image_names.append(f"{album_type}/{file.filename}")
                except Exception as e:
                    print(f"Error saving file {file.filename}: {e}")
                    continue

        if not image_names:
            flash('No valid images were uploaded. Please try again.')
            return render_template('upload.html', album_type=album_type)

        return render_template('album.html', album_type=album_type, images=image_names)

    return render_template('upload.html', album_type=album_type)

if __name__ == '__main__':
    app.run(debug=True)
