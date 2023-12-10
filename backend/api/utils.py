from django.shortcuts import get_object_or_404

from recipes.models import Recipe, Subscription


def create(request, pk, serializer_in, serializer_out, model):
    """
    Создания связей в Favorite, ShoppingCart, Subscription.
    """
    user = request.user.id
    obj = get_object_or_404(model, id=pk)

    recipe_data = {'user': user, 'recipe': obj.id}
    subscribe_data = {'user': user, 'author': obj.id}

    if model is Recipe:
        serializer = serializer_in(data=recipe_data)
    else:
        serializer = serializer_in(data=subscribe_data)

    serializer.is_valid(raise_exception=True)
    serializer.save()
    serializer_to_response = serializer_out(obj, context={'request': request})
    return serializer_to_response


def delete(request, pk, model_object, delete_object):
    """
    Удаления связей в Favorite, ShoppingCart, Subscription.
    """
    user = request.user

    obj_recipe = get_object_or_404(model_object, id=pk)
    obj_subscription = get_object_or_404(model_object, id=pk)

    if delete_object is Subscription:
        object = get_object_or_404(
            delete_object, user=user, author=obj_subscription
        )
    else:
        object = get_object_or_404(
            delete_object, user=user, recipe=obj_recipe
        )
    object.delete()
