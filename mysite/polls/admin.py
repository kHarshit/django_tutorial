from django.contrib import admin
from .models import Question, Choice

# admin.site.register(Question)
# admin.site.register(Choice)

class ChoiceInline(admin.TabularInline):  # StackedInline
    model = Choice
    extra = 3

class QuesionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields':['question_text']}),
        ('Date information', {'fields':['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['quesiton_text']

admin.site.register(Question, QuesionAdmin)