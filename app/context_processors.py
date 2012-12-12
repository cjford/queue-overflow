def login_form(request):
  from app.forms import LoginForm
  form = LoginForm(initial={'current_page':request.path})
  return {'login_form':form}
