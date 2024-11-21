var by = function(a) {
    return function(c, e) {
        var h, g;
        if ("object" === typeof c && "object" === typeof e && c && e) return h = c[a], g = e[a], 
        h === g ? 0 :typeof h === typeof g ? h < g ? -1 :1 :typeof h < typeof g ? -1 :1;
        throw "error";
    };
}, requestCount = 0, keyvalueOld = "", regNum = /^[0-9]*[0-9][0-9]A*$/, regEn = /^[A-Za-z]+$/, regCn = RegExp("[一-龥]"), requestOccur = 0;

function searchJudge(a) {
    "输入景点名、城市名 查天气" != a ? readData(a, 0) :hide();
}

$(document).ready(function() {
$(".more_li").hover(function(){
			$(".weather_li_open").show();	
		},function(){
			$(".weather_li_open").hide();		
		})
$(".city-tt a").click(function(){
	
		$(this).addClass("cur").siblings().removeClass("cur");
		$(".w_city").eq($(".city-tt a").index($(this))).show().siblings(".w_city").hide();
	})
	$(".text").click(function(){
		$(".city-box").addClass("show_head").show();
	})

	
    $("#txtZip").focus(function() {
              $(".city-box").show();

        if ("" == $("#txtZip").val() || "输入景点名、城市名 查天气" == $("#txtZip").val()) $("#idss").show(), 
        hide();
        $(this).val() == this.defaultValue ? $(this).val("") :"" != $("#txtZip").val() && "输入景点名、城市名 查天气" != $("#txtZip").val() && $("#show").show();
        setInterval(function() {
            var a = $("#txtZip").val();
            "" == a && hide();
            a != keyvalueOld && ($("#idss").hide(), searchJudge(a));
        }, 300);
       $('#idss').load('/profile/search_addition1.html');
      $(".city-box").show();
    });
    $(document).click(function() {
        "" == $("#txtZip").val() ? ($("#show").hide(), $("#txtZip").val("输入景点名、城市名 查天气")) :($("#show").hide());
        $("#idss").hide();
      
      if($(".city-box").hasClass("show_head")){
		$(".city-box").removeClass("show_head").hide();
		}

    });
    $("#txtZip").add("#selectsionTabs").click(function(a) {
        a.stopPropagation();
        return !1;
    });
    $("#selectsionTabs span").click(function() {
        var a = $("#selectsionTabs span").index(this);
        $("#selectsionGroups ul").hide();
        $("#selectsionGroups ul").eq(a).show();
        $("#selectsionTabs span").removeClass("active");
        $(this).addClass("active");
    });
    $("#selectsionTabs .tab").click(function() {
        event.stopPropagation();
        return !1;
    });
    $("#btnZip").bind("click", function(a) {
        a.stopPropagation();
        a = $("#txtZip").val();
        if ("" == a || "输入景点名、城市名 查天气" == $.trim(a)) return window.location = "http://www.weather.com.cn/forecast/index.shtml", 
        !1;
        readData(a, 1);
    });
    $("#txtZip").keyup(function(a) {
        var c = $("#txtZip");
        c.offset();
        c.height();
        "" == $("#txtZip").val() && (keyvalueOld = "");
        keysearch(a);
    });
});

function readData(a, c) {
    keyvalueOld = a;
    $.ajax({
        type:"GET",
        url:"http://toy1.weather.com.cn/search?cityname=" + a + "",
        dataType:"jsonp",
        requestCount:++requestCount,
        jsonp:"callback",
        jsonpCallback:"success_jsonpCallback",
        timeout:3e3,
        async:!1,
        success:function(e) {
            requestCount === this.requestCount && (0 == c && ("" == e ? ($("#show ul").html("<span style='color:#f00;'>对不起，未找到您查询的城市天气!</a></span>"), 
            $("#show").show()) :displayData(a, e)), 1 == c && ("" == e ? window.location = "http://www.weather.com.cn/forecast/index.shtml" :(displayData(a, e), 
            areaid = $("#show li.select").attr("num"), regEn.test(areaid) && (window.location = "http://www.weather.com.cn/html/province/" + areaid + ".shtml"), 
            regNum.test(areaid) && (window.location = "http://www.weather.com.cn/weather1d/" + areaid + ".shtml"))));
        },
        error:function() {
            1 == c && (window.location = "http://www.weather.com.cn/weather1d/" + areaid + ".shtml");
        }
    });
}

