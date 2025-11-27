from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Message, Follow
from .forms import PostForm
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db.models import Max, Q


@login_required
def main(request):
    posts = Post.objects.all().order_by('-created_at')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    for p in posts:
        p.is_following = Follow.objects.filter(follower=request.user, following=p.author).exists()

    return render(request, 'main/main.html', {'form': form, 'posts': posts})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('home')

    if request.method == 'POST':
        post.delete()

    return redirect('home')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('home')

    if request.method == "POST":
        new_content = request.POST.get('content')

        if new_content:
            post.content = new_content
            post.edited = True
            post.save()

        return JsonResponse({'status': 'ok', 'content': new_content})


User = get_user_model()
@login_required
def dialog_list(request):
    user = request.user

    dialogs = (
        Message.objects.filter(Q(sender=user) | Q(receiver=user))
        .values('sender', 'receiver')
    )

    users_set = set()

    for d in dialogs:
        if d['sender'] != user.id:
            users_set.add(d['sender'])
        if d['receiver'] != user.id:
            users_set.add(d['receiver'])

    users = User.objects.filter(id__in=users_set).annotate(
        last_msg=Max('sent_messages__timestamp')
    ).order_by('-last_msg')

    return render(request, 'main/dialogs.html', {'users': users})

@login_required
def dialog(request, user_id):
    other = get_object_or_404(User, id=user_id)
    current = request.user

    msgs = Message.objects.filter(
        (Q(sender=current) & Q(receiver=other)) |
        (Q(sender=other) & Q(receiver=current))
    ).order_by('timestamp')

    return render(request, 'main/dialog.html', {
        'messages': msgs,
        'other': other
    })

@login_required
def send_message(request, user_id):
    if request.method == 'POST':
        receiver = get_object_or_404(User, id=user_id)
        content = request.POST.get('content')

        if content.strip():
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content
            )

    return redirect('dialog', user_id=user_id)

@login_required
def toggle_follow(request, user_id):
    target = get_object_or_404(User, id=user_id)

    follow_obj = Follow.objects.filter(follower=request.user, following=target)

    if follow_obj.exists():
        follow_obj.delete()
    else:
        Follow.objects.create(follower=request.user, following=target)

    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def following_list(request):
    following = Follow.objects.filter(follower=request.user).select_related("following")
    return render(request, "main/following.html", {"following": following})
