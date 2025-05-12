from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Question, Answer

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Username'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Obrigatório. 150 caráteres ou menos. Apenas letras, dígitos e @/./+/-/_ .</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>A sua password não pode ser demasiado parecida com a sua informação pessoal.</li><li>A sua password tem que conter pelo menos 8 caratéres.</li><li>A sua password não pode ser uma que seja usada vulgarmente.</li><li>A sua password não pode conter apenas números.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Introduza a sua password novamente.</small></span>'

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body', 'image']
        
        labels = {
        	'title': 'Questão',
			'body': 'Detalhes',
            'image': 'Imagem',
		}
        
        widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título', 'rows': 2}),
			'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Texto', 'rows': 5}),
		}

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['body']
        
        labels = {
			'body': 'Resposta',
		}
        
        widgets = {
			'body': forms.Textarea(attrs={'class': 'form-control', 'title': 'Resposta', 'placeholder': 'Texto', 'rows': 5}),
		}
        
class ChallengeAnswerForm(forms.Form):
    user_answer = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resposta', 'maxlength': '255'})
    )
    
    def clean_user_answer(self):
        cleaned_data = self.cleaned_data
        user_answer = cleaned_data.get('user_answer')
        return user_answer