function search_postcode() {
    new daum.Postcode({
        oncomplete: function(data) {
            let addr = '';
            let extraAddr = '';

            if (data.userSelectedType === 'R') {
                addr = data.roadAddress;
            } else {
                addr = data.jibunAddress;
            }

            if (data.userSelectedType === 'R') {
                if(data.bname !== '' && /[동|로|가]$/g.test(data.bname)){
                    extraAddr += data.bname;
                }

                if(data.buildingName !== '' && data.apartment === 'Y'){
                    extraAddr += (extraAddr !== '' ? ', ' + data.buildingName : data.buildingName);
                }
            }
            // } else {
            //     document.getElementById("sample6_extraAddress").value = '';
            // }

            document.getElementById('id_postcode').value = data.zonecode;
            document.getElementById("id_address").value = addr;
            document.getElementById("id_detail_address").focus();
        }
    }).open();
}

document.getElementById('search_postcode').addEventListener('click', search_postcode);