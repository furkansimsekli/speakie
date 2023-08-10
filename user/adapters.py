from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialApp, SocialAccount

from . import utils


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)

        if sociallogin.account.provider == 'google':
            social_app = SocialApp.objects.get(provider='google')
            if social_app:
                google_account = SocialAccount.objects.get(user=user, provider='google')
                profile_picture = utils.save_image_from_google(google_account.get_avatar_url())
                user.profile_picture = profile_picture
                user.save()
