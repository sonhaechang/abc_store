document.getElementById('order-pay').addEventListener('submit', e => {
	e.preventDefault();

	const form = e.currentTarget;
	const data = new FormData(form);
	let params = {};

	for (var d of data.entries()) { params[d[0]] = d[1] }

	params['name'] = document.getElementById('imp-js').getAttribute('order-name');
	params['amount'] = document.getElementById('total-amount').getAttribute('data-value');
	delete params['imp_uid'];
	delete params['detail_addr'];

	IMP.init(document.getElementById('imp-js').getAttribute('imp-id'));
	IMP.request_pay(params, function(response){
		if ( response.success ) {
			document.getElementById('id_imp_uid').value = response.imp_uid;
			form.submit();
		} else {
			console.log(response);
			alert(`${response.error_msg}(${response.error_code})`);
		}
	});
});