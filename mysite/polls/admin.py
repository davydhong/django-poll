from django.contrib import admin

from .models import Question, Choice


# NOTE: By registering the Question model with admin.site.register(Question), Django was able to construct a default form representation. Often, you’ll want to customize how the admin form looks and works. You’ll do this by telling Django the options you want when you register the object.


# admin.site.register(Choice)
""" 
NOTE: Also note the “Add Another” link next to “Question.” Every object with a ForeignKey relationship to another gets this for free. When you click “Add Another”, you’ll get a popup window with the “Add question” form. If you add a question in that window and click “Save”, Django will save the question to the database and dynamically add it as the selected choice on the “Add choice” form you’re looking at. 

But, really, this is an inefficient way of adding Choice objects to the system. It’d be better if you could add a bunch of Choices directly when you create the Question object. Let’s make that happen.
 """


class ChoiceInLine(admin.TabularInline):
    """SEE: https://docs.djangoproject.com/en/2.2/intro/tutorial07/"""
    # admin.StackInline vs admin.TabularInline
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # fields = ['pub_date', 'question_text']
    """ This particular change above makes the “Publication date” come before the “Question” field: This isn’t impressive with only two fields, but for admin forms with dozens of fields, choosing an intuitive order is an important usability detail. """
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    """You can split fields into fieldsets"""
    inlines = [ChoiceInLine]
    """
    This tells Django: “Choice objects are edited on the Question admin page. By default, provide enough fields for 3 choices."
    """
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    # NOTE: was_published_recently() can be added on the admin field
    list_

admin.site.register(Question, QuestionAdmin)
