from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(UserFollowers)
admin.site.register(UserFollowing)
admin.site.register(Like)
