import os

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Database settings
database_host = "127.0.0.1"
database_port = 3306
database_username = "root"
database_password = ""
database_name = "practica"