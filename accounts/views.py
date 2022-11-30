import random
from typing import Union

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
	login as django_login, 
	logout as django_logout, 
	update_session_auth_hash,
	get_user_model,
)
from django.contrib.auth.decorators import login_required
from django.http import (
	HttpResponse, HttpResponseRedirect, HttpRequest, JsonResponse,
)
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from rest_framework import status

from core.decorators import logout_required

from accounts.forms import (
	LoginForm, SignupForm, 
	ProfileDetailForm, ProfileEditForm,
	PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)

RedirectOrResponse = Union[HttpResponseRedirect, HttpResponse]

User = get_user_model()

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
    return render(request, 'accounts/container/password_change.html', {
        'form': form,
        'app_name': 'change_password'
    })

@logout_required
def password_find(request: HttpResponse) -> HttpResponse:
	''' 비밀번호 찾기 '''

	form = PasswordResetForm()
	email_auth_url = reverse('password_find_email_authenticate')
	auth_confirm_url = reverse('auth_confirm')

	return render(request, 'accounts/container/password_find.html', {
		'form':form,
		'email_auth_url': email_auth_url,
		'auth_confirm_url': auth_confirm_url
	})

@logout_required
def password_find_email_authenticate(request: HttpResponse) -> JsonResponse:
	''' 비밀번호 찾기 인증 메일 발송 '''

	if request.method == 'POST':
		username = request.POST.get('username')
		target_user = get_object_or_404(User, username=username)
		
		#TODO: 1. 메일 발송 비동기로 처리 / 2. 메일을 문자 발송으로 변경

		if target_user:
			auth_num = int(''.join(map(str, random.sample(range(0, 9), 6))))
			print(auth_num)
			target_user.auth_number = auth_num
			target_user.save()

			send_mail(
				'비밀번호 찾기 인증메일입니다.',
				recipient_list=[target_user.email],
				from_email=settings.EMAIL_HOST_USER,
				message='',
				html_message=render_to_string(
					'accounts/container/password_find_email_authenticate.html', 
					{
						'auth_num': auth_num,
						'site_name': 'Site Name' # 사이트명 수정 하드코딩된거 수정 필요
					}
				),
				fail_silently=True
			)

			data = {'uuid': str(target_user.uuid)}

			return JsonResponse(data=data, status=status.HTTP_200_OK)

		return JsonResponse(
			data={'error': '404 (Not Found)'}, status=status.HTTP_404_NOT_FOUND)

	return JsonResponse(
		data={'error': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@logout_required
def auth_confirm(request: HttpResponse) -> JsonResponse:
	''' 인증번호 확인 '''

	if request.method == 'POST':
		user_uuid = request.POST.get('user_uuid')
		auth_num = request.POST.get('auth_num')
		print(user_uuid, auth_num)
		target_user = get_object_or_404(User, uuid=user_uuid, auth_number=auth_num)

		if target_user:
			target_user.auth_number = None
			target_user.save()

			data = {'url': reverse('password_reset', args=[target_user.uuid])}

			return JsonResponse(data, status=status.HTTP_200_OK)
		
		return JsonResponse(
			data={'error': '404 (Not Found)'}, status=status.HTTP_404_NOT_FOUND)

	return JsonResponse(
		data={'error': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@logout_required
def password_reset(request: HttpResponse, uuid: str) -> RedirectOrResponse:
	''' 비밀번호 재설정 '''

	if request.method == 'POST':
		current_user = get_object_or_404(User, uuid=uuid)
		django_login(request, current_user)

		form = SetPasswordForm(request.user, request.POST)
		
		if form.is_valid():
			form.save()
			messages.success(request, "비밀번호가 변경되었습니다. 변경된 비밀번호로 로그인하세요.")
			django_logout(request)
			return redirect(settings.LOGIN_URL)
	else:
		form = SetPasswordForm(request.user)

	return render(request, 'accounts/container/password_reset.html', {
		'form': form
	})