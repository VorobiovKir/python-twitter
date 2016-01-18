from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.generic import TemplateView

from social.apps.django_app.default.models import UserSocialAuth


def api_init(request):
    """

    Initialize twitter API

    Arguments:
        request object -- give User or give User_id

    Returns:
        object -- twitter api object
    """

    if request.GET.get('usid'):
        request.session['usid'] = request.GET.get('usid')

    if request.session.get('usid'):
        user = UserSocialAuth.objects.get(user=request.session['usid']) or None
    else:
        user = UserSocialAuth.objects.get(user=request.user.id) or None

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


class TwitListView(TemplateView):
    """

    Give tweets, user_detail, followers


    """
    template_name = 'twitter_wall/index.html'

    def get_context_data(self, **kwargs):
        context = super(TwitListView, self).get_context_data(**kwargs)
        context['tweets_content'] = self.getTwitContent()
        context['authenticated_user'] = UserSocialAuth.objects.all()

        return context

    def getTwitContent(self):
        tweets = []
        followers = []
        user_detail = []
        try:
            api = api_init(self.request)
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


def addTwit(request):
    """

    Add twitline and redirect on twitter list page
    """
    if request.POST['twit-post-name']:
        api = api_init(request)
        api.PostUpdate(request.POST['twit-post-name'])

    return redirect('twit:twit-list')


def logOut(request):
    logout(request)
    try:
        del request.session['usid']
    except:
        pass

    return redirect('/')


# class IndexView(TemplateView):
#     template_name = 'twitter_wall/index.html'
