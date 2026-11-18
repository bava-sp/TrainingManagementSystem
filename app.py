
from flask import Flask, render_template, request, redirect, send_from_directory
import os

app = Flask(__name__)

# Upload Folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads folder automatically
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# -----------------------------
# Login Data
# -----------------------------

users = {
    "admin": "1234",
    "employee": "emp123"
}

# -----------------------------
# Storage
# -----------------------------

syllabus = []
queries = []

# -----------------------------
# Home
# -----------------------------

@app.route('/')
def home():
    return render_template("login.html")

# -----------------------------
# Login
# -----------------------------

@app.route('/login', methods=['POST'])
def login():

    role = request.form['role']
    username = request.form['username']
    password = request.form['password']

    if role == "admin":

        if username == "admin" and password == "1234":
            return redirect('/admin')

        else:
            return "Invalid Admin Login"

    elif role == "employee":

        if username == "employee" and password == "emp123":
            return redirect('/employee')

        else:
            return "Invalid Employee Login"

# -----------------------------
# Admin Dashboard
# -----------------------------

@app.route('/admin')
def admin():
    return render_template(
        "admin.html",
        syllabus=syllabus,
        queries=queries
    )

# -----------------------------
# Add Syllabus
# -----------------------------

@app.route('/add', methods=['POST'])
def add():

    department = request.form['department']
    title = request.form['title']

    file = request.files['file']

    filename = file.filename

    file.save(
        os.path.join(
            app.config['UPLOAD_FOLDER'],
            filename
        )
    )

    syllabus.append({
        "department": department,
        "title": title,
        "file": filename
    })

    return redirect('/admin')

# -----------------------------
# View Uploaded File
# -----------------------------

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename
    )

# -----------------------------
# Delete
# -----------------------------

@app.route('/delete/<int:id>')
def delete(id):

    syllabus.pop(id)

    return redirect('/admin')

# -----------------------------
# Edit Page
# -----------------------------

@app.route('/edit/<int:id>')
def edit(id):

    item = syllabus[id]

    return render_template(
        "edit.html",
        item=item,
        id=id
    )

# -----------------------------
# Update
# -----------------------------

@app.route('/update/<int:id>', methods=['POST'])
def update(id):

    syllabus[id]['department'] = request.form['department']
    syllabus[id]['title'] = request.form['title']

    return redirect('/admin')

# -----------------------------
# Employee Dashboard
# -----------------------------

@app.route('/employee')
def employee():

    return render_template(
        "employee.html",
        syllabus=syllabus,
        queries=queries
    )

# -----------------------------
# Send Query
# -----------------------------

@app.route('/query', methods=['POST'])
def query():

    employee = request.form['employee']
    question = request.form['question']

    queries.append({
        "employee": employee,
        "question": question,
        "reply": ""
    })

    return redirect('/employee')

# -----------------------------
# Reply
# -----------------------------

@app.route('/reply/<int:id>', methods=['POST'])
def reply(id):

    queries[id]['reply'] = request.form['reply']

    return redirect('/admin')

# -----------------------------
# Run App
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
