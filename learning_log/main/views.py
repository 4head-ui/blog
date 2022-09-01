from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import Http404


def index(request):
    """Домашняя страница приложения Learning Log"""
    return render(request, 'main/index.html')


@login_required
def topics(request):
    """Выводит список тем."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'main/topics.html', context)


@login_required
def topic(request, topic_id):
    """Выводит одну тему и все ее записи."""
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'main/topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
 # Данные не отправлялись; создается пустая форма.
        form = TopicForm()
    else:
 # Отправлены данные POST; обработать данные.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('main:topics')
 # Вывести пустую или недействительную форму.
    context = {'form': form}
    return render(request, 'main/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method != 'POST':
            # Данные не отправлялись; создается пустая форма.
        form = EntryForm()
    else:
            # Отправлены данные POST; обработать данные.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('main:topic', topic_id=topic_id)

        # Вывести пустую или недействительную форму.
    context = {'topic': topic, 'form': form}
    return render(request, 'main/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry,id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        # No data submitted; create a blank form
        form = EntryForm(instance=entry)
    else:
        # Post data submitted;process data
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('main:topic',topic_id=topic.id)


    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'main/edit_entry.html', context)

