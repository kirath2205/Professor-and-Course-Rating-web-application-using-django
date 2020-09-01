from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path("", views.index,name="MainSite"),
    path("contact/", views.contact,name="ContactUs"),
    path("search/", views.search,name="Search"),
    path("about/", views.about,name="about"),
    #path("courseview/<int:id>",views.viewcourse,name="viewcourse"),
    path('postComment',views.postComment,name='postComment'),
    path("courseview/<str:slug>",views.viewcourse,name="viewcourse"),
    path('signup',views.handle_signup,name='handle_signup'),
    path('login',views.handle_login,name='handle_login'),
    path('logout',views.handle_logout,name='handle_logout'),
    path('postRating',views.postRating,name='postRating')
    #,path('postrating',views.postRating,name='postrating')
    
]
