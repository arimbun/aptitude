import apps
from django.contrib import admin
from apps.blog.models import *
from django.core.mail import EmailMultiAlternatives
from django.http import BadHeaderError
import os
# sys.path.append('/opt/pycharm-2.7.3/helpers/pydev/')
# import pydevd


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

        # pydevd.settrace('localhost', port=8001, stdoutToServer=True, stderrToServer=True)
        post_title = obj.title
        post_url = 'http://www.aptitudeworld.com.au/blog'

        # send an email if we are adding a new post
        if not change:
            # send an email to all users in the system to notify them that a new post is available
            email_title = 'Aptitude World ANZ - A new post is available'
            email_from = 'info@aptitudeworld.com.au'

            try:
                # get all user emails in the database
                users = apps.users.models.User.objects.all()
                confirmation_email_txt_template = open(
                    os.getcwd() + '/apps/landing/templates/landing/email/new_post_email.txt', 'r')
                confirmation_email_html_template = open(
                    os.getcwd() + '/apps/landing/templates/landing/email/new_post_email.html', 'r')
                for u in users:
                    email_to = u.email_address
                    full_name = u.first_name + " " + u.last_name

                    email_txt = confirmation_email_txt_template.read() % (full_name, post_title, post_url)
                    email_html = confirmation_email_html_template.read() % (full_name, post_title, post_url)

                    email_message = EmailMultiAlternatives(email_title, email_txt, email_from, [email_to])
                    email_message.attach_alternative(email_html, 'text/html')
                    email_message.send()
            except BadHeaderError:
                pass


admin.site.register(Post, PostAdmin)


class BlogRollAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'sort_order',)
    list_editable = ('sort_order',)


admin.site.register(BlogRoll)