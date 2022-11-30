function count_down(minutes, seconds) {
	const eleName = document.getElementById('timeset');
	let endTime, hours, mins, msLeft, time;

	function twoDigits(n) {
		return (n <= 9 ? "0" + n : n); 
	};

	function updateTimer() {
		msLeft = endTime - (+new Date);
		if ( msLeft < 1000 ) {
			alert("인증시간이 초과되었습니다.");
			eleName.remove();
			location.href = location.href;
		} else {
			time = new Date( msLeft );
			hours = time.getUTCHours();
			mins = time.getUTCMinutes();
			eleName.innerHTML = (hours ? hours + ':' + twoDigits(mins) : twoDigits(mins)
				+ ':' + twoDigits(time.getUTCSeconds()));
			setTimeout(updateTimer, time.getUTCMilliseconds() + 500);
		}
	};

	endTime = (+new Date) + 1000 * (60 * minutes + seconds) + 500;
	updateTimer();
};

class PasswordFind {
	constructor() {
		this.email_auth_url = email_auth_url;
		this.auth_confirm_url = auth_confirm_url;
		this.username = document.getElementById("id_username");
		this.auth_num_form_block = document.getElementById('auth_num_form_block');

		axios.defaults.xsrfCookieName = 'csrftoken';
		axios.defaults.xsrfHeaderName = 'X-CSRFToken';
	}

	makeFormElements() {
		return `<form id="id_auth_confirm">
			<div class="form-group">
				<div class="auth_num_block mt-2" style="position: relative">
					<label for="id_auth_num" class="id_auth_num_label">
						인증번호 입력 (<span id="timeset"></span>)
					</label>
					<input 
						type="number" 
						id="id_auth_num" 
						class="form-control" 
						autocomplete="off"
						autofocus/>
				</div>
			</div>
			
			<input type="submit">
				인증확인
			</input>
		</form>`;
	}

	check_activate() {
		const focusEle = document.activeElement,
			authNum = document.getElementById('id_auth_num'),
			authNumLabel = document.querySelector('.id_auth_num_label');
	
		if ( authNum === focusEle || authNum.value !== '' ) {
			authNumLabel.setAttribute('style','transform:translateY(-100%)');
		} else {
			authNumLabel.setAttribute('style','transform:translateY(0%)');
		}
	}
	
	handle_auth_num_input_event() {
		const authNum = document.getElementById('id_auth_num');
	
		if ( authNum ) {
			document.body.addEventListener('click', () => this.check_activate());
		}
	}

	email_authenticate_confirm(user_uuid) {
		document.getElementById('id_auth_confirm').addEventListener('submit', e => {
			e.preventDefault();
			
			const auth_num = document.getElementById('id_auth_num');
			const data = new FormData();
			data.append('auth_num', auth_num.value);
			data.append('user_uuid', user_uuid);

			console.log(auth_num.value);
			console.log(user_uuid);
			console.log(this.auth_confirm_url);

			axios.post(this.auth_confirm_url, data)
				.then(function (response) {
					alert('인증되었습니다. 비밀번호를 재설정 해주세요.');
					location.href = response.data.url;
				})
				.catch(function (err) {
					console.log(err)
					if (auth_num === "") {
						alert('회원님의 이메일로 전송된 인증번호를 입력해주세요.');
					} else {
						alert('인증번호가 일치하지 않습니다.');
					}
				})
		})
	}

	send_email_authenticate(e, self) {
		e.preventDefault();

		const data = new FormData();
		data.append('username', this.username.value)  

		axios.post(self.email_auth_url, data)
			.then(function (response) {
				alert('회원님의 이메일로 인증코드를 발송하였습니다.');
				e.target.remove();
				self.auth_num_form_block.innerHTML = self.makeFormElements();
				count_down(5, 0);
				console.log(response.data.uuid);
				self.email_authenticate_confirm(response.data.uuid);
				self.handle_auth_num_input_event();
				self.check_activate();
			})
			.catch(function (err) {
				console.error(err);
			})
	}
}

const pw_find_form = document.getElementById('password-find-form');
const pw_find = new PasswordFind();

pw_find_form.addEventListener('submit', e => pw_find.send_email_authenticate(e, pw_find));
pw_find.handle_auth_num_input_event();