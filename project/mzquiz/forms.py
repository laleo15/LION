from django import forms
from .models import WordQuiz

class RadioForm(forms.Form):
    def __init__(self, *args, **kwargs):
        quiz = kwargs.pop('quiz')  # 데이터베이스에서 가져온 질문들
        super(RadioForm, self).__init__(*args, **kwargs)
        
        field_name = f'{quiz.subject}'
        self.fields[field_name] = f = forms.ChoiceField(
            label=f'{quiz.subject}',
            choices=[(1, quiz.answer), (2, quiz.wrong)],
            widget=forms.RadioSelect,
            required=True,
            error_messages={'required': f'You must answer question'}
        )


