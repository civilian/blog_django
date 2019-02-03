from accounts.forms import ( 
                        SignUpUserForm, BlogAuthenticationForm )

def account_processor(request):
    signup_user_form = SignUpUserForm(auto_id='id_signup_%s')
    login_form = BlogAuthenticationForm(auto_id='id_login_%s')
    return {
        'signup_user_form' : signup_user_form,
        'login_form' : login_form,
    }