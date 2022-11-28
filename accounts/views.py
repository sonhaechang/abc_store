from typing import Union

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as django_login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect

from core.decorators import logout_required

from accounts.forms import (
	LoginForm, SignupForm, 
	ProfileDetailForm, ProfileEditForm,
	PasswordChangeForm,
)

RedirectOrResponse = Union[HttpResponseRedirect, HttpResponse]


# Create your views here.
@logout_required
def login(request: HttpRequest) -> RedirectOrResponse:
	''' 로그인 '''

	if request.method == 'POST':
		# 로그인 성공 후 이동할 URL. 주어지지 않으면 None
		next_url = request.GET.get('next')

		form = LoginForm(request=request, data=request.POST)
		if form.is_valid():
			user = form.get_user()

			# Django의 auth앱에서 제공하는 login함수를 실행해 앞으로의 요청/응답에 세션을 유지한다
			django_login(request, user)

			# next_url가 존재하면 해당 위치로, 없으면 메인 목록 화면으로 이동
			return redirect(next_url if next_url else '/')

		# 인증에 실패하면 login_form에 non_field_error를 추가한다
		form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
	else:
		form = LoginForm()
		next_url = request.GET.get('next')

	return render(request, 'accounts/container/login.html', {
		'form': form
	})

@logout_required
def signup(request: HttpRequest) -> RedirectOrResponse:
	''' 회원가입  '''

	if request.method =='POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(settings.LOGIN_URL)
	else:
		form = SignupForm()

	return render(request, 'accounts/container/signup.html', {
		'form': form,
	})

@login_required
def profile(request: HttpResponse) -> RedirectOrResponse:
	''' 프로필 확인 '''

	form = ProfileDetailForm(instance=request.user)

	return render(request, 'accounts/container/profile.html', {
        'form': form,
    })

@login_required
def profile_edit(request: HttpResponse) -> RedirectOrResponse:
	''' 프로필 수정 '''

	if request.method == 'POST':
		form = ProfileEditForm(request.POST, instance=request.user)

		if form.is_valid():
			form.save()
			return redirect('/accounts/profile')
	else:
		form = ProfileEditForm(instance=request.user)

	return render(request, 'accounts/container/profile_edit.html', {
		'form': form,
	})

@login_required
def password_change(request: HttpResponse) -> RedirectOrResponse:
    ''' 비밀번호 변경 '''

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
            return redirect('profile')
        else:
            messages.error(request, '아래 오류를 수정하십시오.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/container/change_password.html', {
        'form': form,
        'app_name': 'change_password'
    })