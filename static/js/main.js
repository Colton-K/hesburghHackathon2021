$("form[name=signup_form").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/signup",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      setCookie("SameSite", "Strict");
      setCookie("email", resp.email);
      setCookie("name", resp.name);
      setCookie("user_id", resp.user_id);
      setCookie("session_id", resp.session_id);

      window.location.href = "/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

function logout(event) {
    document.cookie="session_id=logged_out";
    console.log("logging out")
    window.location.hred = "/";
}

function getGroups(value) {
    // display("Value = " + value);
    // console.log("in get groups")
    var workingDiv = document.getElementById("groupSearchResults");
    var results = "Results: <br>";
    //results += value; 

    $.ajax({
      url: "/user/getGroups",
      type: "POST",
      data: value,
      dataType: "json",
      success: function(resp) {
        
        console.log(resp)
        var len = resp.length;
        console.log(len)
        for (var i = 0; i < len; i++) {
            console.log(resp[i]);
            //results += resp[i]
        }
        workingDiv.innerHTML = results;
      },
      error: function(resp) {
        $error.text(resp.responseJSON.error).removeClass("error--hidden");
      }
    });
    

    // workingDiv.insertAdjacentHTML("afterend", value)
    // workingDiv.insertAdjacentHTML("afterend", "<br>")
};

$("form[name=login_form").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/login",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      setCookie("SameSite", "Strict");
      setCookie("email", resp.email);
      setCookie("name", resp.name);
      setCookie("user_id", resp.user_id);
      setCookie("session_id", resp.session_id);

      window.location.href = "/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});
