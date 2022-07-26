from django import forms as forms

from pyla.forums.models import Comment, Post


class PostCommentForm(forms.ModelForm):
    def __init__(self, post, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.post = post
        self.fields['description'].widget.attrs.update(
            {
                'placeholder': 'What are your thoughts?'
            }
        )

        for field in self.fields:
            self.fields[f'{field}'].label = ""

    def save(self, commit=True):
        # commit false does not persist to database
        # just returns the object to be created
        feedback = super().save(commit=False)

        feedback.post = self.post
        feedback.user = self.user
        if commit:
            feedback.save()

        return feedback

    class Meta:
        model = Comment
        fields = ('description',)
        # widgets = {
        #     'description': forms.TextInput(
        #         attrs={
        #             'placeholder': 'Enter pet name',
        #         }
        #     ),
        # }


class PostForm(forms.ModelForm):
    def __init__(self, forum, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.forum = forum
        self.fields['description'].widget.attrs.update(
            {
                'placeholder': 'Describe your post'
            }
        )

        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'Title of your post'
            }
        )

        for field in self.fields:
            self.fields[f'{field}'].label = ""

    def save(self, commit=True):
        # commit false does not persist to database
        # just returns the object to be created
        feedback = super().save(commit=False)

        feedback.forum = self.forum
        feedback.user = self.user
        if commit:
            feedback.save()

        return feedback

    class Meta:
        model = Post
        fields = ('title', 'description')
        # widgets = {
        #     'description': forms.TextInput(
        #         attrs={
        #             'placeholder': 'Enter pet name',
        #         }
        #     ),
        # }
