from __future__ import unicode_literals

import _datetime
import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum
from django.utils import timezone


class Profile(models.Model):
    user = models.CharField(max_length=30, unique=True)
    avatar = models.ImageField(upload_to='uploads', default=None)

    def __str__(self):
        return self.user


class Tag(models.Model):
    tag_title = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.tag_title

    def get_tags(self):
        tags_list = Tag.objects.all()[:10]


class LikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class Like(models.Model):
    LIKE = 1
    # DISLIKE = -1

    VOTES = (
        (LIKE, 'Like'),
        # (DISLIKE, 'Dislike')
    )

    vote = models.SmallIntegerField(verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(Profile, verbose_name="Пользователь", on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeManager()


class QuestionManager(models.Manager):
    def get_new(self):
        return self.order_by('-pub_date')

    def hot(self):
        return self.order_by('-votes')

    def get_tagged(self, tag_name):
        return self.filter(tags__name=tag_name)

    def get_comments(self):
        comment_list = list(self.comment_set.all())
        return comment_list

    def get_tags(self):
        tags_list = list(self.related.all())
        return tags_list

    def create_question(self, author, title, text, tag_names):
        q = self.create(question_author=author,
                        question_title=title,
                        question_text=text)
        q.add_tags(tag_names)
        return q


class Question(models.Model):
    question_author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question_title = models.CharField(max_length=140)
    question_text = models.CharField(max_length=1000)
    pub_date = models.DateTimeField(default=timezone.now, verbose_name=u'date published')
    is_active = models.BooleanField(default=True, verbose_name=u"Доступность вопроса")

    tags = models.ManyToManyField(Tag, blank=True)
    votes = GenericRelation(Like, related_query_name='question')

    def __str__(self):
        return self.question_text

    def add_tags(self, tag_names):
        for name in tag_names:
            self.tags.add(Tag.objects.get_or_create(tag_title=name)[0])
        self.save()

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    objects = QuestionManager()


class Comment(models.Model):
    comment_author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=1000)
    pub_date = models.DateTimeField(default=timezone.now, verbose_name=u'date published')

    is_open = models.BooleanField(default=True)
    votes = GenericRelation(Like, related_query_name='comment')

    def __str__(self):
        return self.comment_text