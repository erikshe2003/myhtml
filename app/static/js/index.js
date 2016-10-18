/**
* Created by wufeng_wb on 2016/8/22.
*/
//测试代码

//ajax初始化
var ajaxHttp = new XMLHttpRequest();
//新建Date对象
var now_Date = new Date();
var expireDate = new Date();
var now_year = now_Date.getFullYear();
var now_month = now_Date.getMonth();
var year_flag = 0;
var month_flag = 12 - now_month;
//新建一个flag用于告诉页面日历的展示方向
var attendance_flag = 0;
//页面元素初始化
var browserWidth = document.documentElement.clientWidth;
var browserHeight = document.documentElement.clientHeight;
var workspace = document.getElementById('workspace');
var user_top = document.getElementById('user_top');
var user_top_name = document.getElementById('user_top_name');
var user_top_name_li = document.getElementById('user_top_name_li');
var user_top_drop_beforelogin = document.getElementById('user_top_drop_beforelogin');
var user_top_drop_loginfor = document.getElementById('user_top_drop_loginfor');
var user_top_drop_username = document.getElementById("user_top_drop_username");
var user_top_drop_password = document.getElementById("user_top_drop_password");
var user_top_drop_remember = document.getElementById("user_top_drop_remember");
var user_top_drop_afterlogin = document.getElementById('user_top_drop_afterlogin');
var user_top_drop_reset = document.getElementById('user_top_drop_reset');
var user_top_drop_logout = document.getElementById('user_top_drop_logout');
var user_resetpassword = document.getElementById('user_resetpassword');
var user_resetpassword_old = document.getElementById('user_resetpassword_old');
var user_resetpassword_new = document.getElementById('user_resetpassword_new');
var user_resetpassword_confirm =  document.getElementById('user_resetpassword_confirm');
var function_banner =  document.getElementById('function_banner');
var function_banner_1 = document.getElementById('function_banner_1');
var function_banner_1_button = document.getElementById('function_banner_1_button');
var function_banner_2_button = document.getElementById('function_banner_2_button');
var function_banner_3_button = document.getElementById('function_banner_3_button');
var home_page =  document.getElementById('home_page');
var home_page_title =  document.getElementById('home_page_title');
var attendance_page =  document.getElementById('attendance_page');
var attendance_choose_user =  document.getElementById('attendance_choose_user');
var attendance_choose_userlist =  document.getElementById('attendance_choose_userlist');
var attendance_page_date =  document.getElementById('attendance_page_date');
var attendance_page_days_head =  document.getElementById('attendance_page_days_head');
var attendance_page_date_year_n =  document.getElementById('attendance_page_date_year_n');
var attendance_page_date_month_n =  document.getElementById('attendance_page_date_month_n');
var attendance_page_days_body =  document.getElementById('attendance_page_days_body');
var attendance_please_holdon = document.getElementById('attendance_please_holdon');
var tools_page = document.getElementById('tools_page');
var bug2xlsx_mainTab = document.getElementById('bug2xlsx_mainTab');
var bug2xlsx_helpTab = document.getElementById('bug2xlsx_helpTab');
var bug2xlsx_mainPage = document.getElementById('bug2xlsx_mainPage');
var bug2xlsx_helpPage = document.getElementById('bug2xlsx_helpPage');
var errorbar_bottom = document.getElementById('errorbar_bottom');
var errorbar_bottom_img = document.getElementById('errorbar_bottom_img');
var errorbar_bottom_message = document.getElementById('errorbar_bottom_message');
var blackback = document.getElementById("blackback");

