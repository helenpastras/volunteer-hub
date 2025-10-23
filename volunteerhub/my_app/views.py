from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Opportunity, Like, Bookmark


def home(request):
    opportunities = Opportunity.objects.all()
    liked_opps = request.user.liked_opportunities.all() if request.user.is_authenticated else []
    bookmarked_opps = request.user.bookmarked_opportunities.all() if request.user.is_authenticated else []

    return render(request, 'home.html', {
        'opportunities': opportunities,
        'liked_opps': liked_opps,
        'bookmarked_opps': bookmarked_opps,
    })


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def opps_index(request):
    opportunities = Opportunity.objects.all()
    liked_opps = request.user.liked_opportunities.all() if request.user.is_authenticated else []
    bookmarked_opps = request.user.bookmarked_opportunities.all() if request.user.is_authenticated else []

    return render(request, 'opportunities/index.html', {
        'opportunities': opportunities,
        'liked_opps': liked_opps,
        'bookmarked_opps': bookmarked_opps,
        })

def about(request):
    return render(request, 'about.html')

@login_required
def user_opps_index(request):
    user = request.user
    created_opps = Opportunity.objects.filter(created_by=user)
    liked_opps = Opportunity.objects.filter(likes__user=user)
    bookmarked_opps = Opportunity.objects.filter(bookmarks__user=user)

    context = {
        'created_opps': created_opps,
        'liked_opps': liked_opps,
        'bookmarked_opps': bookmarked_opps,
    }
    return render(request, 'opportunities/user_index.html', context)

def likes_index(request):
    liked_opps = request.user.liked_opportunities.all()
    return render(request, 'likes_index.html', {
        'liked_opps': liked_opps,
    })

def bookmarks_index(request):
    bookmarked_opps = request.user.bookmarked_opportunities.all()
    return render(request, 'bookmarks/index.html', {
        'bookmarked_opps': bookmarked_opps,
    })


# CRUD for Opportunities
class OpportunityCreate(LoginRequiredMixin, CreateView):
    model = Opportunity
    fields = ['title', 'description', 'location', 'date', 'tags']
    template_name = 'opportunities/opportunity_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class OpportunityDetail(DetailView):
    model = Opportunity
    template_name = 'opportunities/opportunity_detail.html'


class OpportunityUpdate(LoginRequiredMixin, UserPassesTestMixin , UpdateView):
    model=Opportunity
    fields= ['title', 'description', 'location', 'date', 'tags']
    template_name = 'opportunities/opportunity_form.html'

    def test_func(self):
        return self.get_object().created_by == self.request.user
    

class OpportunityDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Opportunity
    template_name = 'opportunities/opportunity_confirm_delete.html'
    success_url = reverse_lazy('user-opps-index')

    def test_func(self):
        return self.get_object().created_by == self.request.user


# CRUD for Likes
def like_opportunity(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    Like.objects.get_or_create(user=request.user, opportunity=opportunity)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def unlike_opportunity(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    Like.objects.filter(user=request.user, opportunity=opportunity).delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# CRUD for Bookmarks
def bookmark_opportunity(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    Bookmark.objects.get_or_create(user=request.user, opportunity=opportunity)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def remove_bookmark(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    Bookmark.objects.filter(user=request.user, opportunity=opportunity).delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def complete_bookmark(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    bookmark = Bookmark.objects.filter(user=request.user, opportunity=opportunity).first()
    if bookmark:
        bookmark.completed = True
        bookmark.completed_at = timezone.now()
        bookmark.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))