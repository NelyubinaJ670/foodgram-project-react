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


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


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


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name',
        'author', 'pub_date',
    )
    list_filter = ('author', 'name', 'tags',)
    exclude = ('tags',)
    inlines = (IngredientRecipeInline, TagInline,)
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author', 'date_added',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
