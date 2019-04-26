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





def manage(request):
    user_id = int(request.session.get('user_id'))
    if user_id == 1001:
        roles = Administrator.objects.all()
        return render(request, 'price.html', {'roles': roles})
    else:
        return render(request, 'handle.html', {'error': "抱歉，你没有权限！！"})


def delete_role(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id != '1001':
            Administrator.objects.filter(user_id=user_id).delete()
        else:
            return HttpResponse(0)
    return HttpResponseRedirect('/manage/')



def update_role(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        Administrator.objects.filter(user_id=user_id).update(password=password)
    return HttpResponseRedirect('/manage/')



def insert_role(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        Administrator.objects.create(user_id=user_id,password=password)
    return HttpResponseRedirect('/manage/')

