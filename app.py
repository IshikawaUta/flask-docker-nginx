from flask import Flask, render_template, request, redirect, url_for, flash, redirect, url_for, Response
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
import cloudinary
import cloudinary.uploader
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from datetime import datetime

# Muat variabel lingkungan
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Filter kustom untuk memformat objek datetime
@app.template_filter('strftime')
def datetime_format(value, format_string):
    if not isinstance(value, datetime):
        return value
    return value.strftime(format_string)

# --- Konfigurasi ---
# MongoDB Atlas
client = MongoClient(os.getenv("MONGO_URI"))
db = client.portfolio_db
projects_collection = db['projects']
blog_collection = db['blogs']
contact_messages_collection = db['contacts']
reviews_collection = db['reviews']

# Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# BARU: Konfigurasi Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS').lower() in ('true', '1', 't')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
mail = Mail(app)

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id == os.getenv("ADMIN_USERNAME"):
        return User(os.getenv("ADMIN_USERNAME"))
    return None

# --- Rute Frontend ---

@app.route('/')
def index():
    latest_projects = list(db.projects.find().sort([('_id', -1)]).limit(3))

    return render_template('index.html', projects=latest_projects)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    per_page = 4
    try:
        page = int(request.args.get('page', 1))
    except (ValueError, TypeError):
        page = 1
    
    skip = (page - 1) * per_page
    total_projects = projects_collection.count_documents({})
    total_pages = (total_projects + per_page - 1) // per_page
    
    projects = list(projects_collection.find().skip(skip).limit(per_page))
    
    return render_template(
        'projects.html',
        projects=projects,
        page=page,
        total_pages=total_pages
    )

@app.route('/tools')
def tools():
    # Contoh data, bisa juga dari database
    tools_list = [
        {'name': 'Python', 'type': 'Bahasa Pemrograman'},
        {'name': 'Flask', 'type': 'Kerangka Kerja Web'},
        {'name': 'MongoDB', 'type': 'Basis Data'},
        {'name': 'Docker', 'type': 'Containerization'},
        {'name': 'JavaScript', 'type': 'Bahasa Pemrograman'},
        {'name': 'React', 'type': 'Library JavaScript'},
        {'name': 'Git', 'type': 'Version Control'},
        {'name': 'SQLAlchemy', 'type': 'ORM Python'},
        {'name': 'Nginx', 'type': 'Web Server'},
        {'name': 'Celery', 'type': 'Queue Tugas Terdistribusi'},
        {'name': 'PostgreSQL', 'type': 'Basis Data Relasional'},
        {'name': 'HTML', 'type': 'Bahasa Markup'},
        {'name': 'CSS', 'type': 'Lembar Gaya'},
        {'name': 'Bootstrap', 'type': 'Kerangka Kerja CSS'}
    ]
    return render_template('tools.html', tools=tools_list)

# Halaman Layanan Jasa
@app.route('/services')
def services():
    return render_template('services.html')

# Halaman Daftar Pesan Kontak
@app.route('/messages')
def messages():
    per_page = 10
    try:
        page = int(request.args.get('page', 1))
    except (ValueError, TypeError):
        page = 1
    
    skip = (page - 1) * per_page
    total_messages = contact_messages_collection.count_documents({})
    total_pages = (total_messages + per_page - 1) // per_page
    
    messages = list(contact_messages_collection.find().sort('dibuat_pada', -1).skip(skip).limit(per_page))
    
    return render_template(
        'messages.html',
        messages=messages,
        page=page,
        total_pages=total_pages
    )

# Halaman Detail Pesan
@app.route('/messages/<message_id>')
def message_detail(message_id):
    # Ambil pesan dari database berdasarkan ID
    message = contact_messages_collection.find_one({'_id': ObjectId(message_id)})
    if message:
        return render_template('message_detail.html', message=message)
    return "Pesan tidak ditemukan", 404

