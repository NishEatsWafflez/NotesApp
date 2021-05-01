var token;  //initially declare token variable
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
            token = resp[token];
            // console.log("---------------------------------------------------------");
            // console.log(token);
            window.location.href = "/dashboard/?token="+resp['token'];
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
        url: "/user/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            // alert("yeet");
            // alert("no");
            // alert(resp['token']);
            // alert(typeof resp['token']);
            token = resp['token'];   //assign token variable to actual value
            // alert("to");
            // console.log("---------------------------------------------------------");
            window.location.href = "/dashboard/?token="+resp['token'];

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
