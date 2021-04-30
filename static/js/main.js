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

function searchGroups(value) {
    console.log(value)
    var workingDiv = document.getElementById("groupSearchResults");
    var results = "Results: <br>";
    //results += value; 

    $.ajax({
      url: "/user/searchGroups",
      type: "POST",
      data: {
        'query' : value
      },
      dataType: "json",
      success: function(resp) {
        
        console.log(resp)
        var len = resp.length;
        console.log(len)
        if (len == 0) {
                results = "<p align=\"left\">No matching groups found, create a new group below:</p>"
            results += `
				<div class="row">
					<div class="wideColumn">
						<input type='text' id="groupInput" onchange="searchGroups(this.value);" ();" />
						<form name="groupSearch_form" onclick=searchGroups(groupInput.value)> </form>
					</div>
					<div class="thinColumn">
						<button class="button3" onclick="createGroup(groupInput.value)">Create Group</button>
					</div>
				</div>
                `

        }
        else {
            for (var i = 0; i < len; i++) {
                // console.log(resp[i]);
                results += "<p>"
                results += resp[i].name
                results += "<button onclick=\"addGroup(\'"
                results += resp[i].name
                results += "\')\">Add Group</button></p>"
            }
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

function addGroup(groupName) {
    // console.log("groupName: " + groupName)
    
    $.ajax({
        url: "/user/addGroup",
        type: "POST",
        data: {
            'name' : groupName
        },
        dataType: "json",
        success: function(resp) {
            console.log("resp:" + resp)
            window.location.href = "/profile";
        },
        error: function(resp) {
            
        }
    })
}

// TODO: Implement this correctly!
function createGroup(groupName) {
    console.log(groupName)

    $.ajax({
        url:"/user/createGroup",
        type: "POST",
        data: {
            "groupName" : groupName
        },
        dataType: "json",
        success: function(resp) {
            console.log(resp)
        },
        error: function(resp) {
            // $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
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
