
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("book_list")

        return render(request, "accounts/login.html", {
            "error": "Invalid username or password."
        })

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def register_view(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            member_group, created = Group.objects.get_or_create(
                name="Member"
            )

            user.groups.add(member_group)

            return redirect("login")

    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {
        "form": form
    })
