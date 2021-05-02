document.cookie = "token=John Smith; path=/";
$("form[name=signup_form").submit(function(e){
    // console.log("nut")

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    $.ajax({
        url: "/user/signup",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            document.cookie = "token=John Smith; path =/";
            // alert(document.cookie);
            // document.cookie = "token=" + resp['token'];
            var token = document.cookie;   //assign token variable to actual value
            // document.cookie = "path = /";
            // alert(token);
            // alert("no");
            // alert(resp['token']);
            // console.log("---------------------------------------------------------");
            window.location.href = "/dashboard/?" + token;
        },
        error: function(resp){
            // console.log($error.text)
            $error.text(resp.responseJSON.error);
        }
    });

    e.preventDefault();
});

$("form[name=login_form").submit(function(e){
    // console.log("nut")

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    $.ajax({
        url: "/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            // alert(resp['token']);
            // alert("yeet");
            // alert("no");
            // alert(resp['token']);
            // alert(typeof resp['token']);
            // document.cookie="";
            document.cookie = "token=John Smith; path = /";
            // alert(document.cookie);
            // alert(document.cookie);
            document.cookie = "token=" + resp['token'];
            var token = document.cookie;   //assign token variable to actual value
            // document.cookie = "path = /";
            // alert(token);
            // alert("no");
            // alert(resp['token']);
            // console.log("---------------------------------------------------------");
            window.location.href = "/dashboard/?" + token;

        },
        error: function(resp){
            // console.log($error.text)
            $error.text(resp.responseJSON.error);
        }
    });
  e.preventDefault();

});

$("form[name=new_note").submit(function(e){
    // console.log("nut")
    alert(token);
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    $.ajax({
        url: "/new",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            alert("document.cookie");
            var token = document.cookie;
            alert(token);   //attempt to access new value of token
            window.location.href = "/dashboard/?token=" + token;

        },
        error: function(resp){
            // console.log($error.text)
            $error.text(resp.responseJSON.error);
        }
    });

    e.preventDefault();
});

$("form[name=edit_note").submit(function(e){
    // console.log("nut")
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    $.ajax({
        url: "/edits",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            window.location.href = "/dashboard/" + token;

        },
        error: function(resp){
            // console.log($error.text)
            $error.text(resp.responseJSON.error);
        }
    });

    e.preventDefault();
});
