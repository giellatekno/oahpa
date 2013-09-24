from django.conf.urls.defaults import *

# Example wordpress ID:
# http://oahpa.no:8080/sjd_oahpa/openid/ryan
# http://oahpa.no/sjd_oahpa/openid/ryan

# TODO: oahpa or wordpress are doing weird things with usernames in WP, which get set to a url.
#       need to fix this 

# TODO: make a shorter URL that is easier for users, or create a separate
# django service that has access to database tables to check for user
# permissions

# TODO: make the permission check templates prettier / CSS

# TODO: is there some way to automatically fill in the login url on WP so users
# don't have to type it in when they arrive on that page after coming directly
# from Oahpa?

# TODO: Course page needs to be adjusted to show user what their login URL is.

    # You are a member in a course
    #  * Course link
    #  * Copy and paste this URL if you are asked to log in: 

urlpatterns = patterns('openid_provider.views',
    url(r'^$', 'openid_server', name='openid-provider-root'),
    url(r'^decide/$', 'openid_decide', name='openid-provider-decide'),
    url(r'^xrds/$', 'openid_xrds', name='openid-provider-xrds'),
    url(r'^(?P<id>.*)/$', 'openid_xrds', {'identity': True}, name='openid-provider-identity'),
)


