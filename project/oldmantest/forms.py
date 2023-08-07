from django import forms

class RadioForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')  # 데이터베이스에서 가져온 질문들
        super(RadioForm, self).__init__(*args, **kwargs)
        
        for index, question in enumerate(questions,start=1):
            field_name = f'question_{question}'
            self.fields[field_name] = forms.ChoiceField(
                label=f'question_{index}',
                choices=[(1, '동의'), (2, '비동의')],
                widget=forms.RadioSelect,
                required=True,
                error_messages={'required': f'You must answer question: {index}'}
            )
