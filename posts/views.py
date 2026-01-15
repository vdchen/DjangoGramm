from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .forms import PostForm, PostImageForm
from .models import Post, Tag, PostImage


@login_required
def post_create(request):
    if request.method == 'POST':
        p_form = PostForm(request.POST)
        #i_form = PostImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')

        if p_form.is_valid(): #and i_form.is_valid():
            # Save the Post (metadata)
            post = p_form.save(commit=False)
            post.author = request.user
            post.save()
            # Handle the tags string
            tags_data = p_form.cleaned_data.get('tags_str')
            if tags_data:
                tag_list = [t.strip().lower() for t in tags_data.split(',') if
                            t.strip()]
                for tag_name in tag_list:
                    from .models import Tag
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

            # Save the Image and link it to the Post
            #image_instance = i_form.save(commit=False)
            #image_instance.post = post
            #image_instance.save()

            for f in files:
                PostImage.objects.create(post=post, image=f)

            messages.success(request, 'Your post was created successfully!')
            return redirect('home')
    else:
        p_form = PostForm()
        i_form = PostImageForm()

    return render(request, 'posts/post_create.html', {
        'p_form': p_form,
        'i_form': i_form
    })


@login_required
def feed_view(request):
    # Fetch all posts, ordered by newest first
    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'posts/feed.html', {
        'posts': posts
    })


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'count': post.likes.count(),
    })


def tag_view(request, tag_slug):
    tag = get_object_or_404(Tag, name__iexact=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-created_at')

    return render(request, 'posts/feed.html', {
        'posts': posts,
        'tag_name': tag.name
    })