from unicodedata import category
from urllib import response
from django.shortcuts import render, get_object_or_404, redirect
from app.models import Post, Category, Comment
from app.form import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.
def Home(request):
    template_name = 'index.html'
    userSearchKeywork = request.GET.get('search')
    postSearch = []
    response = False
    if userSearchKeywork == None:
        pass
    else:
        postSearch = Post.objects.filter(Q(title__contains=userSearchKeywork) | Q(content__contains=userSearchKeywork))
        print(postSearch)
        if postSearch:
            pass
        else:
            response = True

    if postSearch:
        post  = postSearch
    else: 
        post = Post.objects.filter(approval=True, status='Publish')
    categories = Category.objects.all()
    postCat = []
    allpostCat = []
    ac = []
    

    for c in categories:
        #     allcat = Post.objects.filter(Q(category=c))
        #     # post = allcat
        # print('imagine',allcat)
        
        # print('what',allcat)
        catCount = Post.objects.filter(category=c).count()
        postCat.append(catCount)
        
        allpost = Category.objects.all()
        allcatCount = Post.objects.filter(category=c)
        
        if c == allpost:
            print('yay',c)
            # print(allcatCount)
        # print(allpostCat)
        # for a in allpostCat:
        #     if a:
        #         allcat = Post.objects.filter()
        #         ac.append(allcat)

       
    print('what',ac)
    print(postCat) 
    # post = allcat
        
    # print('now',allcat)
    postCategory = zip(categories, postCat)
    page = request.GET.get('page', 1)
    paginator = Paginator(post, 2)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    recent_post = Post.objects.filter(approval=True, status='Publish').order_by('-created_at')[:3]
    # allcategories = Category.objects.all()
    # postCat = []
    # for c in allcategories:
    #     catCount = Post.objects.filter(allcategory=c).order_by('-created_at')[:3]
    #     allcategories = Category.objects.all()
    #     postCat.append(catCount)
    #     print(postCat)
     

    context = {
        'posts': posts,
        'postCategory': postCategory,
        'response': response,
        'recent_post': recent_post
    }
    return render(request, template_name, context)

def BlogDetails(request, slug):
    template_name = 'details.html'
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post)
    comment_form = CommentForm()
    if request.method == "POST":
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            c = comment_form.save(commit=False)
            c.post = post
            c.save()
            return redirect(f'/detail/{post.slug}')

    context = {
        'post': post,
        'comment_form': comment_form,
        'comments': comments
    }
    return render(request, template_name, context)