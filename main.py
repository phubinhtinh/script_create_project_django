import os
import zipfile
import subprocess
import shutil
from pathlib import Path

def create_django_project():
    """Tạo project Django hoàn chỉnh"""
    
    # Tên project
    project_name = "MySite"
    
    # Tạo thư mục tạm
    temp_dir = Path("temp_project")
    temp_dir.mkdir(exist_ok=True)
    
    try:
        print("🔄 Đang tạo project Django...")
        
        # Chạy lệnh startproject
        subprocess.run([
            "django-admin", "startproject", project_name
        ], cwd=temp_dir, check=True)
        
        project_path = temp_dir / project_name
        
        # Chạy lệnh startapp
        subprocess.run([
            "python", "manage.py", "startapp", "main"
        ], cwd=project_path, check=True)
        
        # Tạo thư mục templates
        (project_path / "main/templates/main").mkdir(parents=True, exist_ok=True)
        
        print(" Project được tạo thành công!")
        print("📁 Đang cấu hình files...")
        
        # Cấu hình settings.py
        configure_settings(project_path)
        
        # Cấu hình main/urls.py
        create_main_urls(project_path)
        
        # Cấu hình main/views.py
        configure_main_views(project_path)
        
        # Cấu hình main/models.py
        configure_main_models(project_path)
        
        # Cấu hình main/admin.py
        configure_main_admin(project_path)
        
        # Cấu hình MySite/urls.py
        configure_project_urls(project_path)
        
        # Tạo template home.html
        create_home_template(project_path)
        
        print(" Tất cả files đã được cấu hình!")
        
        # Chạy migrations
        print("🔄 Đang chạy migrations...")
        subprocess.run(["python", "manage.py", "makemigrations"], cwd=project_path, check=True)
        subprocess.run(["python", "manage.py", "migrate"], cwd=project_path, check=True)
        
        # Tạo dữ liệu mẫu
        create_sample_data(project_path)
        
        # Tạo file ZIP
        create_zip(project_path, project_name)
        
        print(f"🎉 Project '{project_name}' đã được tạo thành công!")
        print(f"📦 File ZIP: {project_name}.zip")
        print("\n🚀 Hướng dẫn sử dụng:")
        print("1. Giải nén file ZIP")
        print("2. cd MySite")
        print("3. python manage.py runserver")
        print("4. Truy cập: http://127.0.0.1:8000/")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi tạo project: {e}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
    finally:
        # Dọn dẹp thư mục tạm
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

def configure_settings(project_path):
    """Cấu hình settings.py"""
    settings_path = project_path / "MySite" / "settings.py"
    
    settings_content = '''import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key-change-in-production'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MySite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MySite.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'vi-vn'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
'''
    
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(settings_content)

def create_main_urls(project_path):
    """Tạo main/urls.py"""
    urls_path = project_path / "main" / "urls.py"
    
    urls_content = '''from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),
]
'''
    
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(urls_content)

def configure_main_views(project_path):
    """Cấu hình main/views.py"""
    views_path = project_path / "main" / "views.py"
    
    views_content = '''from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

def home_page(request):
    posts = Post.objects.all().order_by('-created_at')[:5]
    
    context = {
        'posts': posts,
        'title': 'Trang chủ MySite',
        'description': 'Chào mừng đến với website Django của bạn!',
        'total_posts': Post.objects.count()
    }
    return render(request, 'main/home.html', context)

def about_page(request):
    context = {
        'title': 'Giới thiệu',
        'description': 'Website được xây dựng bằng Django'
    }
    return render(request, 'main/about.html', context)
'''
    
    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(views_content)

def configure_main_models(project_path):
    """Cấu hình main/models.py"""
    models_path = project_path / "main" / "models.py"
    
    models_content = '''from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Bài viết"
        verbose_name_plural = "Các bài viết"
        ordering = ['-created_at']
'''
    
    with open(models_path, 'w', encoding='utf-8') as f:
        f.write(models_content)

def configure_main_admin(project_path):
    """Cấu hình main/admin.py"""
    admin_path = project_path / "main" / "admin.py"
    
    admin_content = '''from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'is_published']
    list_filter = ['created_at', 'is_published']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'
    list_editable = ['is_published']
'''
    
    with open(admin_path, 'w', encoding='utf-8') as f:
        f.write(admin_content)

def configure_project_urls(project_path):
    """Cấu hình MySite/urls.py"""
    urls_path = project_path / "MySite" / "urls.py"
    
    urls_content = '''from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]
'''
    
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(urls_content)

