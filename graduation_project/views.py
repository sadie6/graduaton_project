from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from student.models import Administrator
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = Administrator.objects.get(user_id = username)
        except:
            return HttpResponse("username is Invalid")
        if (user and user.password == password):
            request.session['status'] = 1 
            request.session['user_id'] = username
        else:
            request.session['status'] = 0
            return HttpResponse('Invalid username or password!')
        if request.session['status'] == 1:
            return HttpResponseRedirect('/student/')
        else:
            return HttpResponse('you dont have login')
        

def logout(request):
    request.session.clear()
    return render(request,'login.html')

