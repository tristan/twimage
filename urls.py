from django.conf.urls.defaults import *
from settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = patterns('',
    # Example:
    # (r'^twitter/', include('twitter.foo.urls')),


                       (r'^%s/(?P<path>.*)$' % MEDIA_URL[1:], 'django.views.static.serve', 
                        {'document_root': MEDIA_ROOT, 'show_indexes': True}),
    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
                       (r'^twitter/(?P<username>[\w]+)/(?P<id>[\w]+)/', 'core.views.fromstatus'),
                       (r'^twitter/(?P<username>[\w]+)/', 'core.views.fromuser'),
)
