import random
from random import randint
import collections

from faker import Faker

from app.models import *

locales = collections.OrderedDict([
    ('en-US', 1),
    ('en-PH', 1),
    ('ja_JP', 1),
    ('es_ES', 1),
    ('uk_UA', 1),
    ('ru_RU', 1),
    ('cs_CZ', 1),
    ('lt_LT', 1),
    ('sk_SK', 1),
    ('sl_SI', 1),
])
f = Faker(locales)



def fill_profiles(cnt):
    cnt = int(cnt)
    for i in range(10000):
        Profile.objects.create(user=f.name() + str(i))
        print(i/10000 * 100)


def fill_tags(cnt):
    cnt = int(cnt)
    for i in range(10000):
        Tag.objects.create(tag_title=f.word().lower() + str(i))
        print(i/cnt *100)


def fill_questions(cnt):
    author_ids = list(Profile.objects.all())
    tag_names_list = [tag.tag_title for tag in Tag.objects.all()]
    tags_limit = 5
    for i in range(cnt):
        author_id = f['en-US'].random.choice(author_ids)
        tags = f['en-US'].random.sample(tag_names_list, randint(2, tags_limit))
        title = f.sentence(20)[:19]
        text = f.text(150)[:149]

        question = Question.objects.create_question(
            author=author_id,
            title=title,
            text=text,
            tag_names=tags)

        question.question_author.save()
        question.save()


def fill_likes(cnt, amount_of_questions, amount_of_comments):
    author_ids = list(Profile.objects.all())
    amount_of_authors = len(author_ids)
    likes_per_author = int(cnt / amount_of_authors)
    for i in range(amount_of_authors):
        for j in range(likes_per_author):
            if i % 2 == 1:
                vote = 1
                user = author_ids[i]
                content_type = ContentType.objects.get(app_label='app', model='question')
                object_id = random.uniform(j, amount_of_questions)
                Like.objects.create(vote=vote, user=user, content_type=content_type, object_id=object_id)
            if i % 2 == 0:
                vote = 1
                user = author_ids[i]
                content_type = ContentType.objects.get(app_label='app', model='comment')
                object_id = random.uniform(j, amount_of_comments)
                Like.objects.create(vote=vote, user=user, content_type=content_type, object_id=object_id)
        print(i/amount_of_authors * 100)


def fill_comments(cnt):
    author_ids = list(Profile.objects.all())
    question_ids = list(Question.objects.all())
    for i in range(cnt):
        author_id = f['en-US'].random.choice(author_ids)
        question_id = f['en-US'].random.choice(question_ids)
        text = f.text(150)[:149]
        Comment.objects.create(comment_author=author_id,
                               question=question_id,
                               comment_text=text)
        print(i/cnt *100)

#print(f.name())
#f['en_US']
#fill_tags(10000)
print("tags filled")
#fill_profiles(10000)
print("profiles filled")
fill_questions(100000 - 3500 - 125000)
print("questions filled")
fill_comments(1000000 - 5000)
print("comments filled")
fill_likes(2000000, 1000000, 1000000)
print("likes filled")


