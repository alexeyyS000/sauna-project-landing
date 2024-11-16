from django import forms
from .models import CallbackRequest
from django.contrib.auth import get_user_model
from .utils.validation import is_valid_russian_phone_number

UserModel = get_user_model()


class CallbackRequestForm(forms.ModelForm):

    phone_number = forms.CharField(required=True)

    class Meta:
        model = CallbackRequest
        fields = ["user"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ваше имя"}
            ),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")

        if not is_valid_russian_phone_number(phone_number):

            msg = "Incorrect phone number"
            self.add_error("phone_number", msg)
        return phone_number

    def save(self, commit=True, user=None):

        callback_request = super().save(commit=False)

        phone_number = self.cleaned_data["phone_number"]
        try:
            user = UserModel.objects.get(phone_number=phone_number)
            callback_request.user = user
        except UserModel.DoesNotExist:
            name = self.cleaned_data["name"]
            user = UserModel.objects.create(phone_number=phone_number, first_name=name)
            callback_request.user = user

        if commit:
            callback_request.save()

        return callback_request
