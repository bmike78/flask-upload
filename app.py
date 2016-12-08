import os
import psutil
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = '/upload/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'vmdk', 'ova', 'log', 'mf', 'ovf', 'gz', 'zip', 'qcow2', 'iso', 'exe', 'rpm', 'tar'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# disk usage for upload folder
def diskusage(partition):
    disk = psutil.disk_usage(partition)
    # Divide from Bytes -> KB -> MB -> GB
    free = round(disk.free/1024.0/1024.0/1024.0,1)
    total = round(disk.total/1024.0/1024.0/1024.0,1)
    return str(free) + 'GB free / ' + str(total) + 'GB total ( ' + str(disk.percent) + '% )'


# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html', disk=diskusage(app.config['UPLOAD_FOLDER']))

@app.route('/<user>')
def index_user(user):
    directory = '/upload/%s' % user
    if not os.path.isdir(directory):
      os.makedirs(directory)
    
    return render_template('index.html', user=user, disk=diskusage(app.config['UPLOAD_FOLDER']))

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to the upload
            # folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Save the filename into a list, we'll use it later
            filenames.append(filename)
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
    # Load an html page with a link to each uploaded file
    return render_template('upload.html', filenames=filenames, disk=diskusage(app.config['UPLOAD_FOLDER']))

# Route that will process the file upload
@app.route('/<user>/upload', methods=['POST'])
def upload_user(user):
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to the upload
            # folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + user, filename))
            # Save the filename into a list, we'll use it later
            filenames.append(filename)
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
    # Load an html page with a link to each uploaded file
    return render_template('upload.html', filenames=filenames, user=user, disk=diskusage(app.config['UPLOAD_FOLDER']))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/<user>/uploads/<filename>')
def uploaded_file_user(filename,user):
    return send_from_directory(app.config['UPLOAD_FOLDER'] + "/" + user,
                               filename)


@app.route('/uploads', defaults={'path': ''})
@app.route('/uploads/<path:path>')
def uploads(path):
    BASE_DIR = '/upload'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('files.html', files=files, disk=diskusage(app.config['UPLOAD_FOLDER']))

@app.route('/<user>/uploads')
def uploads_user(user):
    BASE_DIR = '/upload/%s' % user

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('files.html', files=files, user=user, disk=diskusage(app.config['UPLOAD_FOLDER']))

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("8000"),
        threaded=True,
        debug=True
    )
