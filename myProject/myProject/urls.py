
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', signupPage, name='signupPage'),
    path('logoutPage/', logoutPage, name='logoutPage'),
    path('mySigninPage/', mySigninPage, name='mySigninPage'),
    path('dashBoardPage/', dashBoardPage, name='dashBoardPage'),
    path('forget_pass/', forget_pass, name='forget_pass'),
    path('update_pass/', update_pass, name='update_pass'),
    path('addRecipePage/', addRecipePage, name='addRecipePage'),
    path('recipe_categories/', recipe_categories, name='recipe_categories'),
    path('search_results/', search_results, name='search_results'),
    path('viewRecipePage/', viewRecipePage, name='viewRecipePage'),
    path('view_favorites/', view_favorites, name='view_favorites'),
    path('add_to_favorites/<int:recipe_id>/', add_to_favorites, name='add_to_favorites'),
    path('AddRecipeCategoryPage/', AddRecipeCategoryPage, name='AddRecipeCategoryPage'),
    path('activate/<uid64>/<token>', activate,name='activate'),
    path('edit_recipe/<str:myid>', edit_recipe,name='edit_recipe'),
    path('delete_recipe/<str:myid>', delete_recipe,name='delete_recipe'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)