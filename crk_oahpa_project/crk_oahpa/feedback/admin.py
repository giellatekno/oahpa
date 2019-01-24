from crk_feedback.models import Feedback
from django.contrib import admin

# class FeedbackAdmin(admin.ModelAdmin):
# 
#     list_display = ('confirmation', 'confirmed_by', 'name', 'email', 'place','date','message')
# 
#     fieldsets = (
#         (None, {
#         'fields': ('confirmed_by', 'confirmation_date', 'comments', 'message')
#         }),
#         )

# admin.site.register(Feedback, FeedbackAdmin)

admin.site.register(Feedback)
