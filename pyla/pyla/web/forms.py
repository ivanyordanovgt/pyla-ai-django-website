from django import forms
from django.forms import ModelForm

# from pyla.manage_profiles.models import Feedback
#
#
# class FeedbackForm(forms.ModelForm):
#
#     def __init__(self, user, *args, **kwargs):
#         super(FeedbackForm, self).__init__(*args, **kwargs)
#         self.user = user
#         self.fields['image'].label = ""
#         self.fields['image'].text_field = ""
#         self.fields['description'].widget.attrs.update({'placeholder': 'Describe your problem.'})
#         self.fields['title'].widget.attrs.update({'placeholder': 'Enter a title describing your problem.'})
#         self.fields['video'].widget.attrs.update({'placeholder': 'Send us a link to a video of your problem '
#                                                                  'describing it '
#                                                                  'better. (Upload it to YouTube)'})
#
#     class Meta:
#         model = Feedback
#         fields = ("description", "title", "image", 'video')
#         widgets = {
#             'image': forms.FileInput(),
#         }
