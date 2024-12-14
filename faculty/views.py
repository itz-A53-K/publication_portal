from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F
from datetime import datetime

from faculty import models, functions

# Create your views here.

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'faculty/dashboard.html')


def loginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        faculty = authenticate(request, email=email, password=password, is_admin=False)
        if faculty is not None:
            login(request, faculty)
            return redirect('dashboard')
        else:
            return redirect('loginView')
        
    return render(request, 'faculty/login.html')


@login_required(login_url='login')
def logoutView(request):
    logout(request)
    return redirect('/')


@login_required(login_url='login')
def myProfile(request):
    faculty = request.user

    if request.method == 'POST':
        phone = request.POST.get('phone')
        profile_img = request.FILES.get('profile_img')
        qualification = request.POST.get('qualification')
        co_authors = request.POST.get('co_authors')


        faculty_details = models.Faculty_details.objects.filter(faculty=faculty).update(
            phone=phone,
            profile_img=profile_img,
            qualification=qualification,
            co_authors=co_authors
        )

        
    faculty_details = models.Faculty_details.objects.get(faculty=faculty)
    faculty_publications = models.Publication.objects.filter(authors=faculty)

    context = {
        'faculty_details': faculty_details,
        'faculty_publications': faculty_publications,
    }


    return render(request, 'faculty/myProfile.html', context)




@login_required(login_url='login')
def upload_article(request):

    if request.method == 'POST':

        title = request.POST.get('a_title')
        abstract = request.POST.get('a_abstract')
        keywords = request.POST.get('a_keywords')
        publisher = request.POST.get('a_publisher')
        publish_date = request.POST.get('a_publish_date')
        content = request.POST.get('a_content')
        content_pdf = request.FILES.get('a_pdf')
        volume = request.POST.get('a_volume')
        pages = request.POST.get('a_pages')
        authors = request.POST.get('a_authors')
        citations = request.POST.getlist('a_citations')  # Fetch citations list if provided

        if not publish_date:
            publish_date = datetime.now().date()
        else:
            publish_date = datetime.strptime(publish_date, '%Y-%m-%d')

        keywords_json = functions.txt_to_json(keywords,',')
        authors_list = functions.get_author_objs_list(authors)

        # Check for potential redundancy
        is_duplicate = functions.check_redundancy(title, abstract, authors_list, keywords_json)

        if is_duplicate:
            print("Duplicate article found")
        else:
            article_obj = models.Article (
                title = title,
                abstract = abstract,
                keywords = keywords_json,
                publisher = publisher,
                publish_date = publish_date,
                content = content,
                pdf = content_pdf,
                volume = volume,
                pages = pages,
            )

            article_obj.save()
            article_obj.authors.set(authors_list)

            if (citations):
                # add citations to the article
                functions.add_citation(citations , article_obj.id)
                functions.update_h_index(citations)

            for author in authors_list:
                # update author's dept's publication Count
                models.Department.objects.filter(id=author.dept.id).update(publication_count= F('publication_count') + 1)

    return render(request, 'faculty/upload.html')