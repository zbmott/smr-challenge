
# Create your views here.

import json

from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import generic
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_POST

from messageboard import forms as messageboard_forms
from messageboard.models import Like

User = get_user_model()


class JsonFormView(generic.View):
    form_class = None

    @method_decorator(require_POST)
    def post(self, request):
        try:
            form = self.form_class(json.loads(request.body))
        except ValueError:
            return HttpResponseBadRequest()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        raise NotImplementedError()

    def form_invalid(self, form):
        return JsonResponse({
            'status': 400,
            'errors': form.errors
        })


class Login(JsonFormView):
    form_class = messageboard_forms.LoginForm

    def form_valid(self, form):
        user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
        if user is not None:
            login(self.request, user)
            return JsonResponse({
                'status': 200,
                'user': {
                    'username': user.username,
                    'anonymous': user.is_anonymous()
                }
            })

        return JsonResponse({'status': 403})


class CreateAccount(JsonFormView):
    form_class = messageboard_forms.CreateAccountForm

    def form_valid(self, form):
        user = User(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email']
        )
        user.set_password(form.cleaned_data['password'])

        try:
            user.save()
        except IntegrityError:
            return JsonResponse({'status': 400})

        return JsonResponse({
            'status': 200
        })


@method_decorator(require_GET, name='get')
class Logout(generic.View):
    def get(self, request):
        logout(request)
        return JsonResponse({
            'status': 200,
            'user': {
                'anonymous': True
            }
        })


@method_decorator(require_GET, name='get')
class WhoAmI(generic.View):
    def get(self, request):
        if request.user.is_authenticated():
            user = {
                'pk': request.user.pk,
                'username': request.user.username,
                'anonymous': False,
                # list() coerces the queryset into a list, which
                # is JSON-serializable. values_list avoids overhead
                # associated with instantiating model instances.
                'likedPosts': list(Like.objects.filter(
                    user=request.user
                ).values_list('topic_id', flat=True))
            }
        else:
            user = {
                'anonymous': True
            }

        return JsonResponse({'status': 200, 'user': user})
