from accounts.forms import SignUpUserForm

def brand_processor(request):
    brand_first_word = 'Blog'
    brand_second_word = 'Django'
    return {
        'brand_first_word' : brand_first_word,
        'brand_second_word' : brand_second_word
    }

def account_processor(request):
    sign_up_user_form = SignUpUserForm()
    return {
        'sign_up_user_form' : sign_up_user_form,
    }