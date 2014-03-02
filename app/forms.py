from django import forms

class SignUpForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(
                                        attrs={'placeholder':'Password'}))
    email = forms.EmailField(widget=forms.TextInput(
                                        attrs={'placeholder':'Email'}),
    							        max_length=50)
    cell = forms.CharField(widget=forms.TextInput(
                                        attrs={'placeholder':'Cell'}),
    						            max_length=30)


class AddBandForm(forms.Form):
    band = forms.CharField(widget=forms.TextInput(
                                    attrs={'placeholder':'Add kick-ass band'}),
    						        max_length=100,
    					   	        required=True)


class LoginForm(forms.Form):
    username = forms.EmailField(widget=forms.TextInput(
                                            attrs={'placeholder':'Email'}),
    							            max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(
                                            attrs={'placeholder':'Password'}))