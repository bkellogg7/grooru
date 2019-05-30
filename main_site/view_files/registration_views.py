from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ..models import User
from ..forms import UserForm

def register(request):
    template ="register.html"
    if request.method == "GET":
        form = UserForm()
        context = {"form":form}
        return render(request, template, context)
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect("/")
        else:
            context = {"form":form}
            return render(request, template, context)
    return redirect("/")
