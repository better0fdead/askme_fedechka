from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger, EmptyPage


from .models import *
# Create your views here.

context = {
    'best_users': Profile.objects.all(),
    'hot_tags': Tag.objects.all(),
}

global_info = {
    'tags': Tag.objects.all()[:10],
    'best_users': Profile.objects.all()[:10],
}

questions = [
    {
        "id": f'{i}',
        "avatar": f"/static/img/fly.jpg",
        "title": f"Title {i}",
        "text": f"Саппорт Андрей 'ALWAYSWANNAFLY' Бондаренко поделился инсайдами о перестановках в командах во время личного стрима на Twitch. Он также рассказал о поведении Nightfall на старте карьеры, когда они играли в одном составе. ", 
        "best_ans": f"this is best answer for {i} question", 
        "numb_of_answers": f"{i+1}",
        "tags": global_info['tags'][:3],
        "likes": f"{i - 2}",
    } for i in range(30)
]

def paginate(objects_list, request, per_page=5):
    cl = list(objects_list)
    paginator = Paginator(cl, per_page)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    print("hello drujok-pirojok")
    return page_obj

answers = [
    {
        "number": {i},
        "avatar": f"/static/img/avatar{i}.png",
        "text": f"this is text for {i} answer", 
        "like_counter": f"{i}",
        "dislike_counter": f"{i}",
        "correct_or_no": True,
    } for i in range(1, 7)
]
def index(request):
    tag_list = Tag.objects.all()[:10]
    latest_question_list = Question.objects.get_new()
    page_obj = paginate(latest_question_list, request, 5)
    return render(request, "index.html", {'questions': page_obj, 'global_info' : global_info})

def login(request):
    return render(request, "login.html", {'global_info' : global_info})

def register(request):
    return render(request, "register.html", {'global_info' : global_info})

def hot(request):
    tag_list = Tag.objects.all()[:10]
    hottest_question_list = Question.objects.hot()
    page_obj = paginate(hottest_question_list, request, 5)
    return render(request, "hot.html", {'questions': page_obj, 'global_info' : global_info})

def tag(request):
    paginator = Paginator(questions, 5)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return render(request, "tag.html", {'questions': content, 'global_info' : global_info})

def question(request, qid):
    tag_list_all = Tag.objects.all()[:10]
    question = Question.objects.get(pk=qid)
    comments_list = list(question.comment_set.all())
    page_obj = paginate(comments_list, request, 5)
    tag_list = question.tags.all()[:5]
    
    return render(request, "question.html", {'question': question, 'comments': page_obj, 'tags': tag_list_all, 'question_tags': tag_list, 'global_info' : global_info})

def create(request):
    return render(request, "new_question.html", {'global_info' : global_info})

def tag_page(request, tid):
    tag_list = Tag.objects.all()[:10]
    tag = Tag.objects.get(tag_title=tid)
    latest_question_list = tag.question_set.all()
    page_obj = paginate(latest_question_list, request)
    return render(request, 'tag.html', {'tag': tid, 'questions': page_obj, 'tags': tag_list, 'global_info':global_info})