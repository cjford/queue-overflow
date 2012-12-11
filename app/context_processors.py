def login_form(request):
  from app.forms import LoginForm
  form = LoginForm(initial={'current_page':request.path})
  #form = LoginForm(initial={'redirect':request.META['HTTP_REFERER']})
  return {'login_form':form}
