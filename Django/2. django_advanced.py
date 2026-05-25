# ============================================================
# Django Advanced - Learning File
# Topics: Admin & Forms, Django REST Framework, Authentication
# ============================================================

# IMPORTANT NOTE:
# Just like the basics file, this is a "simulated" Django project.
# The code here is written in one file for easy revision, but in reality,
# it would be split across models.py, admin.py, forms.py, serializers.py, etc.

from django.db import models
from django.contrib import admin
from django import forms
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect

# Pretend we are using Django REST Framework (DRF)
# pip install djangorestframework
from rest_framework import serializers, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


# ============================================================
# TOPIC 1: DJANGO AUTHENTICATION (Built-in Auth & Custom Users)
# Location: myapp/models.py & myapp/views.py
# ============================================================

# --- 1A. Custom User Model (models.py) ---
# It is a Django BEST PRACTICE to ALWAYS create a custom user model 
# when starting a new project, even if you don't need extra fields right away.
class CustomUser(AbstractUser):
    # AbstractUser already gives us username, password, email, first_name, last_name
    # But now we can add our own custom fields!
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    def __str__(self):
        return self.username

# (Note: In settings.py, you must tell Django to use this model: 
# AUTH_USER_MODEL = 'myapp.CustomUser')


# --- 1B. Permissions and Groups (views.py) ---
# Django has a built-in permissions system. You can assign permissions to individual users,
# or create 'Groups' (like 'Editors' or 'Managers') and assign permissions to the group.

@login_required(login_url='/login/') # Redirects to login if not authenticated
def dashboard_view(request):
    # We can access the logged-in user via request.user
    return render(request, 'dashboard.html', {'user': request.user})

@permission_required('myapp.add_article', raise_exception=True)
def create_article_view(request):
    # Only users with the 'add_article' permission can access this view
    # If they don't have it, Django raises a 403 Forbidden error.
    return render(request, 'create_article.html')

# (To assign a user to a group in code:)
# managers_group = Group.objects.get(name='Managers')
# request.user.groups.add(managers_group)


# ============================================================
# TOPIC 2: DJANGO ADMIN AND FORMS
# Location: myapp/admin.py & myapp/forms.py
# ============================================================

# Let's create a simple Product model to demonstrate Admin and Forms
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    product_image = models.FileField(upload_to='product_docs/') # File uploads
    is_active = models.BooleanField(default=True)

# --- 2A. Customizing Django Admin (admin.py) ---
# The Django Admin panel is a huge selling point. We can customize exactly how
# our models look and behave inside the admin interface.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Columns to show in the list view
    list_display = ('name', 'price', 'is_active')
    
    # Add filters to the right sidebar
    list_filter = ('is_active',)
    
    # Add a search bar at the top
    search_fields = ('name', 'description')
    
    # Make fields editable directly from the list view!
    list_editable = ('price', 'is_active')


# --- 2B. Django Forms & File Uploads (forms.py) ---
# Django Forms handle HTML generation, validation, and security (CSRF) automatically.
# 'ModelForm' is magic: it builds a form directly from a database model!

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Which fields should be in the form?
        fields = ['name', 'price', 'description', 'product_image']
        
    # Custom Validation!
    # Django automatically looks for methods named clean_<fieldname>
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            # This error will show up right next to the price field in HTML
            raise forms.ValidationError("Price must be greater than zero.")
        return price


# --- 2C. Handling the Form in a View (views.py) ---
def add_product_view(request):
    if request.method == 'POST':
        # request.FILES is required when handling file/image uploads!
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid(): # This runs our 'clean_price' method
            # form.save() automatically creates and saves the Product to the database!
            form.save()
            return redirect('product_list')
    else:
        # If it's a GET request, just show an empty form
        form = ProductForm()
        
    # In HTML, you must include enctype="multipart/form-data" in the <form> tag for file uploads!
    return render(request, 'add_product.html', {'form': form})


# ============================================================
# TOPIC 3: DJANGO REST FRAMEWORK (DRF)
# Location: myapp/serializers.py & myapp/views.py (or api.py)
# ============================================================

# DRF is a powerful toolkit for building Web APIs in Django.
# It handles JSON conversion, complex validation, and API authentication.

# --- 3A. Serializers (serializers.py) ---
# Serializers translate Django Models into JSON (and vice versa).
# They act exactly like Django Forms, but for APIs!

class ProductSerializer(serializers.ModelSerializer):
    # We can add custom fields that aren't in the database
    tax_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'tax_amount', 'is_active']
        
    # Method to calculate our custom 'tax_amount' field
    def get_tax_amount(self, obj):
        return round(float(obj.price) * 0.15, 2) # 15% tax


# --- 3B. API Endpoints - Function Based (views.py) ---
# A simple function-based API view

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated]) # Require authentication!
def product_api_list(request):
    if request.method == 'GET':
        products = Product.objects.filter(is_active=True)
        # many=True because we are serializing a LIST of objects
        serializer = ProductSerializer(products, many=True)
        # Response automatically turns the dictionary into JSON
        return Response(serializer.data)
        
    elif request.method == 'POST':
        # Pass the incoming JSON data to the serializer
        serializer = ProductSerializer(data=request.data)
        
        # is_valid() checks data types and model constraints
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201) # 201 Created
        # If invalid, automatically return the error messages
        return Response(serializer.errors, status=400) # 400 Bad Request


# --- 3C. API Endpoints - ViewSets (views.py) ---
# ViewSets are pure magic. They automatically provide GET, POST, PUT, PATCH, 
# and DELETE endpoints for a model in just a few lines of code!

class ProductViewSet(viewsets.ModelViewSet):
    # What data should it use?
    queryset = Product.objects.all()
    # How should it convert the data to JSON?
    serializer_class = ProductSerializer
    # Who is allowed to use this API? (e.g., Only logged-in users)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# (In urls.py, you would use a 'Router' to automatically generate all the URLs
# for the ProductViewSet: router.register(r'products', ProductViewSet) )


# ============================================================
# QUICK RECAP - What I learned in this file:
# ============================================================
#
# 1. CUSTOM USER MODEL:
#    Always inherit from `AbstractUser` at the start of a project to easily 
#    add fields like `bio` or `avatar` later.
#
# 2. PERMISSIONS:
#    Use `@login_required` or `@permission_required` to protect views.
#    Users can be grouped (e.g., 'Editors') for easier permission management.
#
# 3. DJANGO ADMIN:
#    Use `@admin.register(Model)` and `list_display`, `search_fields`, 
#    and `list_filter` to build a powerful back-office dashboard in minutes.
#
# 4. FORMS & FILES:
#    `ModelForm` automatically generates HTML forms from models.
#    Custom validation happens in `clean_<fieldname>()`.
#    ALWAYS pass `request.FILES` to the form if uploading images/files.
#
# 5. DJANGO REST FRAMEWORK (DRF):
#    - `Serializers`: Convert Django Models to JSON (and validate JSON back to models).
#    - `@api_view`: Decorator to make standard function APIs.
#    - `ModelViewSet`: Magically creates full CRUD APIs (List, Create, Retrieve, Update, Destroy).
#    - `permissions`: Easy way to block unauthorized API access.
# ============================================================
