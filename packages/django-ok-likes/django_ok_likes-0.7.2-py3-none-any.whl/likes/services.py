from typing import TYPE_CHECKING, Tuple

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest

from likes.models import Like
from likes.signals import object_liked, object_unliked

if TYPE_CHECKING:
    from django.db.models import Model

User = get_user_model()

__all__ = (
    'toggle',
    'user_likes_count',
    'object_likes_count',
    'is_liked',
    'get_who_liked',
    'send_signals'
)


def toggle(
        *,
        sender: User,
        content_type: ContentType,
        object_id: str
) -> Tuple['Like', bool]:
    """
    Class method to like-dislike object
    """
    obj, created = Like.objects.get_or_create(
        sender=sender,
        content_type=content_type,
        object_id=object_id
    )

    if not created:
        obj.delete()

    return obj, created


def user_likes_count(*, user: 'User') -> int:
    """
    Returns count of likes for a given user.
    """
    if not user.is_authenticated:
        return 0

    return (
        Like.objects
        .filter(
            sender=user,
            content_type__isnull=False,
            object_id__isnull=False
        )
        .count()
    )


def object_likes_count(*, obj: 'Model') -> int:
    """
    Returns count of likes for a given object.
    """
    return (
        Like.objects
        .filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk
        )
        .count()
    )


def is_liked(*, obj: 'Model', user: 'User') -> bool:
    """
    Checks if a given object is liked by a given user.
    """
    if not user.is_authenticated:
        return False

    ct = ContentType.objects.get_for_model(obj)

    return (
        Like.objects
        .filter(
            content_type=ct,
            object_id=obj.pk,
            sender=user
        )
        .exists()
    )


def get_who_liked(*, obj: 'Model'):
    """
    Returns users, who liked a given object.
    """
    ct = ContentType.objects.get_for_model(obj)

    return (
        User.objects
        .filter(
            likes__content_type=ct,
            likes__object_id=obj.pk
        )
    )


def send_signals(
        *,
        created: bool,
        request: HttpRequest,
        like: 'Like',
        obj
):
    """
    Sends signals when object was liked and unliked.
    """
    if created:
        object_liked.send(
            sender=Like,
            like=like,
            request=request
        )
    else:
        object_unliked.send(
            sender=Like,
            object=obj,
            request=request
        )
