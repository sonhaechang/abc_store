from django.shortcuts import redirect
from django.contrib import messages


def logout_required(function):
	''' 로그아웃 상태인지 확인 '''

	def wrap(request, *args, **kwargs):
		if request.user.is_authenticated:
			messages.error(request, '로그아웃이여야 합니다.')
			return redirect('/')
		return function(request, *args, **kwargs)
	return wrap