# Rute untuk halaman ulasan publik
@app.route('/reviews')
def reviews():
    reviews = list(reviews_collection.find().sort('created_at', -1))
    return render_template('reviews.html', reviews=reviews)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        db.contacts.insert_one({'name': name, 'email': email, 'message': message})

        try:
            sender_email = os.getenv('MAIL_USERNAME')
            msg = Message(subject=f'Pesan Baru dari Portofolio: {name}',
                          sender=sender_email,
                          recipients=[os.getenv('MAIL_DEFAULT_SENDER')],
                          body=f"Nama: {name}\nEmail: {email}\nPesan:\n{message}")
            mail.send(msg)
            flash('Pesan Anda berhasil terkirim!', 'success')
        except Exception as e:
            flash(f'Gagal mengirim email. Silakan coba lagi nanti. Error: {e}', 'danger')
            
        return redirect(url_for('contact'))
    return render_template('contact.html')

# --- Rute Blog Publik ---
@app.route('/blog')
def blog():
    per_page = 4
    try:
        page = int(request.args.get('page', 1))
    except (ValueError, TypeError):
        page = 1

    skip = (page - 1) * per_page
    total_posts = blog_collection.count_documents({})
    total_pages = (total_posts + per_page - 1) // per_page

    posts = list(blog_collection.find().sort('created_at', -1).skip(skip).limit(per_page))
    
    return render_template(
        'blog.html',
        blogs=posts,
        page=page,
        total_pages=total_pages
    )

@app.route('/blog/<blog_id>')
def blog_post(blog_id):
    blog_post = db.blogs.find_one({'_id': ObjectId(blog_id)})
    if not blog_post:
        return render_template('404.html'), 404
    return render_template('blog_post.html', blog_post=blog_post)

