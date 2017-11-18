# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import Indicator
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.utils.translation import gettext, gettext_lazy as _
from .models import Model_param
from django.db.models.manager import Manager

class CreateModelParamForm(forms.ModelForm):
    class Meta:
        model = Model_param
        fields = ('model', 'indicator')

    def save(self, commit=True, *args, **kwargs):
        obj = super(CreateModelParamForm, self).save(commit=False)
        obj.owner = self.owner
        if commit:
            obj.save()
        return obj
