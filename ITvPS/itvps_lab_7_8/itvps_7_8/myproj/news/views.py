from django.shortcuts import render, redirect
from .models import Article, Rubric
from django.contrib import messages
from django.views.generic.edit import CreateView
from .forms import ArticleForm, RubricForm, HashtagForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout


def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрировались!")
            return redirect('login')
    context = {'form': form}
    return render(request, 'news/registerPage.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, "Проверьте правильность ввода значений")
    context = {}
    return render(request, 'news/loginPage.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


def article(request):
    rubrics = Rubric.objects.all()
    return render(request, 'news/article.html', context={'rubrics': rubrics})


def index(request):
    articles = Article.objects.all()
    rubrics = Rubric.objects.all()
    return render(request, 'news/index.html', context={'articles': articles, 'rubrics': rubrics})


def rubrika(request):
    rubrics = Rubric.objects.all()
    return render(request, 'news/rubrika.html', context={'rubrics': rubrics})


def by_rubric(request, rubric_id):
    articles = Article.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'articles': articles, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'news/rubrika.html', context)


def get_one_article(request, article_id):
    current_article = Article.objects.get(pk=article_id)
    rubrics = Rubric.objects.all()
    return render(request, 'news/article.html', context={'current_article': current_article, 'rubrics': rubrics, })


def createArticle(request):
    form = ArticleForm
    if request.method == 'POST':
        articleForm = ArticleForm(request.POST)
        if articleForm.is_valid():
            articleForm.save()
            messages.success(request, "Форма отправлена")
            return redirect('/news/index/')

    return render(request, 'news/createArticle.html', {'form': form})


def createRubric(request):
    form = RubricForm
    if request.method == 'POST':
        rubricForm = RubricForm(request.POST)
        if rubricForm.is_valid():
            rubricForm.save()
            messages.success(request, "Форма отправлена")
            return redirect('/news/index/')

    return render(request, 'news/createRubric.html', {'form': form})


def createHashtag(request):
    form = HashtagForm
    if request.method == 'POST':
        hashtagForm = HashtagForm(request.POST)
        if hashtagForm.is_valid():
            hashtagForm.save()
            messages.success(request, "Форма отправлена")
            return redirect('/news/index/')

    return render(request, 'news/createHashtag.html', {'form': form})
