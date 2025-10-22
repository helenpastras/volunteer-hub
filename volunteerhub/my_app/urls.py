from django.urls import path
from django.contrib.auth.views import LoginView
from . import views # Import views to connect routes to view functions

urlpatterns = [
    path('', views.home, name='home'),
    path('opportunities/', views.opps_index, name='opps-index'),
    path('my-opportunities/', views.user_opps_index, name='user-opps-index'),
    path('opportunities/<int:pk>/like/', views.like_opportunity, name='like-opportunity'),
    path('likes/', views.likes_index, name='likes-index'),
    path('opportunities/<int:pk>/bookmark/', views.bookmark_opportunity, name='bookmark-opportunity'),
    path('bookmarks/', views.bookmarks_index, name='bookmarks-index'),
    path('opportunities/create/', views.OpportunityCreate.as_view(), name='opp-create'),
    path('opportunities/<int:pk>/', views.OpportunityDetail.as_view(), name='opportunity-detail'),
    path('opportunities/<int:pk>/edit/', views.OpportunityUpdate.as_view(), name='opportunity-update'),
    path('opportunities/<int:pk>/delete/', views.OpportunityDelete.as_view(), name='opportunity-delete'),
    path('about/', views.about, name='about'),
    path('login/', LoginView.as_view(), name='login'),
    path('accounts/signup/', views.signup, name='signup'),
]