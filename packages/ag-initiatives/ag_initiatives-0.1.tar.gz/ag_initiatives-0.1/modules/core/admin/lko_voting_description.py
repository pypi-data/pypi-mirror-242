# from django.contrib import admin
# from django_summernote import admin as summernote_admin
# from django.db import models
# from django import forms
#
# from modules.core.mixins import TrackUserMixin
# from modules.core.models import LkoVotingDescription
#
#
# @admin.register(LkoVotingDescription)
# class LkoVotingDescriptionAdmin(TrackUserMixin, summernote_admin.SummernoteModelAdmin):
#     list_display = ["description_id", "voting_type"]
#
#     summernote_fields = ["text"]
#     formfield_overrides = {
#         models.TextField: {"widget": forms.TextInput(attrs={"style": "width: 50em"})},
#     }
