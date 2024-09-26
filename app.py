from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATA_FOLDER = os.path.join(os.getcwd(), 'data')

#  read CSV 
def read_csv(filename):
    with open(os.path.join(DATA_FOLDER, filename), mode='r') as file:
        return list(csv.reader(file))

# write to CSV
def write_csv(filename, data):
    with open(os.path.join(DATA_FOLDER, filename), mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = read_csv('users.csv')

        for user in users[1:]: 
            if user[1] == email and user[2] == password:
                return redirect(url_for('dashboard'))
        flash('Invalid email or password.')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        write_csv('users.csv', [name, email, password])
        return redirect(url_for('success'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    courses = read_csv('courses.csv')
    return render_template('dashboard.html', courses=courses[1:])

@app.route('/consultation', methods=['GET', 'POST'])
def consultation():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        time = request.form['time']
        write_csv('bookings.csv', [name, email, date, time])
        return redirect(url_for('success'))
    return render_template('consultation.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        course_title = request.form['course_title']
        course_desc = request.form['course_desc']
        course_url = request.form['course_url']
        write_csv('courses.csv', [len(read_csv('courses.csv')) + 1, course_title, course_desc, course_url])
    courses = read_csv('courses.csv')
    return render_template('admin.html', courses=courses[1:])  

@app.route('/course/<int:course_id>')
def course_details(course_id):
    courses = read_csv('courses.csv')
    course = courses[course_id] if 0 < course_id < len(courses) else None
    return render_template('course_details.html', course=course)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        # Profile editing 
        flash('Profile updated successfully.')
    return render_template('edit_profile.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@app.route('/course/<course_name>')
def video_list(course_name):
    # Dummy data 
    videos = [
        {
            'title': 'Introduction to ' + course_name,
            'description': 'Learn the basics of ' + course_name + ' in this video.',
            'thumbnail_url': 'https://via.placeholder.com/300x200',
            'video_url': 'https://example.com/video1'
        },
        {
            'title': 'Advanced ' + course_name,
            'description': 'Dive deep into advanced concepts of ' + course_name + '.',
            'thumbnail_url': 'https://via.placeholder.com/300x200',
            'video_url': 'https://example.com/video2'
        }
    ]
    return render_template('video_list.html', course=course_name, videos=videos)


if __name__ == '__main__':
    app.run(debug=True)
