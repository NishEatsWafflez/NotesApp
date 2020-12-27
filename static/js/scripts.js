
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
            window.location.href = "/dashboard/";

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
            window.location.href = "/dashboard/";

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

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    $.ajax({
        url: "/new",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            window.location.href = "/dashboard/";

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
            window.location.href = "/dashboard/";

        },
        error: function(resp){
            // console.log($error.text)
            $error.text(resp.responseJSON.error);
        }
    });

    e.preventDefault();
});
