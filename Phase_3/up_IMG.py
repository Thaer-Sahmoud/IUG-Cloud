# from flask import Flask, render_template, request, redirect, url_for
# import os
#
# app = Flask(__name__)
#
# # Set the directory where uploaded files will be saved
# app.config['UPLOAD_FOLDER'] = 'static/uploads'
#
# # Set the allowed file extensions for uploads
# app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
#
# def allowed_file(filename):
#     # Check if a file has an allowed extension
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
#
# @app.route('/')
# def index():
#     # Render the main page with a file upload form
#     return render_template('upload.html')
#
# @app.route('/upload', methods=['POST'])
# def upload():
#     # Handle file upload and redirect to a new page
#     file = request.files['file']
#     if file and allowed_file(file.filename):
#         filename = file.filename
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return redirect(url_for('uploaded_file', filename=filename))
#     else:
#         error = 'Invalid file format. Allowed formats are PNG, JPG, JPEG, and GIF.'
#         return render_template('upload.html', error=error)
#
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     # Render a page displaying the uploaded file
#     return render_template('view.html', filename=filename)
#
# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, render_template, request, redirect, flash, url_for,g
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

# Set the allowed file extensions for uploads
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    # Check if a file has an allowed extension
    print(f"The extenction is {filename.rsplit('.', 1)[1]}")
    if (filename.rsplit('.', 1)[1]).lower() in app.config['ALLOWED_EXTENSIONS']:
        validation = True
    else:
        validation = False
    print(f"Validation is {validation}")
    return validation

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return render_template('upload.html')
def home():
    return render_template('index.html')
def view():
    return render_template('view.html')
def KEYs():
    return render_template('keys.html')
def Statistics():
    return render_template('statistics.html')
def Images():
    return render_template('images.html')

@app.route('/view', methods=['GET', 'POST'])
def view():
    return render_template('view.html')

@app.route('/statistics', methods=['GET', 'POST'])
def Statistics():
    return render_template('statistics.html')

@app.route('/keys', methods=['GET', 'POST'])
def KEYs():
    return render_template('keys.html')

@app.route('/images', methods=['GET', 'POST'])
def Images():
    return render_template('images.html')

@app.route('/get_file', methods=['GET', 'POST'])
def get_file():
    file = request.files['file']
    if allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        msg_to_disp = 'File Uploaded Sucessfully'
        return render_template('upload_S.html', error=msg_to_disp)
    else:

        return render_template('upload_Invalid.html')

        # return redirect('templates/upload-Good-But-Success.html')
        # return 'file uploaded successfully'
        # return redirect(url_for('UPLOAD_FOLDER', filename=filename))

if __name__ == '__main__':
    app.run(debug=True)
