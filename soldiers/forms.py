from django import forms
from .models import Soldier,FamilyMember, EmergencyContact
from accounts.models import CustomUser

class SoldierForm(forms.ModelForm):
    date_of_birth = forms.DateField(input_formats=['%d-%m-%Y', '%Y-%m-%d'])
    
    class Meta:
        model = Soldier
        fields = '__all__'
        


class FamilyLinkForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = ['soldier', 'relationship', 'can_receive_notifications', 'is_emergency_contact']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)

        if self.user:
            linked_ids = FamilyMember.objects.filter(user=self.user).values_list('soldier_id', flat=True)
            self.fields['soldier'].queryset = self.fields['soldier'].queryset.exclude(id__in=linked_ids)

class AdminFamilyLinkForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = ['soldier', 'user', 'relationship', 'can_receive_notifications', 'is_emergency_contact', 'is_active']

    def __init__(self, *args, **kwargs):
        soldiers_queryset = kwargs.pop('soldiers_queryset', Soldier.objects.all())
        users_queryset = kwargs.pop('users_queryset', CustomUser.objects.filter(role='family', is_active=True))
        super().__init__(*args, **kwargs)

        self.fields['soldier'].queryset = soldiers_queryset
        self.fields['user'].queryset = users_queryset

        
class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['contact_name', 'relationship', 'phone_number', 'email', 'address', 'is_primary']