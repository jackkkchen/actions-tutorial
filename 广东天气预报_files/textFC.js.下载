$(document).ready(function(){
	$(".day_tabs li").click(function(){
		var tab=$(".day_tabs li").index(this);
		$(".day_tabs li").removeClass("selected");
		$(this).addClass("selected");
		$(".hanml:visible .conMidtab").hide().eq(tab).show();
		return false;
	});
	$(".conMidtab .conMidtab2 table").each(function(){
		$(this).find("tr:even").css("background-color","#fff");
		$(this).find("tr:odd").css("background-color","#F3F3F5");
	
	});
	$(".conMidtab .conMidtab3 table:even tr").css("background-color","#ffffff").find(".rowsPan").css("background-color","#ffffff");
	$(".conMidtab .conMidtab3 table:odd tr").css("background-color","#F3F3F5").find(".rowsPan").css("background-color","#F3F3F5");
	$(".conMidtab .conMidtab2 table tr").hover(function(){
		$(this).css("background-color","#E6F3FC");
		},function(){
		$(this).parent().find("tr:even").css("background-color","#fff");
		$(this).parent().find("tr:odd").css("background-color","#F3F3F5");
	});
	$(".conMidtab .conMidtab3 table tr").hover(function(){
		$(this).data("bgcolor",$(this).css("background-color"));
		$(this).css("background-color","#E6F3FC");
		},function(){
		$(this).css("background-color",$(this).data("bgcolor"));
	});
$(".lqcontentBoxheader ul").eq(0).find("li").eq(1).find("a").text("安徽");
});
