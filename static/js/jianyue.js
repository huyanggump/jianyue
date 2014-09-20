/**
 * Created by boyang on 2014/8/6.
 */
$(document).ready(function(){
	$('#qappt').click(function(){
		$.post("/appointment/quick/",{"name":"dingboyang","phone":"18844195718","sex":"Male","longitude":23.4576786,"latitude":24.67867698},
			function(parameters){
                var data = parameters.data;
				$('#text').text(data);
			});
	});
	$('#nappt').click(function(){
		$.post("/appointment/normal/",{"longitude":23.4576786,"latitude":24.67867698,"date":"2014.06.30"},
			function(parameters){
                var data = parameters.data;
				$('#text').text(data);
			});
	});
	$('#isreg').click(function(){
		$.post("customer/isregister/",{"phone":"18844195718"},
			function(parameters){
                var data = parameters.data;
				$('#text').text(data);
			});
	});
	$('#subord').click(function(){
		$.post("/appointment/normal/submit-order/",{"cusphone":"18844195718","cusname":"dingboyang","sex":"Male","hairstyle":"short","remark":"short more","distance":500,"barphone":"18844195719","time":"2014.7.12;6.20-6.40"},
			function(parameters){
                var data = parameters.data;
				$('#text').text(data);
			});
	});
	$('#accord').click(function(){
		$.post("/appointment/quick/order-accepted/",{"orderID":1,"phone":"18844195719"},
			function(parameters){
                var data = parameters.data;
				$('#text').text(data);
			});
	});
});