from django import forms


    
# forms.py
class BinomialForm(forms.Form):
    n = forms.IntegerField(label='Nombre d\'essais', initial=10, min_value=1,widget=forms.NumberInput(attrs={'class': 'form-control '}))
    p = forms.FloatField(label='Probabilité de succès', initial=0.5, min_value=0, max_value=1,widget=forms.NumberInput(attrs={'class': 'form-control'}))

class BernoulliForm(forms.Form):
    p = forms.FloatField(label='Probabilité de succès', initial=0.5, min_value=0, max_value=1,widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    
class NormaleForm(forms.Form):
    mean = forms.FloatField(label='Moyenne',widget=forms.NumberInput(attrs={'class': 'form-control'}))
    std_dev = forms.FloatField(label='Écart-type',widget=forms.NumberInput(attrs={'class': 'form-control'}))
    

class PoissonForm(forms.Form):
    lambda_param = forms.FloatField(label='Paramètre lambda',widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
class UniformeForm(forms.Form):
    a = forms.FloatField(label='Limite inférieure (a)',widget=forms.NumberInput(attrs={'class': 'form-control'}))
    b = forms.FloatField(label='Limite supérieure (b)',widget=forms.NumberInput(attrs={'class': 'form-control'}))

class ExponentielleForm(forms.Form):
    beta = forms.FloatField(label='Paramètre beta',widget=forms.NumberInput(attrs={'class': 'form-control'}))

    
class TraitementForm(forms.Form):
    valeurs = forms.CharField(label='Liste de valeurs', widget=forms.TextInput(attrs={'placeholder': 'Entrez les valeurs séparées par des tirets (-) ou des virgules (,)'}))
