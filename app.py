
from flask import Flask ,render_template ,flash,redirect,request  #flask-framework ,#Flask-python class

app = Flask(__name__)
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#in flask we attach every function to a route so we use the route.

@app.route('/')
def home():
    return render_template('home.html')

#the application layer (business logic layer)

import pymysql    #import pymsql to install on the current project


con= pymysql.connect("localhost", "root", "", "library")    #establish db connection
cursor=con.cursor()  #execute sql -create a cursor object to execute sql

#book display function
@app.route( '/books')
def books():
    con=pymysql.connect("localhost", "root", "","library")
    cursor=con.cursor()

    sql= "SELECT * FROM `books` ORDER BY `title` DESC"
    #EXECUTE SQL
    cursor.execute(sql)

    #count the returned rows
    if cursor.rowcount < 1:
        return render_template('books.html', msg= " no books available")
    else:
        rows =cursor.fetchall()
        #send the rows to the presentation layer,your html
        return render_template('books.html', rows= rows)

#add a book
@app.route('/addbooks', methods=['POST','GET'])
def addbooks():  #logic goes her
    #handle form data
     if request.method=='POST': #check if user posted something
         title=request.form['title']
         author=request.form['author']
         genre = request.form['genre']
         book = request.form['book']
         description=request.form['description']

         #validation
         if title=="":
             return render_template('books.html', msg1="title field is empty")
             #flash("email field is empty")

         if author=="":
             #flash("name field is empty")
             return render_template('books.html', msg2="author field is empty")
         if book=="":
             #flash("name field is empty")

             return render_template('books.html', msg3="book field is empty")

         else:
             #save the three ``fields to the database
             sql= "INSERT INTO `books`(`title`,`author`,`description`, `book`, `genre`) VALUES (%s,%s,%s, %s, %s)"  # %s protects data .
             try:


                cursor.execute(sql,(title,author,description,book,genre))
                con.commit() #commits the changes to the db
                return redirect("/books" )

             except:
               con.rollback()
     else:
         return redirect("/books")


#route for book search
@app.route('/search' , methods=['POST','GET'])
def search():
    if request.method=='POST':

        title=request.form['title']
        genre=request.form['genre']
        con = pymysql.connect("localhost", "root", "", "library")
        cursor = con.cursor()

        sql= "SELECT * FROM books WHERE title=%s or author= %s ORDER BY  `name` desc "
        cursor.execute(sql,(title,genre))

        #check if cursor has zero rows
        if cursor.rowcount==0:
            return render_template('books.html',msg="no book with that title found")
        else:
            rows=cursor.fetchall()
            return render_template('books.html',rows=rows ,msg="match found")
    else:return render_template('books.html')


if __name__ == '__main__':
    app.run()
