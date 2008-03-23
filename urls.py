from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^twitter/', include('twitter.foo.urls')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
                       (r'^twitter/(?P<username>[\w]+)/', 'twimage.views.twittertoimage'),
)
