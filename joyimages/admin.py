from django.contrib import admin
from .models import Image,Profile,Comment,Follow

# Register your models here.

# class ImageAdmin(admin.ModelAdmin):
#     list_display = ('name','posted_on')
#     list_filter = ('name',)
#     search_fields = ['name','caption']

# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('post','user','body','posted_on','active')
#     list_filter = ('active', 'posted_on')
#     search_fields = ('user', 'body')
#     actions = ['approve_comments']

# def approve_comments(self, request, queryset):
#     queryset.update(active=True)


admin.site.register(Profile)
admin.site.register(Image)
admin.site.register(Comment)
# admin.site.register(Post)
admin.site.register(Follow)

