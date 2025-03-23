# App Imports
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import CharField, Form, ModelForm

from llm.models import Summary


class LoginForm(Form):
    username = CharField()
    password = CharField()


class SignupForm(Form):
    username = CharField()
    password = CharField()
    re_password = CharField()

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")
        if password != re_password:
            raise ValidationError(
                {"re_password": "Passwords doesn't match."}, code="invalid"
            )

        user = User(username=username)
        user.validate_unique()
        user.set_password(raw_password=password)
        user.save()
        self.cleaned_data["user"] = user
        return self.cleaned_data


class SummaryForm(ModelForm):
    class Meta:
        model = Summary
        fields = ("attachment", "summary_length")
