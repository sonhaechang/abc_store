function checkChangePasswordInput(self) {
	const oldPasswd = document.getElementById('id_old_password').value;
	const newPasswd = document.getElementById('id_new_password1').value;
	const newPasswd2 = document.getElementById('id_new_password2').value;
	const btn = document.getElementById('change-password-btn');

	if ( oldPasswd && newPasswd && newPasswd2 ) {
		btn.removeAttribute("disabled");
	} else {
		btn.setAttribute("disabled", true);
	}
};