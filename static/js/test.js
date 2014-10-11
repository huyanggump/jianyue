$(document).ready(function(){
	$('#quickappt').click(function(){
		$.post("/appointment/quick/",{"name":$("#form-quickappt-name")[0].value,"phone":$("#form-quickappt-phone")[0].value,"sex":$("#form-quickappt-sex")[0].value,"longitude":$("#form-quickappt-longitude")[0].value,"latitude":$("#form-quickappt-latitude")[0].value},
			function(parameters){
                var data = parameters.data;
				$('#text').text(data);
			});
	});
	$('#normalappt').click(function(){
		$.post("/appointment/normal/",{"longitude":$("#form-normalappt-longitude")[0].value,"latitude":$("#form-normalappt-latitude")[0].value,"date":$("#form-normalappt-date")[0].value},
			function(parameters){
                var data = parameters.data;
				$('#text').text(data);
			});
	});
	$('#subord').click(function(){
		$.post("/appointment/normal/submit-order/",{"cusphone":$("#form-subord-cusphone")[0].value,"cusname":$("#form-subord-name")[0].value,"sex":$("#form-subord-sex")[0].value,"barphone":$("#form-subord-barphone")[0].value,"hairstyle":$("#form-subord-hairstyle")[0].value,"time":$("#form-subord-time")[0].value,"distance":$("#form-subord-distance")[0].value,"remark":$("#form-subord-remark")[0].value},
			function(parameters){
                var data = parameters.data;
				$('#text').text(data);
			});
	});
	$('#isregister').click(function(){
		$.post("/customer/isregister/",{"phone":$("#form-isregister-phone")[0].value},
			function(parameters){
                var data = parameters.data;
				$('#text').text(data);
			});
	});
	$('#ordaccepted').click(function(){
		$.post("/appointment/quick/order-accepted/",{"orderID":$("#form-ordaccepted-id")[0].value,"phone":$("#form-ordaccepted-phone")[0].value,"distance":$("#form-ordaccepted-distance")[0].value},
			function(parameters){
                var data = parameters.data;
				$('#text').text(data);
			});
	});
	$('#baregister').click(function(){
		$.post("/barber/register/",{"name":$("#form-baregister-name")[0].value,"phone":$("#form-baregister-phone")[0].value,"sex":$("#form-baregister-sex")[0].value,"shop":$("#form-baregister-shop")[0].value,"time":$("#form-baregister-time")[0].value,"password":$("#form-baregister-password")[0].value},
			function(parameters){
                var data = parameters.data;
				$('#text').text(data);
			});
	});
    $('#get-near-shop').click(function(){
		$.post("/get-near-shop/",{"longitude":$("#form-get-longitude")[0].value,"latitude":$("#form-get-latitude")[0].value},
			function(parameters){
                var data = parameters.data;
				$('#text').text(data);
			});
	});
    $('#barlogin').click(function(){
		$.post("/barber/login/",{"phone":$("#form-barlogin-phone")[0].value,"password":$("#form-barlogin-password")[0].value},
			function(parameters){
                var data = parameters.data;
				$('#text').text(data);
			});
	});
    $('#barset').click(function(){
		$.post("/barber/set-time/",{"phone":$("#form-barset-phone")[0].value,"time":$("#form-barset-time")[0].value},
			function(parameters){
                var data = parameters.data;
				$('#text').text(data);
			});
	});

    $('#bar-is-register').click(function(){
		$.post("/barber/isregister/",{"phone":$("#form-bar-isregister-phone")[0].value},
			function(parameters){
                var data = parameters.data;
				$('#text').text(data);
			});
	});
    $('#getbarber').click(function(){
		$.post("/appointment/get/barber/",{"phone":$("#form-getbarber-phone")[0].value, "date":$("#form-getbarber-date")[0].value},
			function(parameters){
                var data = parameters.data;
				$('#text').text(data);
			});
	});
    $('#update-cus').click(function(){
		$.post("/update/customer/profile/",{"phone":$("#form-update-cus-phone")[0].value},
			function(parameters){
                var data = parameters.data;
				$('#text').text(data);
			});
	});

});