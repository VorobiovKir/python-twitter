from django.shortcuts import redirect
from django.views.generic import TemplateView


# Create your views here.
class TwitListView(TemplateView):
    template_name = 'twitter_wall/index.html'

    def init_api(self):
        import twitter
        api = twitter.Api(
            consumer_key='nQ1FbhLREforyjU3rmfE0mOai',
            consumer_secret='3uaNilLha1dnpRvst6I2n5LcAnXFgH2nobGt74kr909XtJaxeS',
            access_token_key='4804017803-e4LQBFQMyCBXcggNRlwEriBVd8vtPtsZdq3G3dh',
            access_token_secret='nVRenPJaRIrJiM6iOfFclurGcOjjUMY946ZUZ2ZAPDdLB'
        )
        return api

    def get_context_data(self, **kwargs):
        context = super(TwitListView, self).get_context_data(**kwargs)
        context['tweets'] = self.getTweets()

        return context

    def getTweets(self):
        tweets = []
        try:
            api = self.init_api()
            latest = api.GetUserTimeline('Kir_LightIT')
            for tweet in latest:
                status = tweet.text
                tweet_date = tweet.relative_created_at
                tweets.append({'status': status, 'date': tweet_date})
                # api.PostUpdate('I love python-twitter!')
        except:
            tweets.append({'status': 'Something old', 'date': 'about 10 min ago'})

        return {'tweets': tweets}

    def post(self, request):
        print request.POST
        if request.POST['twit-post-name']:
            api = self.init_api()
            api.PostUpdate(request.POST['twit-post-name'])
        return redirect('twit:twit-list')
