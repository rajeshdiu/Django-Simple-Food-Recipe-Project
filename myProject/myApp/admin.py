
from django.contrib import admin
from .models import *
from django.contrib import admin

class customUserDisplay(admin.ModelAdmin):
    list_display = ('username', 'user_type')

admin.site.register(Custom_User, customUserDisplay)

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'preparation_time', 'cooking_time', 'total_time', 'difficulty', 'total_calorie')
    search_fields = ('title', 'category__name', 'tags__name')
    list_filter = ('category', 'tags', 'difficulty')

class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'user__email')

class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__title')

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeCategory, RecipeCategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
