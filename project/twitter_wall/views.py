from django.shortcuts import redirect

from django.views.generic import TemplateView
from django.contrib.auth import logout

from social.apps.django_app.default.models import UserSocialAuth


class TwitListView(TemplateView):
    template_name = 'twitter_wall/index.html'

    def get_context_data(self, **kwargs):
        context = super(TwitListView, self).get_context_data(**kwargs)
        context['tweets_content'] = self.getTwitContent()
        context['authenticated_user'] = UserSocialAuth.objects.all()

        return context

    def api_init(self):
        if self.request.POST.get('user_id'):
            user = UserSocialAuth.objects.get(user=self.request.POST['user_id'])
        else:
            user = UserSocialAuth.objects.get(user=self.request.user.id) or None

        if user:
            CONSUMER_KEY = 'nQ1FbhLREforyjU3rmfE0mOai'
            CONSUMER_SECRET = '3uaNilLha1dnpRvst6I2n5LcAnXFgH2nobGt74kr909XtJaxeS'
            ACCESS_TOKEN_KEY = user.extra_data['access_token'].get('oauth_token')
            ACCESS_TOKEN_SECRET = user.extra_data['access_token'].get('oauth_token_secret')
        else:
            return None

        import twitter
        api = twitter.Api(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token_key=ACCESS_TOKEN_KEY,
            access_token_secret=ACCESS_TOKEN_SECRET
        )

        return api

    def getTwitContent(self):
        tweets = []
        followers = []
        user_detail = []
        try:
            api = self.api_init()
            user_detail = api.VerifyCredentials()
            followers = api.GetFollowers()
            latest = api.GetUserTimeline()
            for tweet in latest:
                status = tweet.text
                date = tweet.relative_created_at
                tweets.append({'status': status, 'date': date})
        except:
            tweets.append({'status': 'Nothing', 'date': 'never'})

        return {
            'tweets': tweets,
            'followers': followers,
            'user_detail': user_detail
        }

    def post(self, request):
        if request.POST['twit-post-name']:
            api = self.api_init()
            api.PostUpdate(request.POST['twit-post-name'])

        return redirect('twit:twit-list')


def logOut(request):
    logout(request)
    return redirect('/')


class IndexView(TemplateView):
    template_name = 'twitter_wall/index.html'
