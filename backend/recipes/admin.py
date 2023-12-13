from django.contrib import admin

from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    IngredientRecipe,
    ShoppingCart,
    Favorite,
    Subscription
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    list_filter = ('name', )
    empty_value_display = '-пусто-'


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 0
    min_num = 1


class TagInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 0
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name',
        'author', 'pub_date',
    )
    list_filter = ('author', 'name', 'tags',)
    exclude = ('tags',)
    inlines = (IngredientRecipeInline, TagInline,)
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author', 'date_added',)
