# ============================================================
# Django Basics - Learning File
# Topics: Architecture, Models/ORM, Views & Templates
# ============================================================

# IMPORTANT NOTE FOR LEARNING:
# Django is usually split across many files and folders (Project vs App).
# To follow your "Single File" learning rule, this file contains the code 
# you WOULD write in different Django files. 
# I have labeled each section so you know exactly where this code 
# belongs in a real Django project.


# ============================================================
# TOPIC 1: DJANGO ARCHITECTURE & STRUCTURE
# ============================================================

"""
1. The MTV Pattern (Model-Template-View)
   - Model: Handles the database (data logic).
   - Template: Handles the HTML/UI (presentation logic).
   - View: The middleman. It gets data from the Model and passes it to the Template.
   (It's like MVC, but Django calls the controller a "View" and the view a "Template").

2. Projects vs Apps
   - Project: The entire website (e.g., An E-commerce site). Created with: `django-admin startproject myproject`
   - App: A specific feature within the site (e.g., Blog, Store, Forum). Created with: `python manage.py startapp myapp`

3. Standard Project Structure:
   myproject/
   ├── manage.py           <- Command-line utility (runserver, makemigrations)
   ├── myproject/          <- Project configuration folder
   │   ├── settings.py     <- Global settings (DB config, installed apps)
   │   └── urls.py         <- Main URL router
   └── myapp/              <- Your App folder
       ├── models.py       <- Database tables
       ├── views.py        <- Logic (FBVs, CBVs)
       ├── urls.py         <- App-specific URL router
       └── templates/      <- HTML files
"""


# ============================================================
# TOPIC 2: MODELS AND ORM (Database Stuff)
# Location: myapp/models.py
# ============================================================
# Django uses an ORM (Object-Relational Mapper) just like SQLAlchemy,
# but it's built-in and heavily integrated.

from django.db import models

# 1. Defining Models and Fields
class Author(models.Model):
    # Django automatically adds an 'id' primary key field.
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    joined_date = models.DateField(auto_now_add=True) # Automatically sets to today when created

    def __str__(self):
        # This controls what shows up in the Django Admin panel
        return self.name

# 2. Creating Relationships
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # ForeignKey = Many-to-One relationship. (Many articles can have ONE author)
    # on_delete=models.CASCADE means if the Author is deleted, delete their articles too.
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='articles')
    
    # ManyToManyField = Many-to-Many relationship. (An article can have many tags, and vice versa)
    # tags = models.ManyToManyField(Tag) (Assuming a Tag model existed)

    def __str__(self):
        return self.title

"""
3. DJANGO ORM QUERIES (How to use the models above)
   Normally, you write these inside your views, or test them in the `python manage.py shell`.

   CREATE:
   author = Author.objects.create(name="Alice", email="alice@example.com")
   article = Article.objects.create(title="Learn Django", content="...", author=author)

   READ (All):
   all_authors = Author.objects.all()

   READ (Filter):
   # Get all articles where the title contains 'Django' (case-insensitive)
   django_articles = Article.objects.filter(title__icontains="Django")

   READ (Single):
   # Get throws an error if it doesn't exist or finds more than one
   alice = Author.objects.get(name="Alice")

   UPDATE:
   alice.name = "Alice Smith"
   alice.save()

   DELETE:
   alice.delete()
   
   FOLLOWING RELATIONSHIPS:
   # Because we used related_name='articles' in the ForeignKey:
   alices_articles = alice.articles.all()
"""


# ============================================================
# TOPIC 3: VIEWS AND TEMPLATES
# Location: myapp/views.py
# ============================================================
# Views handle the HTTP requests. There are two ways to write them in Django:
# 1. Function-Based Views (FBV) - Simple, explicit, good for beginners.
# 2. Class-Based Views (CBV) - Reusable, less code, uses inheritance.

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

# --- 1. Function-Based View (FBV) ---
def article_list_fbv(request):
    # Step 1: Query the database
    articles = Article.objects.all()
    
    # Step 2: Create a context dictionary (data passed to the template)
    context = {
        'articles': articles,
        'page_title': 'Latest News'
    }
    
    # Step 3: Render the template
    return render(request, 'myapp/article_list.html', context)

def article_detail_fbv(request, article_id):
    # get_object_or_404 is a handy shortcut just like in Flask!
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'myapp/article_detail.html', {'article': article})


# --- 2. Class-Based View (CBV) ---
# This does the EXACT SAME thing as 'article_list_fbv' above, but in 2 lines of code!
class ArticleListView(ListView):
    # Django automatically queries Article.objects.all()
    # and passes it to the template named 'myapp/article_list.html' as 'object_list'
    model = Article
    template_name = 'myapp/article_list.html'
    context_object_name = 'articles' # Renaming it from 'object_list' to 'articles'

class ArticleDetailView(DetailView):
    # Django automatically grabs the ID from the URL, queries the DB,
    # and passes it to 'myapp/article_detail.html'
    model = Article


# ============================================================
# TOPIC 4: URL ROUTING
# Location: myapp/urls.py
# ============================================================
# How do we connect URLs to those views?

from django.urls import path
# In a real file, you would import views: from . import views

urlpatterns = [
    # FBV routing
    path('fbv/articles/', article_list_fbv, name='fbv_list'),
    path('fbv/articles/<int:article_id>/', article_detail_fbv, name='fbv_detail'),
    
    # CBV routing (You must call .as_view() on classes)
    path('cbv/articles/', ArticleListView.as_view(), name='cbv_list'),
    path('cbv/articles/<int:pk>/', ArticleDetailView.as_view(), name='cbv_detail'),
]


# ============================================================
# TOPIC 5: DJANGO TEMPLATE LANGUAGE (DTL)
# Location: myapp/templates/myapp/article_list.html
# ============================================================
# DTL looks VERY similar to Jinja2 (used in Flask).
# It uses {{ variables }} and {% logic tags %}.

HTML_TEMPLATE_EXAMPLE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ page_title }}</title>
</head>
<body>
    <h1>{{ page_title }}</h1>
    
    <ul>
        <!-- Looping through the 'articles' context variable -->
        {% for article in articles %}
            <li>
                <!-- We can follow relationships in templates using dot notation -->
                <h2>{{ article.title }}</h2>
                <p>By: {{ article.author.name }}</p>
                
                <!-- DTL filters use the pipe character | -->
                <p>{{ article.content|truncatewords:30 }}</p>
                
                <!-- Using Django's built-in url tag to generate links -->
                <a href="{% url 'fbv_detail' article.id %}">Read More</a>
            </li>
        {% empty %}
            <!-- This runs if the articles list is empty! -->
            <li>No articles published yet.</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

# ============================================================
# QUICK RECAP - What I learned in this file:
# ============================================================
#
# 1. MTV PATTERN:
#    Models (Database) <-> Views (Logic) <-> Templates (UI).
#
# 2. PROJECTS vs APPS:
#    Project = The whole website. App = A specific feature (Blog, Store).
#
# 3. MODELS & ORM:
#    Define classes extending `models.Model`.
#    Relationships use `ForeignKey` (1-to-many) or `ManyToManyField`.
#    ORM: `Model.objects.all()`, `.filter()`, `.get()`, `.create()`.
#
# 4. VIEWS (FBV vs CBV):
#    FBV: `def my_view(request): return render(...)` (Good for learning/complex logic)
#    CBV: `class MyView(ListView): model = MyModel` (Good for quick, standard tasks)
#
# 5. TEMPLATES:
#    Uses DTL (Django Template Language). Extremely similar to Jinja2.
#    `{% for x in y %}` and `{{ variable|filter }}`.
# ============================================================
