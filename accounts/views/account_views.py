from typing import Union

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, redirect

from accounts.forms import ProfileDetailForm, ProfileEditForm

RedirectOrResponse = Union[HttpResponseRedirect, HttpResponse]

User = get_user_model()


# Create your views here.
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