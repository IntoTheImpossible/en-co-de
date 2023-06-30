from flask import Flask, request, render_template, redirect,url_for,session
from flask_mail import Mail, Message
import steganography 
import secrets
import string
import os

# allowed extentions
ALLOWED_EXTENSIONS = {'png'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Generate a random key with a length of * characters
def generate_random_key(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_key = ''.join(secrets.choice(characters) for _ in range(length))
    return random_key



app = Flask(__name__)
# Generate a random key with a length of 32 characters
app.secret_key = generate_random_key(32)


app.config['MAIL_SERVER'] = ''  # Replace with your SMTP server
app.config['MAIL_PORT'] = 0  # Replace with the SMTP port
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ''  # Replace with your email address
app.config['MAIL_PASSWORD'] = ''  # Replace with your email password

mail = Mail(app)

# index get request
@app.route("/")
def index():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('error.html', error ='No file uploaded' )
    file = request.files['file']
    try:
        process = request.form["selectedOption"]
    except:
        return render_template("error.html", error="You didn`t select option")
    
    if file.filename == '':
        return render_template('error.html', error = 'No selected file')
    # if file.filename.endswith('.txt'):     enother one method for one type check
    if file and allowed_file(file.filename):
    # Process the file upload
        file.save('uploads/' + file.filename)
        # return 'File uploaded successfully'
    if file and not allowed_file(file.filename):
            return render_template('error.html', error = 'Invalid file format')
    session['_imgname'] = file.filename
    # redirects from radiobuttons
    if process == "encr":
        return redirect(url_for("encrypt"))
    if process == "dec":
        return redirect(url_for("decode"))

    



@app.route("/decode",methods=["GET","POST"])
def decode():
    if request.method == 'POST':
        key = request.form.get('key')
        if key is None or key.strip() == "":
            return render_template('error.html', error =  "Some problem with your key")
        else:
            session['_key'] = request.form.get("key")
            return redirect(url_for('decoded'))
    else:
        return render_template('decode.html')

    
@app.route("/decoded",methods=['GET'])
def decoded():
    fileName = session.get('_imgname')
    key = session.get('_key')
    
    text = steganography.decode(("uploads/"+fileName),key)
    os.remove(("uploads/"+fileName))
    return render_template('decoded.html',decoded_phrase=text)


@app.route('/encrypt',methods=["GET","POST"])
def encrypt():
    if request.method == "POST":  
        text = request.form.get('text')
        if text is None or text.strip() == "":
            return render_template('error.html', error = "You haven`t written the text")
            
          
        else:
            session['_text'] = request.form.get("text")
            return redirect(url_for("encrypted"))
            
    else:
        return render_template('encrypt.html')
      

@app.route('/encrypted',methods=['GET'])
def encrypted():
    name = session.get('_imgname')
    text = session.get('_text')
    key = steganography.encryption(('uploads/'+str(name)),text,name,'uploads/')
    return render_template('encrypted.html',ret_paswd=key)

@app.route('/email', methods=["POST"])
def sendMail():
    if request.method == 'POST':
        name = session.get('_imgname')
        email = request.form['email']
        # File path
        filename = 'uploads/'+ name

        msg = Message('Sending File', sender='private.kosinsky@gmail.com', recipients=[email])
        msg.body = 'Your encrypted image'
        with app.open_resource(filename) as fp:
            msg.attach(filename, 'application/octet-stream', fp.read())

        mail.send(msg)
        os.remove(filename)
        return render_template('end.html', result ='Email sent successfully')


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()

