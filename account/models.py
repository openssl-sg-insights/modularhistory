import logging
from tempfile import NamedTemporaryFile
from typing import Union
from urllib.request import urlopen

from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.core.files import File
from django.db import models
from django.db.models import QuerySet
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_django.models import UserSocialAuth

from modularhistory.fields.file_field import upload_to

AuthBackend = Union[BaseOAuth1, BaseOAuth2]

AVATAR_QUALITY: int = 70
AVATAR_WIDTH: int = 200
AVATAR_HEIGHT: int = AVATAR_WIDTH


class UserManager(BaseUserManager):
    """Manager for users."""

    @classmethod
    def locked(cls) -> 'QuerySet[User]':
        """Return a queryset of users with locked accounts."""
        return User.objects.filter(locked=True)


class User(AbstractUser):
    """A user of ModularHistory."""

    email = models.EmailField('email address', unique=True)
    avatar = ProcessedImageField(
        null=True,
        blank=True,
        upload_to=upload_to('account/avatars'),
        processors=[ResizeToFill(AVATAR_WIDTH, AVATAR_HEIGHT)],
        format='JPEG',
        options={'quality': AVATAR_QUALITY},
    )
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    locked = models.BooleanField('Lock the account', default=False)
    force_password_change = models.BooleanField(
        'Prompt user to change password upon first login', default=False
    )

    # address = models.CharField(null=True, blank=True, max_length=100)
    # address2 = models.CharField(null=True, blank=True, max_length=40)
    # city = models.CharField(null=True, blank=True, max_length=20)
    # state = models.CharField(null=True, blank=True, max_length=2, choices=settings.STATES)
    # zip_code = models.CharField(null=True, blank=True, max_length=5)
    # date_of_birth = models.DateField(null=True, blank=True)

    social_auth: 'QuerySet[UserSocialAuth]'
    objects: UserManager = UserManager()

    def __str__(self) -> str:
        """TODO: write docstring."""
        return self.get_full_name()

    @property
    def social_auths(self) -> 'QuerySet[UserSocialAuth]':
        """Wrap the reverse attribute of the UserSocialAuth–User relation."""
        return self.social_auth

    def lock(self):
        """Lock the user account."""
        self.locked = True
        self.save()

    def unlock(self):
        """Unlock the user account."""
        self.locked = False
        self.save()

    def update_avatar(self, url):
        """Update the user's avatar with the image located at the given URL."""
        if self.avatar:
            logging.info(f'{self} already has an avatar: {self.avatar}')
            # TODO: check if image has been updated
        else:
            logging.info(f'{self} has no profile image.')
            img_temp = NamedTemporaryFile(delete=True)
            # TODO: Use requests instead of urllib?
            img_temp.write(urlopen(url).read())  # noqa: S310
            img_temp.flush()
            self.avatar.save(f'{self.pk}', File(img_temp))
