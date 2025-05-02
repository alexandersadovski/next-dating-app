from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import MinValueValidator
from next.accounts.choices import GenderChoices
from next.accounts.models import Profile


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email',)

    first_name = forms.CharField(
        max_length=25,
        required=True,
    )
    last_name = forms.CharField(
        max_length=25,
        required=True,
    )
    age = forms.IntegerField(
        validators=[MinValueValidator(18)],
        required=True,
    )
    gender = forms.ChoiceField(
        choices=GenderChoices.choices,
        required=True,
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        Profile.objects.get_or_create(
            user=user,
            defaults={
                'first_name': self.cleaned_data['first_name'],
                'last_name': self.cleaned_data['last_name'],
                'age': self.cleaned_data['age'],
                'gender': self.cleaned_data['gender'],
            },
        )
        return user


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'first_name', 'last_name', 'age', 'gender', 'location', 'bio']
        labels = {
            'profile_picture': 'Profile Picture:',
            'first_name': 'First Name:',
            'last_name': 'Last Name:',
            'age': 'Age:',
            'gender': 'Gender:',
            'location': 'Location:',
            'bio': 'Bio:',
        }
