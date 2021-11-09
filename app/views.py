from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
# Create your views here.



global_info = {
    "tags": [
        f"tag{j}"
        for j in range(10)
        ]
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
    paginator = Paginator(questions, 5)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return render(request, "index.html", {'questions': content, 'global_info' : global_info})

def login(request):
    return render(request, "login.html", {'global_info' : global_info})

def register(request):
    return render(request, "register.html", {'global_info' : global_info})

def hot(request):
    paginator = Paginator(questions, 5)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return render(request, "hot.html", {'questions': content, 'global_info' : global_info})

def tag(request):
    paginator = Paginator(questions, 5)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return render(request, "tag.html", {'questions': content, 'global_info' : global_info})

def question(request):
    i = 1
    return render(request, "question.html", {'question': questions[i], 'global_info' : global_info})

def create(request):
    return render(request, "new_question.html", {'global_info' : global_info})