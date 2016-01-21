import twitter

from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import logout
from django.views.generic import TemplateView, RedirectView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

    try:
        user = UserSocialAuth.objects.get(user=request.session.get('usid', request.user.id))
    except UserSocialAuth.DoesNotExist:
        return {}

    CONSUMER_KEY = 'nQ1FbhLREforyjU3rmfE0mOai'
    CONSUMER_SECRET = '3uaNilLha1dnpRvst6I2n5LcAnXFgH2nobGt74kr909XtJaxeS'
    ACCESS_TOKEN_KEY = user.extra_data['access_token'].get('oauth_token')
    ACCESS_TOKEN_SECRET = user.extra_data['access_token'].get('oauth_token_secret')

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
    template_name = 'twitter_wall/twitter.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(TwitListView, self).get_context_data(**kwargs)
        context['authenticated_user'] = UserSocialAuth.objects.all()
        context['tweets_content'] = self.get_twit_content()
        tweets = context['tweets_content']['tweets']

        paginator = Paginator(tweets, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            context['tweets_content']['tweets'] = paginator.page(page)
        except PageNotAnInteger:
            context['tweets_content']['tweets'] = paginator.page(1)
        except EmptyPage:
            context['tweets_content']['tweets'] = paginator.page(paginator.num_pages)

        return context

    def get_twit_content(self):  # get_twit_content
        tweets = []
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
            followers = []
            user_detail = []

        return {
            'tweets': tweets,
            'followers': followers,
            'user_detail': user_detail
        }

    def post(self, request, *args, **kwargs):
        """

        Add twitline and redirect on twitter list page
        """
        if request.POST['twit-post-name']:
            api = api_init(request)
            api.PostUpdate(request.POST['twit-post-name'])

        return redirect('twit:twit-list')


class LogoutView(RedirectView):
    url = reverse_lazy('twit:twit-list')

    def get(self, request, *args, **kwargs):
        if request.session.get('usid'):
            del request.session['usid']
        logout(request)

        return super(LogoutView, self).get(request, *args, **kwargs)


class LoginView(RedirectView):
    url = reverse_lazy('social:begin', kwargs={'backend': 'twitter'})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            logout(request)

        return super(LoginView, self).get(request, *args, **kwargs)
