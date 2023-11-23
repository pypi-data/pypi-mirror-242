from django.contrib import admin

from modules.core.mixins import TrackUserMixin
from modules.core.models import RoleInstruction, InstructionFile


# @admin.register(InstructionFile)
# class InstructionFileAdmin(TrackUserMixin, admin.ModelAdmin):
#     pass
#
#
# @admin.register(RoleInstruction)
# class RoleInstructionAdmin(TrackUserMixin, admin.ModelAdmin):
#     filter_horizontal = ("instructions",)
