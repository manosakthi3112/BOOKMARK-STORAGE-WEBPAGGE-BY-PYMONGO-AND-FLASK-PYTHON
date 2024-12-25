from flask import Flask, render_template, request, redirect, url_for, session
from urllib.parse import quote_plus
import pymongo

app = Flask(__name__)
app.secret_key = "3112"  

username = "manot6114"
password = "vOqJN4bEV7KEMxq7"
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

myclient = pymongo.MongoClient("mongodb+srv://{encoded_username}:{encoded_password}@project1.z0gbb.mongodb.net/?retryWrites=true&w=majority&appName=project1")
mydb = myclient["link"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['GET', 'POST'])
def check():
    try:
        if request.method == "POST":
            result = request.form.get('fname')
            session['result'] = result  
        else:
            result = session.get('result')  
        
        if not result:
            return redirect(url_for('index'))  

        mycol = mydb[result]
        data = list(mycol.find())
        print(data)
        return render_template('base.html', data=data)
    except Exception as e:
        print(f"Error in check route: {e}")
        return render_template('index.html', error="error")

@app.route('/add', methods=['GET', 'POST'])
def add():
    try:
        if request.method == "POST":
            return render_template('page.html')
    except Exception as e:
        print(f"Error in add route: {e}")
        return render_template('index.html', error="error")

@app.route('/insert', methods=['POST'])
def insert():
    try:
        result = session.get('result')  
        if not result:
            return redirect(url_for('index'))

        mycol = mydb[result]
        if result in mydb.list_collection_names():
            link_name = request.form.get('link_n')
            link_ = request.form.get('link')
            d = {'link_name': link_name, "link": link_}
            mycol.insert_one(d)
            return redirect(url_for('check')) 
        else:
            return render_template('page.html', error=" not exist.")
    except Exception as e:
        print(f"Error in insert route: {e}")
        return render_template('index.html', error="unexpected error")

@app.route('/delete', methods=['POST'])
def delete():
    try:
        result = session.get('result')
        if not result:
            return redirect(url_for('index'))

        link_name = request.form.get('name')
        mycol = mydb[result]
        delete_result = mycol.delete_one({"link_name": link_name})
        return redirect(url_for('check'))
    except Exception as e:
        return render_template('index.html', error="unexpected error ")

if __name__ == "__main__":
    port=int(os.environ.get("PORT",4000))
    app.run(host="0.0.0.0",debug=True, threaded=False,port=port)
