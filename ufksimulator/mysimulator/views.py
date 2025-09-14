from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings


temporary_posts = []

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def insert_data(request):
    return render(request, 'insert_data.html')

def eu_parliament(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT name, seats FROM EU_Parties ORDER BY seats DESC;
        """)
        raw_parties = cursor.fetchall()

    # Mapeamento dos nomes para versões legíveis
    name_mapping = {
        "GUE_NGL": "The Left in the European Parliament - GUE/NGL",
        "S_D": "Progressive Alliance of Socialists & Democrats - S&D",
        "Greens_ALE": "Greens/European Free Alliance - EFA",
        "EPP": "European People's Party - EPP",
        "Renew_Europe": "Renew Europe",
        "ECR": "European Conservatives and Reformists - ECR",
        "ID": "Identity and Democracy - ID",
        "NI": "Non-Inscrits - NI",
    }

    # Substituir nomes conforme o dicionário
    parties = [(name_mapping.get(name, name), seats) for name, seats in raw_parties]

    return render(request, 'eu_parliament.html', {'parties': parties})


def check_parliament(request):
    # Fetch EU countries directly from the database
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name FROM EU_Countries ORDER BY name;")
        countries = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]
    
    return render(request, 'check_parliament.html', {'countries': countries})

def country_parliament(request):
    # Fetch data based on the selected country_id passed from JavaScript
    country_id = request.GET.get('country_id')
    if not country_id:
        return JsonResponse([])  # Return an empty response if no country_id is selected
    
    # Query the parliament seats for the selected country
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ps.epp, ps.s_d, ps.renew_europe, ps.greens_ale, ps.ecr, ps.gue_ngl, ps.ni, ps.total_seats, c.name
            FROM EU_Parliament_Seats ps
            JOIN EU_Countries c ON c.id = ps.country_id
            WHERE c.id = %s;
        """, [country_id])
        result = cursor.fetchall()

    # Return the data as JSON
    if result:
        return JsonResponse([{
            'party_name': row[8],  # country name
            'epp': row[0], 
            's_d': row[1], 
            'renew_europe': row[2],
            'greens_ale': row[3], 
            'ecr': row[4], 
            'gue_ngl': row[5], 
            'ni': row[6], 
            'total_seats': row[7]
        } for row in result], safe=False)
    else:
        return JsonResponse({"error": "No data found"}, status=404)

def fetch_data_from_db(query):
    """ Helper function to execute raw SQL queries and return results as dictionaries """
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def insert_data(request):
    global temporary_posts

    if request.method == "POST":
        country = request.POST.get('country')
        disinfo_technique = request.POST.get('disinfo_technique')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        image_url = None
        if image:
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            image_url = fs.url(filename)

        temporary_posts.append({
            'country': country,
            'disinfo_technique': disinfo_technique,
            'description': description,
            'image_url': image_url,
        })

        return redirect('posts')

    return render(request, 'insert_data.html')


def posts(request):
    return render(request, 'posts.html', {'posts': temporary_posts})


def delete_all_posts(request):
    global temporary_posts  # To modify the global list

    if request.method == "POST":
        password = request.POST.get('password')
        if password == "iamthebest":
            temporary_posts.clear()  # Clear in-memory posts list
            messages.success(request, "All posts have been deleted.")
            return redirect('posts')
        else:
            messages.error(request, "Incorrect password.")
    return render(request, "delete_all.html")

def delete_single_post(request, index):
    global temporary_posts
    if request.method == "POST":
        password = request.POST.get('password')
        if password == "iamthebest":
            try:
                temporary_posts.pop(index)
            except IndexError:
                pass  # Post not found; do nothing
    return redirect('posts')
