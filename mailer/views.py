from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.http import JsonResponse, Http404
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from .forms import UserCreateForm, SendMailForm
from django import forms


class SendMailFormView(FormView):
    template_name = 'index.html'
    form_class = SendMailForm
    success_url = '/'

    def form_valid(self, form):
        subject = 'Message from %s' % (self.request.user)
        message = self.request.POST.get('message')
        from_email = self.request.user.email
        to_email = self.request.POST.get('email')
        try:
            status = send_mail(
                subject,
                message,
                from_email,
                [to_email],
                fail_silently=True
            )
            if status:
                status = 'Success'
            else:
                status = 'Fail'
        except:
            status = 'Fail'
        form.save(self.request.user, status)
        return super(SendMailFormView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(SendMailFormView, self).form_invalid(form)


class AuthViewHelper(FormView):

    def get_success_url(self):
        return reverse('index')

    def form_invalid(self, form):
        if self.request.is_ajax():
            response = {
                'html': render_to_string(
                    'registration/auth_form_ajax.html',
                    {'form': form},
                    request=self.request,
                )
            }
            return JsonResponse(response, status=400)
        else:
            raise Http404


class LoginView(AuthViewHelper):
    template_name = 'registration/auth_form_login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        if self.request.is_ajax():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(self.request, user)
                return JsonResponse({'url': super(LoginView, self).get_success_url()})
        else:
            raise Http404


class SignUpView(AuthViewHelper):
    template_name = 'registration/auth_form_register.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        if self.request.is_ajax():
            form.save()
            return JsonResponse({'url': super(SignUpView, self).get_success_url()})
        else:
            raise Http404


def logout_view(request):
    logout(request)
    return redirect('index')