//动态调整workspase大小为浏览器展示区大小
workspace.style.width = browserWidth + "px";
workspace.style.height = browserHeight + "px";
//动态调整user_top_name_li的字体大小与line-height
user_top_name_li.style.lineHeight = user_top_name.clientHeight +"px";
user_top_name_li.style.fontSize = user_top_name.clientHeight * 0.5 +"px";
//动态调整user_top_drop_beforelogin的大小
user_top_drop_beforelogin.style.width = user_top_name.clientWidth +"px";
//动态调整user_top_drop_username和user_top_drop_password的宽度
user_top_drop_username.style.width = user_top_name.clientWidth * 0.85 - 22 + "px";
user_top_drop_password.style.width = user_top_name.clientWidth * 0.85 - 22 + "px";
//动态调整user_top_drop_afterlogin的大小
user_top_drop_afterlogin.style.width = user_top_name.clientWidth +"px";
//动态调整user_top_drop_reset按钮的高度
user_top_drop_reset.style.height = user_top_name.clientHeight * 0.5 +"px";
//动态调整user_top_drop_logout按钮的高度
user_top_drop_logout.style.height = user_top_name.clientHeight * 0.5 +"px";
//动态调整重置密码三个输入框的宽度
user_resetpassword_old.style.width = browserWidth * 0.12 - 41 + "px";
user_resetpassword_new.style.width = browserWidth * 0.12 - 41 + "px";
user_resetpassword_confirm.style.width = browserWidth * 0.12 - 41 + "px";
//动态调整function_banner_1下input的高度与其中字体的大小
$('.function_banner_1').children('input').css({'height':browserHeight * 0.04 + 'px','font-size':browserHeight * 0.02 + 'px'});
//动态调整home_page_title的字体大小
home_page_title.style.fontSize = browserHeight * 0.06 + "px";
//动态调整attendance_page_date的字体大小
attendance_page_date.style.fontSize = browserHeight * 0.07 + "px";
//动态调整attendance_page_days_head中星期字体的大小
$(".attendance_page_days_head > tr > th").css('font-size',browserHeight * 0.03 + 'px');
//动态调整attendance_page_days_body中日期/文字/时间的字体大小
$(".attendance_page_days_body > tr > td").css('font-size',browserHeight * 0.018 + 'px');
//动态调整attendance_please_holdon的字体大小与屏幕位置
attendance_please_holdon.style.fontSize = browserWidth * 0.08 + "px";
attendance_please_holdon.style.top = browserHeight * 0.32 + "px";
attendance_please_holdon.style.right = browserWidth * 0.45 - parseInt(attendance_please_holdon.style.fontSize) * 3 / 2 + "px";
//动态调整attendance_choose_user中文字的字体大小
$(".attendance_choose_user > p").css('font-size',browserHeight * 0.025 + 'px');
$(".attendance_choose_user > label").css('font-size',browserHeight * 0.023 + 'px');
$(".attendance_choose_userlist").css('font-size',browserHeight * 0.023 + 'px');
//动态调整errorbar_bottom的位置
errorbar_bottom.style.left = (browserWidth - errorbar_bottom.clientWidth)/ 2 + "px";
errorbar_bottom.style.lineHeight = errorbar_bottom.clientHeight +"px";
//动态调整errorbar_bottom_img的位置
errorbar_bottom_img.style.paddingLeft = errorbar_bottom.clientHeight / 2 - 18 + "px";
errorbar_bottom_img.style.paddingTop = errorbar_bottom.clientHeight / 2 - 18 + "px";
//动态调整errorbar_bottom_message的位置
errorbar_bottom_message.style.lineHeight = errorbar_bottom.clientHeight + "px";
errorbar_bottom_message.style.paddingLeft = errorbar_bottom.clientHeight / 2 - 18 + "px";
errorbar_bottom_message.style.paddingRight = errorbar_bottom.clientHeight / 2 - 18 + "px";
//定义全体show方法
//定义show_loginPage方法,展现给用户登陆前的页面元素
function show_loginPage(){
    //user_top_name_li修改为"登录"字样
    user_top_name_li.innerHTML = "登录";
    //user_top从页面顶部移入,此时的下拉框为user_top_drop_beforelogin
    $(".user_top").animate({top: 0},600).mouseenter(function(){
        setTimeout(function(){
            $(".user_top_drop_beforelogin").stop().animate({opacity:0.7},400);
        },1);
        $(".user_top_drop_beforelogin").css({"display":"block","opacity":0});
    }).mouseleave(function(){
        $(".user_top_drop_beforelogin").css({"display":"none"});
    });
}
//定义show_logedPage方法,展现给用户本机cookie教研通过后的页面元素
function show_logedPage(name){
    //user_top_name_li修改为用户名
    user_top_name_li.innerHTML = "欢迎," + name;
    //user_top从页面顶部移入,此时的下拉框为user_top_drop_afterlogin
    $(".user_top").animate({top: 0},600).mouseenter(function(){
        setTimeout(function(){
            $(".user_top_drop_afterlogin").stop().animate({opacity:0.7},400);
        },1);
        $(".user_top_drop_afterlogin").css({"display":"block","opacity":0});
    }).mouseleave(function(){
        $(".user_top_drop_afterlogin").css({"display":"none"});
    });
    //function_banner从页面左边移入
    $(".function_banner").animate({left: 0},600);
    //打开页面默认进入home_page
    //首先改变按钮背景色
    change_function_banner_button_color(function_banner_1_button,"white");
    //然后打开home_page
    show_element(home_page,600,1);
    //年月定义
    $(".attendance_page_date_year_n").html(now_year);
    $(".attendance_page_date_month_n").html((now_month + 1));
    //绘画当前月份
    draw_attendence_request(now_year,now_month + 1);
}
//定义show_afterloginPage方法,接收用户名,被login_response_actions方法使用
function show_user_resetpassword() {
    user_resetpassword_old.value = "";
    user_resetpassword_new.value = "";
    user_resetpassword_confirm.value = "";
    show_element(blackback,500,0.2);
    show_element(user_resetpassword,500,1);
}
//定义取消重置密码的方法,点击后黑背景与user_resetpassword隐藏
function show_afterloginPage(name) {
    //首先是user_top_name慢慢透明,user_top_drop_beforelogin不再展示
    $(".user_top_name").animate({opacity:0},800);
    $(".user_top_drop_beforelogin").remove();
    //然后是user_top_name_li的内容变为用户名
    setTimeout(_changeInnerHTML(user_top_name_li,"欢迎," + name),805);
    //接着user_top_name慢慢展示出来
    setTimeout('$(".user_top_name").animate({opacity:0.8},800)',810);
    //最后将user_top_drop_afterlogin展示出来,且opacity值为0
    user_top.appendChild(user_top_drop_afterlogin);
    $(".user_top_drop_afterlogin").css({"display":"none"});
    $(".user_top").animate({top: 0},600).mouseenter(function(){
        setTimeout(function(){
            $(".user_top_drop_afterlogin").stop().animate({opacity:0.7},400);
        },1);
        $(".user_top_drop_afterlogin").css({"display":"block","opacity":0});
    }).mouseleave(function(){
        $(".user_top_drop_afterlogin").css({"display":"none"});
    });
    //function_banner从页面左边移入
    $(".function_banner").animate({left: 0},600);
    //打开页面默认进入home_page
    //首先改变按钮背景色
    change_function_banner_button_color(function_banner_1_button,"white");
    //然后打开home_page
    show_element(home_page,600,1);
    //年月定义
    $(".attendance_page_date_year_n").html(now_year);
    $(".attendance_page_date_month_n").html(((now_month) + 1));
    //绘画当前月份
    draw_attendence_request(now_year,now_month + 1);
}
//定义一个接收元素和动画时间的方法,作用是控制元素渐出,可直接用或者用于setTimeout
function show_element(element,time,opacity) {
    element.style.display = "block";
    $("." + element.id).animate({opacity:opacity},time);
}
//定义一个接收元素和动画时间的方法,作用是控制元素渐隐,返回无参函数,可直接用或者用于setTimeout
function hide_element(element,time) {
    $("." + element.id).animate({opacity:0},time);
    setTimeout(function () {
        element.style.display = "none";
    },time)
}
//定义修改function_banner上任意按钮颜色与选中状态的方法,一旦某个按钮被选中,则其他按钮释放
function change_function_banner_button_color(button,color) {
    //首先初始化所有按钮
    function_banner_1_button.style.backgroundColor = "rgb(247,247,247)";
    function_banner_1_button.checked = false;
    function_banner_2_button.style.backgroundColor = "rgb(247,247,247)";
    function_banner_2_button.checked = false;
    function_banner_3_button.style.backgroundColor = "rgb(247,247,247)";
    function_banner_3_button.checked = false;
    //然后单独修改需要改变的按钮
    button.style.backgroundColor = color;
    button.checked = true;
}
//定义打开page的方法,接收某个页面.作用是检查当前打开页面,关闭它,然后打开目的页面
function show_page(page){
    //首先禁用所有function_banner处的按钮
    var buttonlist = [function_banner_1_button,function_banner_2_button,function_banner_3_button];
    for (var j = 0;j < buttonlist.length;j++){
        buttonlist[j].disabled = "disabled";
    }
    //检测当前打开页面.当前系统一共三个页面
    var pagelist = [home_page,attendance_page,tools_page];
    for (var i = 0;i < pagelist.length;i++){
        if (pagelist[i].style.display == "block"){
            // hide_element(pagelist[i],400);
            // 首先将功能页向右移动
            $('.' + pagelist[i].id).animate({left: (browserWidth * 0.11 + "px")},100);
            // 然后隐藏功能页
            hide_element(pagelist[i],200);
        }
    }
    //然后打开目的页面
    setTimeout(function () {
        // 最后将页面位置归位
        page.style.left = browserWidth * 0.1 + "px";
        show_element(page,300,1);
    },300);
    //最后放开所有按钮
    setTimeout(function () {
        for (var k = 0;k < buttonlist.length;k++){
            buttonlist[k].disabled = "";
        }
    },600);
}
//定义一个展示人员选择对话框的方法
function show_export_attendance() {
    //清空人员选项,重置全选按钮
    $('.attendance_choose_user > div')[0].innerHTML = '';
    $('.attendance_choose_user > label > input').prop({'checked':false});
    //请求人员列表
    var cookieList = document.cookie.split(";");
    var reg_test_username = /username=/;
    var reg_match_username = /username=(.*)/;
    var reg_test_netkey = /netkey=/;
    var reg_match_netkey = /netkey=(.*)/;
    for (var x = 0; x < cookieList.length; x++) {
        if (reg_test_username.test(cookieList[x]) == true) {
            var username = cookieList[x].match(reg_match_username)[1];
        }
        if (reg_test_netkey.test(cookieList[x]) == true) {
            var netkey = cookieList[x].match(reg_match_netkey)[1];
        }
    }
    var request = {'username': username, "netkey": netkey};
    var url = "/queryUserlist";
    ajaxHttp.open("POST", url, true);
    ajaxHttp.setRequestHeader("Content-Type", "application/json");
    ajaxHttp.onreadystatechange = show_export_attendance_actions;
    ajaxHttp.send(JSON.stringify(request));
}
//定义打开我的主页的方法
function click_button(object) {
    // 如果按钮对应的页面打开着,则点击该按钮页面无响应
    //如果点击的按钮是第一个,并且此时"我的主页"展示中,则按钮点击后页面无响应
    if (object.id == 'function_banner_1_button' && home_page.style.display == "block"){}
    else if (object.id == 'function_banner_2_button' && attendance_page.style.display == "block"){}
    else if (object.id == 'function_banner_3_button' && tools_page.style.display == "block"){}
    // 否则改变按钮颜色,且改变页面
    else {
        //首先改变按钮背景色
        change_function_banner_button_color(object,"white");
        if (object.id == 'function_banner_1_button'){
            show_page(home_page);
        }else if (object.id == 'function_banner_2_button'){
            show_page(attendance_page);
        }else if (object.id == 'function_banner_3_button'){
            show_page(tools_page);
        }
    }
}
//定义各请求方法
//定义check_cookie_response_actions方法,告诉页面当服务器返回cookie有效无效的值后干点什么
function check_cookie_response_actions() {
    if (ajaxHttp.readyState == 4) {
        var respones_JSON = ajaxHttp.responseText;
        var respones_Data = eval("(" + respones_JSON + ")");
        if (ajaxHttp.status == 200) {
            if (respones_Data.state == 0) {
                prompt_message("出错啦!账户于别处登陆,请重新登陆", 0);
                show_loginPage();
            } else if (respones_Data.state == 1) {
                prompt_message("您好!欢迎回来~", 1);
                show_logedPage(respones_Data.name);
            } else if (respones_Data.state == 2) {
                prompt_message("检查cookie失败!数据库无法连接", 0);
            } else {
                prompt_message("检查cookie失败!请清理浏览器缓存", 0);
            }
        } else {
            prompt_message("出错啦!检查cookie失败", 0);
        }
    }
}
//创建一个校验cookie是否有效的ajax请求
function check_cookie_request(){
    var cookieList = document.cookie.split(";");
    var patt_regUsername = /username=(.*)/;
    var patt_testUsername = /username=/;
    var patt_regCookie = /value=(.*)/;
    var patt_testCookie = /value=/;
    //遍历cookieList
    for (var i = 0;i < cookieList.length;i++){
        if (patt_testUsername.test(cookieList[i]) == true){
            var username = cookieList[i].match(patt_regUsername)[1];
        }else if (patt_testCookie.test(cookieList[i]) == true){
            var cookie = cookieList[i].match(patt_regCookie)[1];
        }
    }
    var url = "/checkCookie";
    var checkData = {"username":username, "cookie":cookie};
    ajaxHttp.open("POST",url,true);
    ajaxHttp.setRequestHeader("Content-Type","application/json");
    ajaxHttp.onreadystatechange = check_cookie_response_actions;
    ajaxHttp.send(JSON.stringify(checkData));
}
//定义login_response_actions方法,告诉页面当服务器返回登录相关信息值后干点什么
function login_response_actions() {
    if (ajaxHttp.readyState == 4) {
        var logData_JSON = ajaxHttp.responseText;
        var logData = eval("(" + logData_JSON + ")");
        if (ajaxHttp.status == 200) {
            if (logData.state == "0") {
                prompt_message("出错啦!数据库连接错误",0);
            } else if (logData.state == "1") {
                prompt_message("出错啦!用户名和密码不要留空",0);
            } else if (logData.state == "2") {
                prompt_message("出错啦!用户貌似不存在哦",0);
            } else if (logData.state == "3") {
                prompt_message("出错啦!密码输错了哟",0);
            } else if (logData.state == '4') {
                prompt_message("成功啦!欢迎进入系统",1);
                document.cookie = "username=" + logData.username;
                document.cookie = "netkey=" + logData.netkey;
                if (logData.key != ""){
                    document.cookie = "value=" + logData.key;
                }
                show_afterloginPage(logData.name);
            }
        } else {
            prompt_message("系统错误!登录失败",0)
        }
    }
}
//定义login_request方法,取username/password/rememberMe三值,并用ajax方式传递值至服务器
function login_request(){
    var loginInfor = {"username":user_top_drop_username.value,"password":user_top_drop_password.value,"rememberMe":user_top_drop_remember.checked};
    var url = "/login";
    ajaxHttp.open("POST",url,true);
    ajaxHttp.setRequestHeader("Content-Type","application/json");
    ajaxHttp.onreadystatechange = login_response_actions;
    ajaxHttp.send(JSON.stringify(loginInfor));
}
//定义修改密码请求的响应
function reset_password_respones_actions() {
    if (ajaxHttp.readyState == 4){
        var reset_password_respones_JSON = ajaxHttp.responseText;
        var reset_password_respones_Data = eval("(" + reset_password_respones_JSON + ")");
        if (ajaxHttp.status == 200){
            if (reset_password_respones_Data.state == 0){
                prompt_message("出错啦!您没有修改密码的权限",0);
            }else if(reset_password_respones_Data.state == 1){
                prompt_message("出错啦!旧密码输入错误",0);
            }else if(reset_password_respones_Data.state == 2){
                prompt_message("修改密码成功",1);
                hide_element(user_resetpassword,600);
                hide_element(blackback,600);
            }else if(reset_password_respones_Data.state == 3){
                prompt_message("修改密码失败!数据库无法连接",0);
            }
        }else {
            prompt_message("出错啦!密码修改失败",0);
        }
    }
}
//定义修改密码的请求
function reset_password_request(old_password,new_password) {
    var cookieList = document.cookie.split(";");
    var reg_test_username = /username=/;
    var reg_match_username = /username=(.*)/;
    var reg_test_netkey = /netkey=/;
    var reg_match_netkey = /netkey=(.*)/;
    for (var i = 0;i < cookieList.length;i++){
        if (reg_test_username.test(cookieList[i]) == true){
            var username = cookieList[i].match(reg_match_username)[1];
        }
        if (reg_test_netkey.test(cookieList[i]) == true){
            var netkey = cookieList[i].match(reg_match_netkey)[1];
        }
    }
    var loginInfor = {"username":username,"old":old_password,"new":new_password,"netkey":netkey};
    var url = "/resetPassword";
    ajaxHttp.open("POST",url,true);
    ajaxHttp.setRequestHeader("Content-Type","application/json");
    ajaxHttp.onreadystatechange = reset_password_respones_actions;
    ajaxHttp.send(JSON.stringify(loginInfor));
}
//定义元素相关方法
//创建一个接收参数返回无参的方法,适用于setTimeout,作用是改变元素内的文字
function _changeInnerHTML(a,b) {
    return function (){
        a.innerHTML = b;
    }
}
//定义一个接收错误/正确信息(string),错误/正确状态(int)的方法,作用是让errorbar_bottom出现然后消失
function prompt_message(message,status) {
    if (status == 1){
        errorbar_bottom_img.src = "../static/images/success_36px.png";
    }else {
        errorbar_bottom_img.src = "../static/images/stop_36px.png";
    }
    errorbar_bottom_message.innerHTML = message;
    errorbar_bottom.style.left = (browserWidth - errorbar_bottom.clientWidth)/ 2 + "px";
    if ($(".errorbar_bottom").is(":animated")){}else {
        $(".errorbar_bottom").animate({bottom: (workspace.clientHeight * 0.02 + "px")},500);
        setTimeout(function () {
            $(".errorbar_bottom").animate({bottom: (workspace.clientHeight * 0.02 + "px")},1000);
        },505);
        setTimeout(function () {
            $(".errorbar_bottom").animate({bottom: (-workspace.clientHeight * 0.06 + "px")},700);
        },1010);
    }
}
//定义其他关键方法
// 定义logout方法
function logout() {
    //提示用户"注销成功"
    prompt_message("注销成功",1);
    user_top_drop_username.value = "";
    user_top_drop_password.value = "";
    user_top_drop_remember.checked = false;
    //cookie需要清空
    document.cookie = "value=" + ";expires=" + expireDate.toGMTString();
    document.cookie = "netkey=" + ";expires=" + expireDate.toGMTString();
    document.cookie = "username=" + ";expires=" + expireDate.toGMTString();
    //user_top_name慢慢透明,user_top_drop_afterlogin不再展示
    $(".user_top_name").animate({opacity:0},800);
    $(".user_top_drop_afterlogin").remove();
    //然后是user_top_name_li的内容变为"登录"
    setTimeout(_changeInnerHTML(user_top_name_li,"登录"),805);
    //接着user_top_name慢慢展示出来
    setTimeout('$(".user_top_name").animate({opacity:0.8},800)',810);
    //最后将user_top_drop_beforelogin展示出来,且opacity值为0
    user_top.appendChild(user_top_drop_beforelogin);
    $(".user_top_drop_beforelogin").css({"display":"none"});
    $(".user_top").animate({top:0},600).mouseenter(function(){
        setTimeout(function(){
            $(".user_top_drop_beforelogin").stop().animate({opacity:0.7},400);
        },1);
        $(".user_top_drop_beforelogin").css({"display":"block","opacity":0});
    }).mouseleave(function(){
        $(".user_top_drop_beforelogin").css({"display":"none"});
    });
    //function_banner向页面左边移出
    $(".function_banner").animate({left: (-browserWidth * 0.1 + "px")},600);
    //移除当前展示页面
    //首先检测当前打开页面.当前系统一共两个页面
    var pagelist = [home_page,attendance_page];
    for (var i = 0;i < pagelist.length;i++){
        if (pagelist[i].style.display == "block"){
            hide_element(pagelist[i],400);
        }
    }
}
//检测用户cookie.若不存在,则调用loginPage方法;若存在但与数据库中不符合,则调用loginPage方法;若存在且和数据库中一致,则调用logedPage方法
$(document).ready(function(){
    if (document.cookie == ""){
        show_loginPage();
    } else {
        var patt_testValue = /value=/;
        var patt_testUsername = /username=/;
        if (patt_testValue.test(document.cookie) == false || patt_testUsername.test(document.cookie) == false){
            show_loginPage();
        }else {
            check_cookie_request();
        }
    }
});
//定义退出重置密码页面方法,点击后渐出黑背景与user_resetpassword
function cancel_reset_password() {
    hide_element(blackback,500);
    hide_element(user_resetpassword,500);
}
//定义退出人员选择对话框的方法,点击后淡出黑背景与对话框
function concel_export_attendance(){
    hide_element(blackback,500);
    hide_element(attendance_choose_user,500);
}
//定义提交修改密码请求的方法
function confirm_reset_password() {
    //如果三个都有内容,则正常流程
    if (user_resetpassword_old.value != "" && user_resetpassword_new.value != "" && user_resetpassword_confirm.value != ""){
        if (user_resetpassword_new.value == user_resetpassword_confirm.value){
            //调用修改密码的方法,传入旧密码与新密码
            reset_password_request(user_resetpassword_old.value,user_resetpassword_new.value);
        }else {
            //如果再输一遍与新密码不符,则报错
            prompt_message("出错啦!新密码与确认密码不一致",0);
        }
    }else{
        //如果三个其中有一个为空,则报异常
        prompt_message("出错啦!请完整填写各项内容",0);
    }
}
//定义创建日历每一天考情记录div的方法,接收每天div的id
function create_everyday(id,clockin_time,clockout_time,day_state) {
    if (clockin_time != undefined){
        var clockin_list = clockin_time.split(":");
    }
    if (clockout_time != undefined){
       var clockout_list = clockout_time.split(":");
    }
    var maindiv = document.getElementById(id);
    var clockin = document.createElement("div");
    var clockout = document.createElement("div");
    // 新建用于选择当天是否节假日相关的select
    var state = document.createElement("select");
    state.id = id + "_state";
    state.className = id + "_state";
    state.style.fontSize = browserHeight * 0.02 + 'px';
    state.style.height = browserHeight * 0.035 + 'px';
    state.addEventListener("change",function () {
        // 改变后判断当前value值,然后修改当前背景
        switch (this.value){
            case '0':
                this.style.backgroundColor = 'rgb(248, 244, 244)';
                break;
            case '1':
                this.style.backgroundColor = 'rgb(255, 105, 99)';
                break;
            case '2':
                this.style.backgroundColor = 'rgb(150, 151, 153)';
                break;
        }
    });
    // 新增三个选项:空(默认);休;班
    var state_blank = document.createElement("option");
    state_blank.value = '0';
    state_blank.innerHTML = '';
    state_blank.style.backgroundColor = 'rgb(248, 244, 244)';
    state.appendChild(state_blank);
    var state_break = document.createElement("option");
    state_break.value = '1';
    state_break.innerHTML = '休';
    state_break.style.backgroundColor = 'rgb(255, 105, 99)';
    state.appendChild(state_break);
    var state_work = document.createElement("option");
    state_work.value = '2';
    state_work.innerHTML = '班';
    state_work.style.backgroundColor = 'rgb(150, 151, 153)';
    state.appendChild(state_work);
    if (day_state == '0'){
        state.selectedIndex = 0;
        state.style.backgroundColor = 'rgb(248, 244, 244)';
    }else if(day_state == '1'){
        state.selectedIndex = 1;
        state.style.backgroundColor = 'rgb(255, 105, 99)';
    }else if(day_state == '2'){
        state.selectedIndex = 2;
        state.style.backgroundColor = 'rgb(150, 151, 153)';
    }
    maindiv.appendChild(state);
    //新建用于显示日期的p,并修改其id和class
    var days_x_y_p = document.createElement("p");
    days_x_y_p.id = id + "_p";
    days_x_y_p.className = id + "_p";
    days_x_y_p.style.fontSize = browserHeight * 0.025 + 'px';
    maindiv.appendChild(days_x_y_p);
    //新增上班时间文字
    var clock_in_b = document.createElement("b");
    clock_in_b.id = id + "_clockin_b";
    clock_in_b.className = id + "_clockin_b";
    clock_in_b.innerHTML = "上班:";
    clockin.appendChild(clock_in_b);
    //新增上班时间的小时select
    var clock_in_select_h = document.createElement("select");
    clock_in_select_h.id = id + "_clockin_h";
    clock_in_select_h.className = id + "_clockin_h";
    clock_in_select_h.style.fontSize = browserHeight * 0.018 + 'px';
    //新增24小时(包括不填写)
    var clockin_h_option_ = document.createElement("option");
    clockin_h_option_.value = '';
    clockin_h_option_.innerHTML = '';
    clock_in_select_h.appendChild(clockin_h_option_);
    for (var i = 0;i < 24;i++){
        var clockin_h_option = document.createElement("option");
        clockin_h_option.value = i;
        clockin_h_option.innerHTML = i;
        clock_in_select_h.appendChild(clockin_h_option);
    }
    if (clockin_time != undefined){
        clock_in_select_h.selectedIndex = parseInt(clockin_list[0]) + 1;
    }
    clockin.appendChild(clock_in_select_h);
    //新增上班时间的"时"
    var clock_in_b1 = document.createElement("b");
    clock_in_b1.innerHTML = "时";
    clockin.appendChild(clock_in_b1);
    //新增上班时间的分钟select
    var clock_in_select_m = document.createElement("select");
    clock_in_select_m.id = id + "_clockin_m";
    clock_in_select_m.className = id + "_clockin_m";
    clock_in_select_m.style.fontSize = browserHeight * 0.018 + 'px';
    //新增60分,包括空
    var clockin_m_option_ = document.createElement("option");
        clockin_m_option_.value = '';
        clockin_m_option_.innerHTML = '';
        clock_in_select_m.appendChild(clockin_m_option_);
    for (var j = 0;j < 60;j++){
        var clockin_m_option = document.createElement("option");
        clockin_m_option.value = j;
        clockin_m_option.innerHTML = j;
        clock_in_select_m.appendChild(clockin_m_option);
    }
    if (clockin_time != undefined){
        clock_in_select_m.selectedIndex = parseInt(clockin_list[1]) + 1;
    }
    clockin.appendChild(clock_in_select_m);
    //新增上班时间的"分"
    var clock_in_b2 = document.createElement("b");
    clock_in_b2.innerHTML = "分";
    clockin.appendChild(clock_in_b2);
    clockin.style.marginBottom = '3px';
    maindiv.appendChild(clockin);
    //新增下班时间文字
    var clock_out_b = document.createElement("b");
    clock_out_b.id = id + "_clockin_b";
    clock_out_b.className = id + "_clockin_b";
    clock_out_b.innerHTML = "下班:";
    clockout.appendChild(clock_out_b);
    //新增下班时间的小时select
    var clock_out_select_h = document.createElement("select");
    clock_out_select_h.id = id + "_clockout_h";
    clock_out_select_h.className = id + "_clockout_h";
    clock_out_select_h.style.fontSize = browserHeight * 0.018 + 'px';
    //新增24小时,包括空
    var clockout_h_option_ = document.createElement("option");
        clockout_h_option_.value = '';
        clockout_h_option_.innerHTML = '';
        clock_out_select_h.appendChild(clockout_h_option_);
    for (var x = 0;x < 24;x++){
        var clockout_h_option = document.createElement("option");
        clockout_h_option.value = x;
        clockout_h_option.innerHTML = x;
        clock_out_select_h.appendChild(clockout_h_option);
    }
    if (clockout_time != undefined){
        clock_out_select_h.selectedIndex = parseInt(clockout_list[0]) + 1;
    }
    clockout.appendChild(clock_out_select_h);
    //新增下班时间的"时"
    var clock_out_b1 = document.createElement("b");
    clock_out_b1.innerHTML = "时";
    clockout.appendChild(clock_out_b1);
    //新增下班时间的分钟select
    var clock_out_select_m = document.createElement("select");
    clock_out_select_m.id = id + "_clockout_m";
    clock_out_select_m.className = id + "_clockout_m";
    clock_out_select_m.style.fontSize = browserHeight * 0.018 + 'px';
    //新增60分,包括空
    var clockout_m_option_ = document.createElement("option");
        clockout_m_option_.value = '';
        clockout_m_option_.innerHTML = '';
        clock_out_select_m.appendChild(clockout_m_option_);
    for (var y = 0;y < 60;y++){
        var clockout_m_option = document.createElement("option");
        clockout_m_option.value = y;
        clockout_m_option.innerHTML = y;
        clock_out_select_m.appendChild(clockout_m_option);
    }
    if (clockout_time != undefined){
        clock_out_select_m.selectedIndex = parseInt(clockout_list[1]) + 1;
    }
    clockout.appendChild(clock_out_select_m);
    //新增下班时间的"分"
    var clock_out_b2 = document.createElement("b");
    clock_out_b2.innerHTML = "分";
    clockout.appendChild(clock_out_b2);
    maindiv.appendChild(clockout);
}
//定义取得考勤记录后(不管有没有)的绘画操作
function draw_attendence_response_actions(){
    if (ajaxHttp.readyState == 4){
        var draw_attendence_response_JSON = ajaxHttp.responseText;
        var draw_attendence_response_Data = eval("(" + draw_attendence_response_JSON + ")");
        if (ajaxHttp.status == 200){
            if (draw_attendence_response_Data.state == 0) {
                prompt_message("出错啦!您没有查询考勤记录的权限", 0);
            }else if (draw_attendence_response_Data.state == 2) {
                prompt_message("查询考勤记录失败!数据库无法连接", 0);
            }else {
                var data = draw_attendence_response_Data.data;
                var day_state = draw_attendence_response_Data.day_state;
                var year = $(".attendance_page_date_year_n")[0].innerHTML;
                var month = $(".attendance_page_date_month_n")[0].innerHTML;
                //每次绘画日历前,要初始化一下,清空请稍候提示和days的内容重置颜色
                attendance_please_holdon.style.display = "none";
                for (var x = 0; x < 6; x++) {
                    //申明列向量k
                    for (var y = 0; y < 7; y++) {
                        $("." + "days_" + x.toString() + "_" + y.toString()).html("").css("background-color","white");
                    }
                }
                //拼接年份和月份,判断当月第一天是周几.返一个星期中的某一天，其中0为星期日
                //parse() 方法可解析一个日期时间字符串，并返回 1970/1/1 午夜距离该日期时间的毫秒数
                var first_day = new Date(Date.parse(year + '/' + (parseInt(month)).toString() + '/1')).getDay(); //将日期值格式化
                //获取当月最大天数
                var max_days = new Date(year,(parseInt(month)),0);
                //首先写第一行.此时因为已经获取了第一天是周几,所以从days_0_first_day开始向days_0_6写数字,数字从1开始.直到到达days_0_6,此时需要换行,从days_1_0开始写,直到days_1_6再换行.一直到数字到达max_days则停止循环
                //申明i,用来写日期
                var i = 1;
                //申明行向量j
                for (var j = 0; j < 6; j++) {
                    //申明列向量k
                    for (var k = 0; k < 7; k++) {
                        //当判断列代表的星期几和first_day一致时,将i的值写入
                        if (j == 0 && k == first_day) {
                            if (data[year + '-' + month + '-' + i]){
                                create_everyday("days_0_" + k.toString(),data[year + '-' + month + '-' + i]['clockin_time'],data[year + '-' + month + '-' + i]['clockout_time'],day_state[year + '-' + month + '-' + i]);
                            }else {
                                create_everyday("days_0_" + k.toString());
                            }
                            $("." + "days_0_" + k.toString() + "_p").html("" + i.toString());
                            $("." + "days_0_" + k.toString()).css("background-color","rgb(248, 244, 244)");
                            i++;
                        } else if (i > 1) {
                            if (data[year + '-' + month + '-' + i]){
                                create_everyday("days_" + j.toString() + "_" + k.toString(),data[year + '-' + month + '-' + i]['clockin_time'],data[year + '-' + month + '-' + i]['clockout_time'],day_state[year + '-' + month + '-' + i]);
                            }else {
                                create_everyday("days_" + j.toString() + "_" + k.toString());
                            }
                            $("." + "days_" + j.toString() + "_" + k.toString() + "_p").html("" + i.toString());
                            $("." + "days_" + j.toString() + "_" + k.toString()).css("background-color","rgb(248, 244, 244)");
                            i++;
                        }
                        if (i > max_days.getDate()) break;
                    }
                    if (i > max_days.getDate()) break;
                }
                //1是向左,2是向右,0不变
                if (attendance_flag == 1){
                    //挪动日历位置
                    setTimeout(function () {
                        $(".attendance_page_days").css("left",(attendance_page.clientWidth * 0.1 + "px"));
                    },220);
                    //最后将日历展示出来
                    setTimeout(function () {
                        $(".attendance_page_days").animate({left:(attendance_page.clientWidth * 0.05 + "px"),opacity:1},200);
                    },230);
                }
                if (attendance_flag == 2){
                    //挪动日历位置
                    setTimeout(function () {
                        $(".attendance_page_days").css("left",0);
                    },220);
                    //最后将日历展示出来
                    setTimeout(function () {
                        $(".attendance_page_days").animate({left:(attendance_page.clientWidth * 0.05 + "px"),opacity:1},200);
                    },230);
                }
                //执行完毕后释放
                $(".attendance_page_button_previous").removeAttr("disabled");
                $(".attendance_page_button_next").removeAttr("disabled");
            }
        }else {
            prompt_message("出错啦!网络连接错误", 0);
        }
    }
}
//定义一个构造日历的方法,接受一个年份参数和一个月份参数,且方法内需要作异步数据请求,返回考勤记录后再画出日历
function draw_attendence_request(year,month) {
    //
    var cookieList = document.cookie.split(";");
    var reg_test_username = /username=/;
    var reg_match_username = /username=(.*)/;
    var reg_test_netkey = /netkey=/;
    var reg_match_netkey = /netkey=(.*)/;
    for (var x = 0; x < cookieList.length; x++) {
        if (reg_test_username.test(cookieList[x]) == true) {
            var username = cookieList[x].match(reg_match_username)[1];
        }
        if (reg_test_netkey.test(cookieList[x]) == true) {
            var netkey = cookieList[x].match(reg_match_netkey)[1];
        }
    }
    var date = year + "-" + month;
    var request = {'username': username, "netkey": netkey, "date": date};
    var url = "/queryAttendance";
    ajaxHttp.open("POST", url, true);
    ajaxHttp.setRequestHeader("Content-Type", "application/json");
    ajaxHttp.onreadystatechange = draw_attendence_response_actions;
    ajaxHttp.send(JSON.stringify(request));
}
//定义输出上一个月日历的方法
function show_previous_month() {
    //点击后按钮不可用,防止多次触发
    $(".attendance_page_button_previous").attr({"disabled":"disabled"});
    $(".attendance_page_button_next").attr({"disabled":"disabled"});
    var i = now_year;
    var j = 12;
    if (month_flag == 12){
        month_flag = 1;
        year_flag++;
        $(".attendance_page_date_year_n").animate({top:(-attendance_page.clientHeight * 0.01 + "px"),opacity:0},200);
        setTimeout(function () {
            $(".attendance_page_date_year_n").html(now_year - year_flag);
        },210);
        setTimeout(function () {
            $(".attendance_page_date_year_n").css("top",(attendance_page.clientHeight * 0.01 + "px"));
        },220);
        setTimeout(function () {
            $(".attendance_page_date_year_n").animate({top:0,opacity:1},200);
        },230);
        $(".attendance_page_date_month_n").animate({top:(-attendance_page.clientHeight * 0.01 + "px"),opacity:0},200);
        setTimeout(function () {
            $(".attendance_page_date_month_n").html(j);
        },210);
        setTimeout(function () {
            $(".attendance_page_date_month_n").css("top",(attendance_page.clientHeight * 0.01 + "px"));
        },220);
        setTimeout(function () {
            $(".attendance_page_date_month_n").animate({top:0,opacity:1},200);
        },230);
    }else {
        $(".attendance_page_date_month_n").animate({top:(-attendance_page.clientHeight * 0.01 + "px"),opacity:0},200);
        setTimeout(function () {
            $(".attendance_page_date_month_n").html(j + 1 - month_flag);
        },210);
        setTimeout(function () {
            $(".attendance_page_date_month_n").css("top",(attendance_page.clientHeight * 0.01 + "px"));
        },220);
        setTimeout(function () {
            $(".attendance_page_date_month_n").animate({top:0,opacity:1},200);
        },230);
        month_flag++;
    }
    //首先将日历向右挪动,同时透明度降低直至看不见
    $(".attendance_page_days").animate({left:(attendance_page.clientWidth * 0.1 + "px"),opacity:0},200);
    //请稍候
    attendance_please_holdon.style.display = "block";
    //然后构建新日历,2代表向右
    attendance_flag = 2;
    setTimeout(function () {
        draw_attendence_request((now_year - year_flag), (j - month_flag + 1));
    },210);
}
//定义输出下一个月日历的方法
function show_next_month() {
    //点击后按钮不可用,防止多次触发
    $(".attendance_page_button_previous").attr({"disabled":"disabled"});
    $(".attendance_page_button_next").attr({"disabled":"disabled"});
    var i = now_year;
    var j = 12;
    if (month_flag == 1){
        month_flag = 12;
        year_flag--;
        $(".attendance_page_date_year_n").animate({top:(attendance_page.clientHeight * 0.01 + "px"),opacity:0},200);
        setTimeout(function () {
            $(".attendance_page_date_year_n").html(now_year - year_flag);
        },210);
        setTimeout(function () {
            $(".attendance_page_date_year_n").css("top",(-attendance_page.clientHeight * 0.01 + "px"));
        },220);
        setTimeout(function () {
            $(".attendance_page_date_year_n").animate({top:0,opacity:1},200);
        },230);
        $(".attendance_page_date_month_n").animate({top:(attendance_page.clientHeight * 0.01 + "px"),opacity:0},200);
        setTimeout(function () {
            $(".attendance_page_date_month_n").html(j + 1 - month_flag);
        },210);
        setTimeout(function () {
            $(".attendance_page_date_month_n").css("top",(-attendance_page.clientHeight * 0.01 + "px"));
        },220);
        setTimeout(function () {
            $(".attendance_page_date_month_n").animate({top:0,opacity:1},200);
        },230);
    }else {
        month_flag--;
        //首先向下挪动控件并且隐藏,然后修改文字,接着修改控件位置,最后展示控件
        $(".attendance_page_date_month_n").animate({top:(attendance_page.clientHeight * 0.01 + "px"),opacity:0},200);
        setTimeout(function () {
            $(".attendance_page_date_month_n").html(j + 1 - month_flag);
        },210);
        setTimeout(function () {
            $(".attendance_page_date_month_n").css("top",(-attendance_page.clientHeight * 0.01 + "px"));
        },220);
        setTimeout(function () {
            $(".attendance_page_date_month_n").animate({top:0,opacity:1},200);
        },230);
    }
    //首先将日历向右挪动,同时透明度降低直至看不见
    $(".attendance_page_days").animate({left:0,opacity:0},200);
    //请稍候
    attendance_please_holdon.style.display = "block";
    //然后构建新日历,1代表向左
    attendance_flag = 1;
    //然后构建新日历
    setTimeout(function () {
        draw_attendence_request((now_year - year_flag), (j - month_flag + 1));
    },210);
}
//定义提交考勤记录请求的响应
function attendance_commit_response_actions() {
    if (ajaxHttp.readyState == 4){
        var attendance_commit_response_JSON = ajaxHttp.responseText;
        var attendance_commit_response_Data = eval("(" + attendance_commit_response_JSON + ")");
        if (ajaxHttp.status == 200){
            if (attendance_commit_response_Data.state == 0) {
                prompt_message("出错啦!您没有提交考勤记录的权限", 0);
            }else if (attendance_commit_response_Data.state == 1){
                prompt_message("提交考勤记录成功",1);
            }else if (attendance_commit_response_Data.state == 2){
                prompt_message("提交考勤失败!数据库无法连接",0);
            }
        }else {
            prompt_message("出错啦!网络连接出错",0);
        }
    }
}
//定义提交考勤记录的请求
function attendance_commit_request(){
    var clockin = '';
    var clockout = '';
    var date = '';
    var data = {};
    var day_state = {};
    var flag = 'Y';
    var cookieList = document.cookie.split(";");
    var reg_test_username = /username=/;
    var reg_match_username = /username=(.*)/;
    var reg_test_netkey = /netkey=/;
    var reg_match_netkey = /netkey=(.*)/;
    for (var x = 0;x < cookieList.length;x++){
        if (reg_test_username.test(cookieList[x]) == true){
            var username = cookieList[x].match(reg_match_username)[1];
        }
        if (reg_test_netkey.test(cookieList[x]) == true){
            var netkey = cookieList[x].match(reg_match_netkey)[1];
        }
    }
    for (var i = 0;i < 6;i++){
        for (var j = 0;j < 7;j++){
            var clockin_h = $(".days_" + i + "_" + j + "_clockin_h").val();
            var clockin_m = $(".days_" + i + "_" + j + "_clockin_m").val();
            var clockout_h = $(".days_" + i + "_" + j + "_clockout_h").val();
            var clockout_m = $(".days_" + i + "_" + j + "_clockout_m").val();
            var state = $(".days_" + i + "_" + j + "_state").val();
            var backgroundColor = $(".days_" + i + "_" + j).css('background-color');
            if (backgroundColor != "rgb(255, 255, 255)" && clockin_h != '' && clockin_m != '' && clockout_h != '' && clockout_m != ''){
                if ((parseInt(clockout_h) * 60 + parseInt(clockout_m) - parseInt(clockin_h) * 60 - parseInt(clockin_m)) > 0){
                    if (backgroundColor == 'rgb(233, 99, 80)'){
                        $(".days_" + i + "_" + j).animate({backgroundColor: 'rgb(248, 244, 244)'}, 600);
                    }
                    date = $(".attendance_page_date_year_n")[0].innerHTML + "-" + $(".attendance_page_date_month_n")[0].innerHTML + "-" + $(".days_" + i + "_" + j + "_p")[0].innerHTML;
                    clockin = clockin_h + ':' + clockin_m;
                    clockout = clockout_h + ':' + clockout_m;
                    data[date] = {'clockin':clockin,'clockout':clockout};
                    day_state[date] = state;
                }else {
                    flag = 'N';
                    $(".days_" + i + "_" + j).animate({backgroundColor:'#E96350'}, 600);
                }
            }
        }
    }
    if (flag == 'Y'){
        var attendanceData = {'username':username,"netkey":netkey,"data":data,"day_state":day_state};
        var url = "/commitAttendance";
        ajaxHttp.open("POST",url,true);
        ajaxHttp.setRequestHeader("Content-Type","application/json");
        ajaxHttp.onreadystatechange = attendance_commit_response_actions;
        ajaxHttp.send(JSON.stringify(attendanceData));
    }else {
        prompt_message("出错啦!上下班时间填写错误,请修复", 0);
    }
}
//定义返回人员列表后页面响应的方法
function show_export_attendance_actions(){
    if (ajaxHttp.readyState == 4){
        var userlist_response_JSON = ajaxHttp.responseText;
        var userlist_response_DATA = eval("(" + userlist_response_JSON + ")");
        if (ajaxHttp.status == 200){
            if (userlist_response_DATA.state == 0) {
                prompt_message("出错啦!您没有导出考勤记录的权限", 0);
            }else if (userlist_response_DATA.state == 1){
                prompt_message("查询人员列表失败!数据库无法连接", 0);
            }else {
                for (var i in userlist_response_DATA.data){
                    var user_input = document.createElement('input');
                    user_input.type = 'checkbox';
                    user_input.title = i;
                    var user_label = document.createElement('label');
                    user_label.appendChild(user_input);
                    user_label.innerHTML+= userlist_response_DATA.data[i];
                    attendance_choose_userlist.appendChild(user_label);
                }
                show_element(attendance_choose_user,500,1);
                show_element(blackback,500,0.2);
            }
        }else {
            prompt_message("出错啦!网络连接错误", 0);
        }
    }
}
//定义点击导出按钮后请求考勤xlsx的方法
function export_attendance_request() {
    var userlist = [];
    var userlist_input = $('.attendance_choose_userlist').find('input');
    for (var i =0;i < userlist_input.length;i++){
        if (userlist_input[i].checked == true){
            userlist.push(userlist_input[i].title);
        }
    }
    if (userlist == ''){
        prompt_message("出错啦!请勾选需要导出考勤的人员", 0);
    }else {
        var cookieList = document.cookie.split(";");
        var reg_test_username = /username=/;
        var reg_match_username = /username=(.*)/;
        var reg_test_netkey = /netkey=/;
        var reg_match_netkey = /netkey=(.*)/;
        for (var x = 0; x < cookieList.length; x++) {
            if (reg_test_username.test(cookieList[x]) == true) {
                var username = cookieList[x].match(reg_match_username)[1];
            }
            if (reg_test_netkey.test(cookieList[x]) == true) {
                var netkey = cookieList[x].match(reg_match_netkey)[1];
            }
        }
        var date = attendance_page_date_year_n.innerHTML + "-" + attendance_page_date_month_n.innerHTML;
        var form = document.createElement("form");   //定义一个form表单
        form.style.display = 'none';
        form.method = 'post';
        form.action = "/exportAttendance";
        var post_username = document.createElement("input");
        post_username.value = username;
        post_username.name = 'username';
        var post_netkey = document.createElement("textarea");
        post_netkey.name = 'netkey';
        post_netkey.value = netkey;
        var post_date = document.createElement("textarea");
        post_date.name = 'date';
        post_date.value = date;
        var post_userlist = document.createElement("textarea");
        post_userlist.name = 'userlist';
        post_userlist.value = userlist;
        form.appendChild(post_username);
        form.appendChild(post_netkey);
        form.appendChild(post_date);
        form.appendChild(post_userlist);
        form.submit();
        hide_element(attendance_choose_user,500);
        hide_element(blackback,500);
        // $.post({"username":'111'});
    }
}
//定义一个多选框全选的方法
function selectAll(object) {
    if(object.checked){
        $('.attendance_choose_userlist > label > input').prop({'checked':true,'disabled':'disabled'});
    }else {
        $('.attendance_choose_userlist > label > input').prop({'checked':false,'disabled':''});
    }
}
//定义一个下载文件的方法
function fileDownload(object){
    // alert(object.id);
    var form = document.createElement("form");   //定义一个form表单
    form.style.display = 'none';
    form.method = 'post';
    form.action = "/fileDownload";
    var filename = document.createElement("textarea");
    filename.name = 'filename';
    filename.value = object.id;
    form.appendChild(filename);
    form.submit();
}
//定义一个打开功能页的方法
function openFunctionPage(object){
    toolsPageList = {'bug2xlsx': 'bug2xlsx_online'};
    $('.' + toolsPageList[object.id]).css({display: 'block'}).animate({opacity: 1}, 500);
    show_element(blackback, 500, 0.3);
}
//定义一个关闭功能页的方法
function closeFunctionPage(object){
    var toolsPageList = {'bug2xlsx_online_close': 'bug2xlsx_online'};
    $('.' + toolsPageList[object.id]).animate({opacity: 0}, 500);
    hide_element(blackback, 500);
    setTimeout(function () {
        $('.' + toolsPageList[object.id]).css({display: 'none'});
    }, 500);
}
//定义一个修改元素背景色的方法
function changeBackgroundColor(object) {
    // 改变后判断当前value值,然后修改当前背景
    switch (object.value){
        case '0':
            object.style.backgroundColor = 'rgb(248, 244, 244)';
            break;
        case '1':
            object.style.backgroundColor = 'rgb(255, 68, 51)';
            break;
        case '2':
            object.style.backgroundColor = 'rgb(150, 151, 153)';
            break;
    }
}
//定义一个bug2xlsx切换上tab的方法
function bug2xlsx_changeTab(object){
    if (object.id == 'bug2xlsx_mainTab'){
        bug2xlsx_mainTab.style.backgroundImage = "url(../static/images/tabWidgetTab_selected.png)";
        bug2xlsx_helpTab.style.backgroundImage = "url(../static/images/tabWidgetTab_!selected.png)";
        $('.bug2xlsx_mainPage').css("display", 'block');
        $('.bug2xlsx_helpPage').css("display", 'none');
    }else {
        bug2xlsx_helpTab.style.backgroundImage = "url(../static/images/tabWidgetTab_selected.png)";
        bug2xlsx_mainTab.style.backgroundImage = "url(../static/images/tabWidgetTab_!selected.png)";
        $('.bug2xlsx_helpPage').css("display", 'block');
        $('.bug2xlsx_mainPage').css("display", 'none');
    }
}
//定义一个test()方法
function test() {
    var date = attendance_page_date_year_n.innerHTML + '-' + attendance_page_date_month_n.innerHTML;
    alert(date);
}