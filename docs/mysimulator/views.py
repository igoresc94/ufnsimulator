from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.http import JsonResponse
from .models import Post
from .forms import PostForm


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def fetch_data_from_db(query):
    """ Helper function to execute raw SQL queries and return results as dictionaries """
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def insert_data(request):
    countries = fetch_data_from_db("SELECT id, name FROM EU_Countries;")
    sectors = fetch_data_from_db("SELECT id, name FROM Sectors;")
    fake_news_techniques = fetch_data_from_db("SELECT id, name FROM Fake_News_Techniques;")
    counter_disinfo_techniques = fetch_data_from_db("SELECT id, name FROM Counter_Disinfo_Techniques;")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = PostForm()

    context = {
        "form": form,
        "countries": countries,
        "sectors": sectors,
        "fake_news_techniques": fake_news_techniques,
        "counter_disinfo_techniques": counter_disinfo_techniques,
    }

    return render(request, "insert_data.html", context)


def posts(request):
    all_posts = Post.objects.all()
    return render(request, "posts.html", {"posts": all_posts})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('posts')


def eu_parliament(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT name, seats FROM EU_Parties ORDER BY seats DESC;
        """)
        raw_parties = cursor.fetchall()

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

    parties = [(name_mapping.get(name, name), seats) for name, seats in raw_parties]

    return render(request, 'eu_parliament.html', {'parties': parties})


def check_parliament(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name FROM EU_Countries ORDER BY name;")
        countries = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]

    return render(request, 'check_parliament.html', {'countries': countries})


def country_parliament(request):
    country_id = request.GET.get('country_id')
    if not country_id:
        return JsonResponse([])

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ps.epp, ps.s_d, ps.renew_europe, ps.greens_ale, ps.ecr, ps.gue_ngl, ps.ni, ps.total_seats, c.name
            FROM EU_Parliament_Seats ps
            JOIN EU_Countries c ON c.id = ps.country_id
            WHERE c.id = %s;
        """, [country_id])
        result = cursor.fetchall()

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
