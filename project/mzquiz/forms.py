from django import forms
from .models import WordQuiz

class RadioForm(forms.Form):
    group = forms.ChoiceField(
        choices=[("1", "왼쪽"), ("2", "오른쪽")],
        widget=forms.RadioSelect(attrs={'class': 'radio-group'}),
        error_messages={'required': '라디오 그룹을 선택해주세요.'}
    )


