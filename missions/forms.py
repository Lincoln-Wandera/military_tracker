from django import forms
from .models import Mission, SoldierMission

class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = '__all__'

class SoldierMissionForm(forms.ModelForm):
    class Meta:
        model = SoldierMission
        fields = '__all__'

