from django.utils import timezone
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import modelTask
from .forms import taskForm
from django.contrib.auth.decorators import login_required


def home(request):
    """
    It takes a request, and returns a rendered template

    :param request: The request is an HttpRequest object. It contains metadata about the request
    :return: The render function is being returned.
    """
    template_name = 'base.html'
    return render(request, template_name)


def userRegister(request):
    """
    If the request method is GET, render the register.html template with the UserCreationForm.
    If the request method is POST, check if the passwords match, if they do, create a user with the
    username and password, save the user, log the user in, and redirect to the task page.
    If the passwords don't match, render the register.html template with the UserCreationForm and an
    error message.
    If the user already exists, render the register.html template with the UserCreationForm and an error
    message

    :param request: The request object is the first parameter to every view function. It contains
    information about the request that was made to the server
    :return: The user is being returned.
    """
    template_name = 'register.html'
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            'form': form
        }
        return render(request, template_name, context)
    else:
        if request.POST['password1'] == request.POST['password2']:
            username = request.POST['username']
            pwd = request.POST['password1']
            try:
                user = User.objects.create_user(
                    username=username, password=pwd)
                user.save()
                login(request, user)
                return redirect('task')
            except IntegrityError:
                context = {
                    'form': UserCreationForm,
                    'error': 'User already exists'
                }
                return render(request, template_name, context)
        context = {
            'form': UserCreationForm,
            'error': 'Password do not match'
        }
        return render(request, template_name, context)

@login_required
def taskView(request):
    """
    It takes a request, gets the data from the database, and then renders the template with the data

    :param request: The request object is the first parameter to the view function. It contains
    information about the request that was made to the server
    :return: The render function is returning a HttpResponse object.
    """
    data = modelTask.objects.filter(
        user=request.user, datecompleted__isnull=True)
    context = {
        'data': data
    }
    template_name = 'tasks.html'
    return render(request, template_name, context)

@login_required
def taskCompleted(request):
    data = modelTask.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    context = {
        'data': data
    }
    template_name = 'task_completed.html'
    return render(request, template_name, context)

@login_required
def logoutView(request):
    """
    It logs out the user and redirects them to the home page

    :param request: The request is a HttpRequest object
    :return: The logoutView function is returning a redirect to the home page.
    """
    logout(request)
    return redirect('home')


def singin(request):
    """
    If the request method is GET, render the login page with the form.
    If the request method is POST, authenticate the user and redirect to the task page.

    :param request: The request object is the first parameter to every view function. It contains
    information about the request that was made to the server, such as the HTTP method, the path, the
    headers, and the body
    :return: the result of the render function.
    """
    if request.method == 'GET':
        context = {
            'form': AuthenticationForm,
        }
        return render(request, 'login.html', context)
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            context = {
                'form': AuthenticationForm,
                'error': 'User or password is incorrect'
            }
            return render(request, 'login.html', context)
        else:
            login(request, user)
            return redirect('task')

@login_required
def createTask(request):
    """
    If the request method is GET, render the create_task.html template with the taskForm. 
    If the request method is POST, save the form data to the database.

    :param request: The request object is the first parameter to every view function. It contains
    information about the request that was made to the server, such as the HTTP method, the URL, the
    headers, and the body of the request
    :return: the render function, which is a function that returns an HttpResponse object.
    """
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': taskForm
        })
    else:
        form = taskForm(request.POST)
        try:
            task_new = form.save(commit=False)
            task_new.user = request.user
            task_new.save()
            return redirect('task')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': taskForm,
                'error': 'Suministre datos válidos'
            })

@login_required
def taskDetail(request, task_id):
    """
    It takes the task_id from the URL, finds the task with that id in the database, and then passes that
    task to the template

    :param request: The request is an HttpRequest object. It contains metadata about the request, such
    as the HTTP method
    :param task_id: This is the primary key of the task we want to retrieve
    :return: The task_detail.html page is being returned.
    """
    tasksDetails = get_object_or_404(modelTask, pk=task_id, user=request.user)
    context = {
        'task': tasksDetails
    }
    return render(request, 'task_detail.html', context)

@login_required
def taskEdit(request, task_id):
    """
    If the request is a GET request, then render the task_edit.html template with the task and form
    variables. 
    If the request is a POST request, then save the form and redirect to the task page.

    :param request: The request object is the first parameter to all Django views. It contains metadata
    about the request, such as the HTTP method, the remote IP address, and the raw HTTP headers
    :param task_id: The id of the task that we want to edit
    :return: The task_edit.html page is being returned.
    """
    if request.method == 'GET':
        tasksDetails = get_object_or_404(
            modelTask, pk=task_id, user=request.user)
        form = taskForm(instance=tasksDetails)
        context = {
            'task': tasksDetails,
            'form': form
        }
        return render(request, 'task_edit.html', context)
    else:
        try:
            tasksDetails = get_object_or_404(
                modelTask, pk=task_id, user=request.user)
            form = taskForm(request.POST, instance=tasksDetails)
            form.save()
            return redirect('task')
        except ValueError:
            context = {
                'task': tasksDetails,
                'form': form,
                'error': 'No updating task'
            }
            return render(request, 'task_edit.html', context)

@login_required
def taskComplete(request, task_id):
    """
    If the request method is POST, then set the datecompleted field to the current time and save the
    task.

    :param request: The request is an HttpRequest object
    :param task_id: The primary key of the task to be completed
    :return: The task.datecompleted is being returned.
    """
    task = get_object_or_404(modelTask, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('task')

@login_required
def taskDelete(request, task_id):
    task = get_object_or_404(modelTask, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task')
