import pymysql  # import pymsql to install on the current project
from werkzeug.utils import secure_filename
import os
from os.path import join, dirname, realpath

# flask-framework ,#Flask-python class
from flask import Flask, render_template, flash, redirect, request, session

app = Flask(__name__)  # we create a flask application parsing its name
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/?>'  # used in encrypting the session

#saving files in the database
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')

#specify allowed extensions
ALLOWED_EXTENSIONS = set(['epub', 'pdf', 'txt'])

#configure upload folder in the app

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 3*1024*1024

#CHECK IF FILENAME UPLOADED MEETS ALLOWED EXTENSIONS


def allowed_file(filename):
    return '.'in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# establish db connection
con = pymysql.connect("localhost", "root", "", "library")
cursor = con.cursor()  # execute sql -create a cursor object to execute sql


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/books')
def books():
    sql = "SELECT * FROM `books` ORDER BY `title` DESC"

    cursor.execute(sql)  # EXECUTE SQL

    #count the returned rows
    if cursor.rowcount < 1:
        return render_template('books.html', msg=" no books available")
    else:
        rows = cursor.fetchall()
    print(rows)
    #send the rows to the presentation layer,your html
    return render_template('books.html', rows=rows)


#route for book add
@app.route('/addbooks', methods=['POST', 'GET'])
def addbooks():  # logic goes her
    #handle form data

     if request.method == 'POST':  # check if user posted something
         title = request.form['title']
         author = request.form['author']
         genre = request.form['genre']
         description = request.form['description']
         file = request.files['file']  # receives file
         # #check if file is present and allowed
         if file and allowed_file(file.filename):
             filename = secure_filename(file.filename)
             #saves the file and its filename
             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
             #once the file is saved, save the link to database0

         #validation
         if title == "":
             return render_template('books.html', msg1="title field is empty")
             #flash("email field is empty")

         if author == "":
             #flash("name field is empty")
             return render_template('books.html', msg2="author field is empty")
         if file == "":
             #flash("name field is empty")

             return render_template('books.html', msg3="book field is empty")

         else:
             # establish db connection
             con = pymysql.connect("localhost", "root", "", "library")
             cursor = con.cursor()  # execute sql -create a cursor object to execute sql
             #save the three ``fields to the database
             # %s protects data .
             sql = "INSERT INTO `books`(`title`,`author`,`description`, `file`, `genre`) VALUES (%s,%s,%s, %s, %s)"
             try:

                cursor.execute(
                    sql, (title, author, description, filename, genre))
                con.commit()  # commits the changes to the db
                return render_template('books.html', msg="add successful")

             except:
               con.rollback()
     else:
         return redirect("/books")

#book display function


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':

        title = request.form['title']

        con = pymysql.connect("localhost", "root", "", "library")
        cursor = con.cursor()

        sql = "SELECT * FROM `books` WHERE `title` LIKE  '%%%s%%' "
        cursor.execute(sql, (title))

        #check if cursor has zero rows
        if cursor.rowcount == 0:
            return render_template('books.html', msg="no book with that title found")
        else:
            rows = cursor.fetchall()
            return render_template('books.html', rows=rows)
    else:
        return render_template('books.html')


#registration


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        con = pymysql.connect("localhost", "root", "", "library")
        cursor = con.cursor()

        sql = "INSERT INTO `registration`(`username`,`email`,`password`) VALUES (%s,%s,%s)"
        try:
            cursor.execute(sql, (username, email, password))
            con.commit()
            return render_template('home.html', message="welcome")
        except:
            con.rollback()
    else:
        return render_template('registration.html')
#login route


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        con = pymysql.connect("localhost", "root", "", "library")
        cursor = con.cursor()
        sql = "SELECT * FROM `registration` where `username`=%s and `password`=%s"

        #execute sql using the cursor object
        cursor.execute(sql, (username, password))
        #check if a match was found or not
        if cursor.rowcount == 0:
            return render_template("login.html", msg1="No match .Wrong input")
        elif cursor.rowcount == 1:
            # create a session for the user
            #we store username in session variable, you dont store password in session

            session['userkey'] = username

            return redirect('/books')
        elif cursor.rowcount > 1:
            return render_template('login.html', msg1="try again later")
        else:
            return render_template('login.html', msg1="contact admin")

    else:
        #shows login page, after the route is visited
        return render_template('login.html')

#logout


@app.route('/logout')
def logout():
    session.pop('userkey', None)
    return redirect('login')


if __name__ == '__main__':
    app.run()