function displayData(a, c) {
    var e = [];
    $.each(c, function(a, b) {
        e[a] = b.ref.split("~");
    });
    var h = e.sort(by("0")), g = "", f = "";
    regNum.test(a) && $.each(h, function(j, b) {
        var d = b[2] + "-" + b[9], c = RegExp(a, "ig");
        c.test(b[6]) && (d += "-" + b[6]);
        c.test(b[7]) && (d += "-" + b[7]);
        d = d.replace(c, "<b>" + a + "</b>");
        0 == j && (f += '<li class="select" num=' + b[0] + ">" + d + "</li>");
        12 > j && 0 < j && (f += '<li class="unselect" num=' + b[0] + ">" + d + "</li>");
        if (11 == j) return !1;
    });
    regEn.test(a) && $.each(h, function(j, b) {
        var d = "" != b[9] ? b[2] + "-" + b[9] :b[2], c = RegExp(a, "ig");
        c.test(b[3]) && (d += "-" + b[3]);
        c.test(b[5]) && (d = b[2] + "-" + b[9] + "-" + b[5]);
        d = d.replace(c, "<b>" + a + "</b>");
        c.test(b[8]) && (d += "-<b>" + b[8].toUpperCase() + "</b>");
        0 == j && (f += '<li class="select" num=' + b[0] + ">" + d + "</li>");
        12 > j && 0 < j && (f += '<li class="unselect" num=' + b[0] + ">" + d + "</li>");
        if (11 == j) return !1;
    });
    regCn.test(a) && $.each(h, function(c, b) {
        var d = "" != b[9] ? b[2] + "-" + b[9] :b[2], e = RegExp(a, "ig"), e = RegExp(a, "ig"), d = d.replace(e, "<b>" + a + "</b>");
        0 == c && (f += '<li class="select" num=' + b[0] + ">" + d + "</li>");
        12 > c && 0 < c && (f += '<li class="unselect" num=' + b[0] + ">" + d + "</li>");
        if (11 == c) return !1;
    });
    $("#show ul").html(f);
    $("#show").show();
    $("#show li").mouseover(function() {
        $("#show li.select").removeClass("select").addClass("unselct");
        $(this).removeClass("unselect").addClass("select");
    }).mouseout(function() {
        $(this).removeClass("select").addClass("unselect");
    }).click(function() {
        var a = $("#show li.select").text(), a = a.split("-");
        g = $("#show li.select").attr("num");
        regEn.test(g) && (window.location = "http://www.weather.com.cn/html/province/" + g + ".shtml");
        regNum.test(g) && (window.location = "http://www.weather.com.cn/weather1d/" + g + ".shtml");
        1 < a.length && $("#txtZip").val(a[0]);
        hide();
    });
}

function hide() {
    $("#show").hide();
}

function keysearch(a) {
    38 == a.keyCode || 40 == a.keyCode || 13 == a.keyCode || 27 == a.keyCode || 9 == a.keyCode ? (40 == a.keyCode && ("" != $("#show li.select").next().text() ? $("#show li.select").removeClass("select").addClass("unselect").next().removeClass("unselect").addClass("select") :($("#show li.select").removeClass("select").addClass("unselect"), 
    $("#show li:first").removeClass("unselect").addClass("select"))), 38 == a.keyCode && ("" != $("#show li.select").prev().text() ? $("#show li.select").removeClass("select").addClass("unselect").prev().removeClass("unselect").addClass("select") :($("#show li.select").removeClass("select").addClass("unselect"), 
    $("#show li:last").removeClass("unselect").addClass("select"))), 13 == a.keyCode && (a = $("#show li.select").text(), 
    a = a.split("-"), areaid = $("#show li.select").attr("num"), regEn.test(areaid) && (window.location = "http://www.weather.com.cn/html/province/" + areaid + ".shtml"), 
    regNum.test(areaid) && (window.location = "http://www.weather.com.cn/weather1d/" + areaid + ".shtml"), 
    1 < a.length && $("#txtZip").val(a[0]), hide())) :0 == $("#txtZip").val().length && hide();
}
