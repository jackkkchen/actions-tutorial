var html = "";
datalist = city_data;
for(var o in datalist){
	html+='<a href="javascript:void(0);" title='+o+'>'+o+'</a>';
}
$("#searchCityList").append(html);


function getProLevel(para1,para2){
	var cityList_city = "";
	$("#cityList_city").html("");
	if(para2==""){
		if(para1=="北京"||para1=="天津"||para1=="上海"||para1=="重庆"){
			datalist_city = city_data[para1][para1];
			for(var o in datalist_city){
				cityList_city+='<a href="http://www.weather.com.cn/weather1d/'+city_data[para1][para1][o]["AREAID"]+'.shtml#search" title='+o+'>'+o+'</a>';
			}
			setTimeout(function(){
				$(".province-level").attr('data-level', '3');
			},500)
		}else{
			datalist_city = city_data[para1];
			for(var o in datalist_city){
				cityList_city+='<a href="javascript:void(0);" data-city="'+para1+'" title='+o+'>'+o+'</a>';
			}
			$(".province-level").attr('data-level', '1');
		}
		$("#cityList_city").append(cityList_city);
		$(".province-level").text("全国");
		$(".province-area span").text(para1);
		$(".city-box-province").show();
		$("#searchCityProvince").hide();
		setTimeout(function(){
			$(".city-box-province").addClass('show_head_province');
		},500)
	}else{
		datalist_city = city_data[para1][para2];
		for(var o in datalist_city){
			cityList_city+='<a href="http://www.weather.com.cn/weather1d/'+city_data[para1][para2][o]["AREAID"]+'.shtml#search" title='+o+'>'+o+'</a>';
		}
		$("#cityList_city").append(cityList_city);
		$(".province-level").text(para1);
		$(".province-area span").text(para2);
		setTimeout(function(){
			$(".province-level").attr('data-level', '2');
			$(".city-box-province").addClass('show_head_province');
		},500)
	}
}



$("#searchCityList").on('click', 'a', function(event) {
	event.stopPropagation();
	var para1 = $(this).text();
	getProLevel(para1,"");
});
$("#cityList_city").on('click', 'a', function(event) {
	var level = $(".province-level").attr('data-level');
	if(level==1){
		event.stopPropagation();
		var para1 = $(this).attr('data-city');
		var para2 = $(this).text();
		getProLevel(para1,para2);
	}
});
$(".province-back,.province-level").on('click', function(event) {
	var level = $(".province-level").attr('data-level');
	var para1 = $(".province-level").text();
	if(para1=="全国"&&(level=="1"||level==3)){
		$(".city-box-province").hide();
		$("#searchCityProvince").show();
		setTimeout(function(){

			$("#txtZip").focus();
		},200)
	}else{
		getProLevel(para1,"");
	}
});
$(document).click(function(){
	var level = $(".province-level").attr('data-level');
	$(".search").removeClass('searchcur');
	if(level==2||level==3){
		if ($(".city-box-province").hasClass("show_head_province")) {
			$(".city-box-province").hide();
			$("#searchCityProvince").show();
		}
	}
});
var taptext = $("#txtZip").val(); //搜索框input提示语
$("#txtZip").focus(function() {
	if ($("#txtZip").val() == "" || $("#txtZip").val() == taptext) {
		if ($(".city-box-province").hasClass("show_head_province")) {
			$(".city-box-province").hide();
			$("#searchCityProvince").show();
			$(".province-level").attr('data-level', '1');

		}
		$(".search").addClass('searchcur');
	}
});