# --- Rute Admin ---

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Periksa username dan password dengan hash
        if username == os.getenv("ADMIN_USERNAME") and check_password_hash(os.getenv("ADMIN_PASSWORD_HASH"), password):
            user = User(username)
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Login gagal. Periksa kembali username dan password.', 'danger')
    return render_template('admin_login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    projects_list = list(db.projects.find())
    return render_template('admin_dashboard.html', projects=projects_list)

@app.route('/admin/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        technologies = [tech.strip() for tech in request.form.get('technologies').split(',')]
        demo_link = request.form.get('demo_link')  # BARU: Ambil link demo
        
        image_file = request.files['image']
        if image_file:
            upload_result = cloudinary.uploader.upload(image_file)
            image_url = upload_result['secure_url']
            
            db.projects.insert_one({
                'title': title,
                'description': description,
                'technologies': technologies,
                'image_url': image_url,
                'demo_link': demo_link  # BARU: Simpan link demo
            })
            flash('Proyek berhasil ditambahkan!', 'success')
            return redirect(url_for('admin_dashboard'))
    return render_template('add_project.html')

@app.route('/admin/edit_project/<project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = db.projects.find_one({'_id': ObjectId(project_id)})
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        technologies = [tech.strip() for tech in request.form.get('technologies').split(',')]
        demo_link = request.form.get('demo_link')  # BARU: Ambil link demo
        
        update_data = {
            'title': title,
            'description': description,
            'technologies': technologies,
            'demo_link': demo_link # BARU: Update link demo
        }
        
        image_file = request.files['image']
        if image_file:
            upload_result = cloudinary.uploader.upload(image_file)
            update_data['image_url'] = upload_result['secure_url']
            
        db.projects.update_one({'_id': ObjectId(project_id)}, {'$set': update_data})
        flash('Proyek berhasil diperbarui!', 'success')
        return redirect(url_for('admin_dashboard'))
        
    return render_template('edit_project.html', project=project)

@app.route('/admin/delete_project/<project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    db.projects.delete_one({'_id': ObjectId(project_id)})
    flash('Proyek berhasil dihapus!', 'success')
    return redirect(url_for('admin_dashboard'))

# --- Rute Blog Admin ---
@app.route('/admin/blog')
@login_required
def admin_blog_dashboard():
    blogs = list(db.blogs.find().sort([('created_at', -1)]))
    return render_template('admin_blog_dashboard.html', blogs=blogs)

@app.route('/admin/add_blog', methods=['GET', 'POST'])
@login_required
def add_blog():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = current_user.id
        
        db.blogs.insert_one({
            'title': title,
            'content': content,
            'author': author,
            'created_at': datetime.now()
        })
        flash('Blog berhasil ditambahkan!', 'success')
        return redirect(url_for('admin_blog_dashboard'))
    return render_template('add_blog.html')

@app.route('/admin/edit_blog/<blog_id>', methods=['GET', 'POST'])
@login_required
def edit_blog(blog_id):
    blog_post = db.blogs.find_one({'_id': ObjectId(blog_id)})
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        update_data = {
            'title': title,
            'content': content,
            'updated_at': datetime.now()
        }
        
        db.blogs.update_one({'_id': ObjectId(blog_id)}, {'$set': update_data})
        flash('Blog berhasil diperbarui!', 'success')
        return redirect(url_for('admin_blog_dashboard'))
    return render_template('edit_blog.html', blog_post=blog_post)

@app.route('/admin/delete_blog/<blog_id>', methods=['POST'])
@login_required
def delete_blog(blog_id):
    db.blogs.delete_one({'_id': ObjectId(blog_id)})
    flash('Blog berhasil dihapus!', 'success')
    return redirect(url_for('admin_blog_dashboard'))

# Rute Admin untuk mengelola ulasan
@app.route('/admin/reviews')
@login_required
def admin_reviews():
    reviews = list(reviews_collection.find().sort('created_at', -1))
    return render_template('admin_reviews.html', reviews=reviews)

@app.route('/admin/add_review', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        author = request.form.get('author')
        content = request.form.get('content')
        rating = int(request.form.get('rating'))
        
        reviews_collection.insert_one({
            'author': author,
            'content': content,
            'rating': rating,
            'created_at': datetime.now()
        })
        flash('Ulasan berhasil ditambahkan!', 'success')
        return redirect(url_for('admin_reviews'))
    return render_template('add_review.html')

@app.route('/admin/delete_review/<review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    reviews_collection.delete_one({'_id': ObjectId(review_id)})
    flash('Ulasan berhasil dihapus!', 'success')
    return redirect(url_for('admin_reviews'))

# Halaman Sitemap.xml
@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Menghasilkan sitemap.xml secara dinamis."""
    # Kumpulkan semua URL statis
    static_urls = [
        url_for('index', _external=True),
        url_for('about', _external=True),
        url_for('projects', _external=True),
        url_for('blog', _external=True),
        url_for('tools', _external=True),
        url_for('services', _external=True),
        url_for('reviews', _external=True),
        url_for('messages', _external=True),
        url_for('contact', _external=True)
    ]

    # Kumpulkan URL dinamis dari blog dan proyek
    dynamic_urls = []
    
    projects = projects_collection.find()
    for project in projects:
        dynamic_urls.append(url_for('projects', _external=True))
    
    posts = blog_collection.find()
    for post in posts:
        dynamic_urls.append(url_for('blog_post', blog_id=str(post['_id']), _external=True))
    
    # Gabungkan semua URL
    all_urls = list(set(static_urls + dynamic_urls)) # Gunakan set untuk menghindari duplikasi
    
    sitemap_xml = render_template('sitemap.xml', all_urls=all_urls)
    
    return Response(sitemap_xml, mimetype='application/xml')

# Halaman robots.txt
@app.route('/robots.txt')
def robots_txt():
    """Menghasilkan file robots.txt."""
    sitemap_url = url_for('sitemap', _external=True)
    return Response(
        f"""User-agent: *
Allow: /
Sitemap: {sitemap_url}""",
        mimetype='text/plain'
    )

# --- Jalankan Aplikasi ---
if __name__ == '__main__':
    app.run(debug=True)