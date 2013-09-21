from django.contrib import admin
from apps.blog.models import *
from django.core.mail import EmailMultiAlternatives
from django.http import BadHeaderError


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish', 'status')
    list_filter = ('publish', 'categories', 'status')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        """
        Given a ModelForm return an unsaved instance. ``change`` is True if
        the object is being changed, and False if it's being added.
        """
        admin.ModelAdmin.save_model(self, request, obj, form, change)

        # send an email if we are adding a new post
        if not change:
            # send an email to all users in the system to notify them that a new post is available
            title = 'Aptitude World ANZ - new post is available'
            email_txt = """
                Dear Customer,

                This is a courtesy email to inform you that a new post is now available to view on our website on the following URL:

                Regards,
                Aptitude World ANZ
            """
            email_html = """
                Dear Customer,

                This is a courtesy email to inform you that a new post is now available to view on our website on the following URL:

                Regards,
                Aptitude World ANZ
            """

            email_from = 'info@aptitudeworld.com.au'
            email_to = 'anggiarto@gmail.com'

            try:
                # email_message = EmailMultiAlternatives(title, email_txt, email_from, [email_to],
                #                                        ['info@aptitudeworld.com.au'])
                email_message = EmailMultiAlternatives(title, email_txt, email_from, [email_to])
                email_message.attach_alternative(email_html, 'text/html')
                email_message.send()
            except BadHeaderError:
                pass


admin.site.register(Post, PostAdmin)


class BlogRollAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'sort_order',)
    list_editable = ('sort_order',)


admin.site.register(BlogRoll)