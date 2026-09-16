from django.shortcuts import redirect


def librarian_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.groups.filter(name="Librarian").exists():
            return view_func(request, *args, **kwargs)

        return redirect("book_list")

    return wrapper