def create_home_template(project_path):
    """Tạo template home.html"""
    template_path = project_path / "main" / "templates" / "main" / "home.html"
    
    home_content = '''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            line-height: 1.6;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px; 
        }
        .header { 
            background: rgba(255,255,255,0.1); 
            backdrop-filter: blur(10px);
            color: white; 
            padding: 60px 20px; 
            text-align: center; 
            border-radius: 20px;
            margin-bottom: 40px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        }
        .header h1 { font-size: 3.5rem; margin-bottom: 10px; }
        .header p { font-size: 1.3rem; opacity: 0.9; }
        .stats { 
            display: flex; 
            justify-content: center; 
            gap: 30px; 
            margin-top: 30px; 
        }
        .stat-item { 
            background: rgba(255,255,255,0.2); 
            padding: 20px; 
            border-radius: 15px; 
            text-align: center; 
            min-width: 120px;
        }
        .stat-number { font-size: 2rem; font-weight: bold; color: #fff; }
        .stat-label { color: rgba(255,255,255,0.8); font-size: 0.9rem; }
        .posts-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
            gap: 25px; 
            margin-top: 40px; 
        }
        .post-card { 
            background: rgba(255,255,255,0.95); 
            padding: 25px; 
            border-radius: 20px; 
            box-shadow: 0 10px 40px rgba(0,0,0,0.1); 
            transition: all 0.3s ease; 
            border: 1px solid rgba(255,255,255,0.2);
        }
        .post-card:hover { 
            transform: translateY(-10px); 
            box-shadow: 0 20px 60px rgba(0,0,0,0.15); 
        }
        .post-title { 
            color: #333; 
            font-size: 1.4rem; 
            margin-bottom: 15px; 
            line-height: 1.3; 
        }
        .post-content { 
            color: #666; 
            line-height: 1.7; 
            margin-bottom: 15px; 
        }
        .post-meta { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            color: #888; 
            font-size: 0.9rem; 
        }
        .no-posts { 
            text-align: center; 
            color: rgba(255,255,255,0.8); 
            padding: 80px 20px; 
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        @media (max-width: 768px) {
            .header h1 { font-size: 2.5rem; }
            .stats { flex-direction: column; align-items: center; }
            .posts-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ title }}</h1>
            <p>{{ description }}</p>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">{{ total_posts }}</div>
                    <div class="stat-label">Bài viết</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">100%</div>
                    <div class="stat-label">Hoạt động</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">24/7</div>
                    <div class="stat-label">Online</div>
                </div>
            </div>
        </div>
        
        {% if posts %}
            <div class="posts-grid">
                {% for post in posts %}
                <div class="post-card">
                    <h3 class="post-title">{{ post.title }}</h3>
                    <p class="post-content">{{ post.content|truncatewords:25 }}</p>
                    <div class="post-meta">
                        <span>📅 {{ post.created_at|date:"d/m/Y H:i" }}</span>
                        <span>👁️ {{ post.id }} views</span>
                    </div>
                </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="no-posts">
                <h2>🎉 Chào mừng!</h2>
                <p>Website của bạn đã sẵn sàng. Hãy thêm bài viết đầu tiên qua <a href="/admin/" style="color: #4CAF50; text-decoration: none;">Admin Panel</a></p>
            </div>
        {% endif %}
    </div>
</body>
</html>
'''
    
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(home_content)
    
    # Tạo template about.html
    about_path = project_path / "main" / "templates" / "main" / "about.html"
    about_content = '''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body { 
            font-family: 'Segoe UI', sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: rgba(255,255,255,0.95); 
            padding: 40px; 
            border-radius: 20px; 
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        }
        h1 { 
            color: #333; 
            text-align: center; 
            margin-bottom: 30px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }
        .info-card {
            background: #f8f9ff;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            border-left: 5px solid #667eea;
        }
        .info-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ title }}</h1>
        <p style="text-align: center; color: #666; font-size: 1.1rem; line-height: 1.7;">
            {{ description }}
        </p>
        
        <div class="info-grid">
            <div class="info-card">
                <div class="info-icon">⚡</div>
                <h3>Tốc độ cao</h3>
                <p>Được xây dựng với Django - Framework Python mạnh mẽ nhất</p>
            </div>
            <div class="info-card">
                <div class="info-icon">🔒</div>
                <h3>An toàn</h3>
                <p>Hệ thống bảo mật hoàn chỉnh với CSRF protection</p>
            </div>
            <div class="info-card">
                <div class="info-icon">📱</div>
                <h3>Responsive</h3>
                <p>Thiết kế đẹp mắt trên mọi thiết bị</p>
            </div>
            <div class="info-card">
                <div class="info-icon">⚙️</div>
                <h3>Dễ mở rộng</h3>
                <p>Cấu trúc chuẩn Django, dễ dàng thêm tính năng mới</p>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 40px; padding-top: 30px; border-top: 1px solid #eee;">
            <p><strong>👨‍💻 Được tạo bởi:</strong> Django Developer</p>
            <p><em>Ngày tạo: {{ current_date }}</em></p>
        </div>
    </div>
</body>
</html>
'''
    
    with open(about_path, 'w', encoding='utf-8') as f:
        f.write(about_content)

def create_sample_data(project_path):
    """Tạo dữ liệu mẫu"""
    sample_data_script = '''from main.models import Post
from django.utils import timezone
from datetime import timedelta

# Xóa dữ liệu cũ
Post.objects.all().delete()

# Tạo dữ liệu mẫu
sample_posts = [
    {
        'title': 'Chào mừng đến với MySite!',
        'content': 'Website của bạn đã được tạo thành công với Django. Bạn có thể bắt đầu thêm nội dung ngay bây giờ.',
        'is_published': True
    },
    {
        'title': 'Django - Framework mạnh mẽ',
        'content': 'Django là một framework web Python cấp cao giúp phát triển nhanh chóng và thực tế. Nó khuyến khích việc phát triển nhanh chóng và thiết kế sạch sẽ.',
        'is_published': True
    },
    {
        'title': 'Hướng dẫn sử dụng Admin',
        'content': 'Để quản lý nội dung, hãy truy cập /admin/ và đăng nhập với tài khoản superuser. Bạn có thể tạo, sửa, xóa các bài viết dễ dàng.',
        'is_published': True
    }
]

for post_data in sample_posts:
    Post.objects.create(**post_data)

print(f" Đã tạo {len(sample_posts)} bài viết mẫu!")
'''
def create_zip(project_path, project_name):
    """Tạo file ZIP"""
    zip_filename = f"{project_name}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, project_path)
                zipf.write(file_path, arcname)
    
    print(f"📦 File ZIP đã được tạo: {zip_filename}")
    print(f"📊 Kích thước: {os.path.getsize(zip_filename) / 1024:.1f} KB")

if __name__ == "__main__":
    create_django_project()