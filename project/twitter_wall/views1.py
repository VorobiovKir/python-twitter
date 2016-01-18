from django.shortcuts import redirect

from django.views.generic import TemplateView
from django.contrib.auth import logout

from social.apps.django_app.default.models import UserSocialAuth


# Create your views here.
class TwitListView(TemplateView):
    template_name = 'twitter_wall/index.html'
    paginate_by = 3
    page = 1

    def paginated(self, items, page):
        tweets_from = 0 + self.paginate_by * (page - 1)
        tweets_to = self.paginate_by + self.paginate_by * (page - 1)

        return items[tweets_from:tweets_to]

    def init_api(self):
        import twitter

        # user = UserSocialAuth.objects.filter(user=self.request.user.id)

        api = twitter.Api(
            consumer_key='nQ1FbhLREforyjU3rmfE0mOai',
            consumer_secret='3uaNilLha1dnpRvst6I2n5LcAnXFgH2nobGt74kr909XtJaxeS',
            # access_token_key='4804017803-e4LQBFQMyCBXcggNRlwEriBVd8vtPtsZdq3G3dh',
            # access_token_secret='nVRenPJaRIrJiM6iOfFclurGcOjjUMY946ZUZ2ZAPDdLB'
            access_token_key='4804084887-4VxxUJhjRtgBbXTA1Vpkqaybjy08DStFjLhrUaI',
            access_token_secret='CrQMUKVyRscH5V2XmHxXwWdIjuhQaqNIO4Rwnp5euBcCQ'
        )

        return api
        # access_token = {
        #     "access_token": {
        #         "oauth_token_secret": "nVRenPJaRIrJiM6iOfFclurGcOjjUMY946ZUZ2ZAPDdLB",
        #         "oauth_token": "4804017803-e4LQBFQMyCBXcggNRlwEriBVd8vtPtsZdq3G3dh",
        #         "x_auth_expires": "0",
        #         "user_id": "4804017803",
        #         "screen_name": "Kir_LightIT"
        #     },
        #     "id": 4804017803}

        # access_token = {"oauth_token_secret": "CrQMUKVyRscH5V2XmHxXwWdIjuhQaqNIO4Rwnp5euBcCQ", "oauth_token": "4804084887-4VxxUJhjRtgBbXTA1Vpkqaybjy08DStFjLhrUaI", "x_auth_expires": "0", "user_id": "4804084887", "screen_name": "MaistrenkoAnton"}

        # api = twitter.Api(

        #     # consumer_key = 'HZ4Wf9hGIahvbIwxHpVFDo5Au',
        #     # consumer_secret = 'TqPu0GQZV3oQcCcjQnmRHhEs8c37BxhVD28bRJtxcgkJpnmcfC',
        #     # access_token_key='4804084887-4VxxUJhjRtgBbXTA1Vpkqaybjy08DStFjLhrUaI',
        #     # access_token_secret='CrQMUKVyRscH5V2XmHxXwWdIjuhQaqNIO4Rwnp5euBcCQ',

        #     # token=access_token.to_string()
        #     # -- MY
        #     consumer_key='nQ1FbhLREforyjU3rmfE0mOai',
        #     consumer_secret='3uaNilLha1dnpRvst6I2n5LcAnXFgH2nobGt74kr909XtJaxeS',
        #     # access_token_key='4804017803-e4LQBFQMyCBXcggNRlwEriBVd8vtPtsZdq3G3dh',
        #     # access_token_secret='nVRenPJaRIrJiM6iOfFclurGcOjjUMY946ZUZ2ZAPDdLB'
        #     access_token='4804084887-4VxxUJhjRtgBbXTA1Vpkqaybjy08DStFjLhrUaI',
        #     access_token_secret='CrQMUKVyRscH5V2XmHxXwWdIjuhQaqNIO4Rwnp5euBcCQ',
        # )

    def get_context_data(self, **kwargs):
        context = super(TwitListView, self).get_context_data(**kwargs)
        context['tweets'] = self.getTweets()

        return context

    def getTweets(self):
        tweets = []
        followers = {}
        user = {}
        authenticated_user = {}
        try:
            user = UserSocialAuth.objects.get(user=self.request.user.id)
            print user
            api = self.init_api()
            items = api.GetUserTimeline()
            latest = self.paginated(items, self.page)
            for tweet in latest:
                status = tweet.text
                tweet_date = tweet.relative_created_at
                tweets.append({'status': status, 'date': tweet_date})
            followers = api.GetFollowers()
            user = api.VerifyCredentials()
            authenticated_user = UserSocialAuth.objects.all()
        except:
            tweets.append({'status': 'Something old', 'date': 'about 10 min ago'})

        return {
            'tweets': tweets,
            'followers': followers,
            'user': user,
            'authenticated_user': authenticated_user
        }

    def post(self, request):
        if request.POST['twit-post-name']:
            api = self.init_api()
            api.PostUpdate(request.POST['twit-post-name'])

        print '-------------------'

        return redirect('twit:twit-list')


class IndexView(TemplateView):
    template_name = 'twitter_wall/index.html'


def logOut(request):
    logout(request)
    # return redirect(reverse('twit-home'))
    return redirect('/')
