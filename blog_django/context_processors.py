from accounts.forms import RegisterUserForm

def brand_processor(request):
    brand_first_word = 'Blog'
    brand_second_word = 'Django'
    return {
        'brand_first_word' : brand_first_word,
        'brand_second_word' : brand_second_word
    }

def account_processor(request):
    register_user_form = RegisterUserForm()
    return {
        'register_user_form' : register_user_form,
    }