import os
from django import forms
from django.conf import settings

from .models import Commodities


"""
When Django is launched, prefetch a Queryset of active postcodes (i.e. the postcodes in which a distributor is active)
"""


# class commodity_dropdown_field(forms.Form):
#
#     commodity_one = forms.ModelChoiceField(
#         queryset=Commodities.objects.all(),
#         label=u"",
#     )
#
#     commodity_two = forms.ModelChoiceField(
#         queryset=Commodities.objects.all(),
#         label=u"",
#     )
#
#
#     def __init__(self, *args, **kwargs):
#         super(commodity_dropdown_field, self).__init__(*args, **kwargs)
#         queryset = Commodities.objects.all()
#         self.fields['commodity_one'].queryset = queryset
#         self.fields['commodity_one'].initial = queryset.first()
#
#         self.fields['commodity_two'].queryset = queryset
#         self.fields['commodity_two'].initial = queryset.get(commodity_name='Silver')
