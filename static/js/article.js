
$("#author-name").keyup(function() {
        var dInput = $(this).val();
        if($(this).val().length>0)
          check_if_name_exist();
});

$("#author-mname").keyup(function() {
        var dInput = $(this).val();
        if($(this).val().length>0)
          check_if_name_exist();
});

$("#author-lname").keyup(function() {
        var dInput = $(this).val();
        if($(this).val().length>0)
          check_if_name_exist();
});

function check_if_name_exist(){
  $.get('/admission/check_names',{fname:$("#patient-name").val(),mname:$("#patient-mname").val(), lname:$("#patient-lname").val()},
    function(data){
      if(data.exist=='no'){
        $("#signup-button").prop('disabled',false);
        $("#error_center").remove();
      }else if(data.exist=='yes'){

        $("#signup-button").prop('disabled',true);
        $("#error_div").html("<center id='error_center' > <h5 class='alert alert-danger' id='error_messge' > Patient name already exist</h5>  </center>");
      }
    });
}

// changed attribute for patient_field
$(document).ready(function() {

  // $("button#remove_coauthor").on('click', function() {
  //     $(this).parent().parent().remove()
  // });
  
  // $("#view-auth-modal").on('hide.bs.modal', function () {
		// $('#author_department').append(data.department)
		// $('#author_contact_num').append(data.contact_num)
		// $('#author_position_title').append(data.position_title)
		// $('#author_email_add').append(data.email_add)
		// $('#author_name').append(data.author_name)
  // });

}); //document ready

function remove_art_auth(auth_del, auth_name){    
	
	var r = confirm(auth_name +" will be deleted");
	if (r == true) {
		
		$("#"+auth_del).remove()

		$.get('/articles/remove-author',{art_auth:auth_del},
			function(data){
				if(data=='yes'){
	      	alert('Author has been removed ' + auth_name+ 'on the author list');
	      }
	      else{
			alert('Author ' + auth_name+ ' was not removed on the author list');		
		  }
		});
	} else {
		x = "You pressed Cancel!";
	}
	
}

function del_supp_file(file_det, art_filename){    
	
	var r = confirm(art_filename +" will be deleted");
	if (r == true) {
		
		

		$.get('/articles/remove-file',{file_del:file_det},
			function(data){
				if(data=='yes'){
					$("#"+file_det).remove()
	      	alert('File has been removed.');
	      }
	      else{
					alert('File was not removed on the author list');		
		  	}
		});
	} else {
		x = "You pressed Cancel!";
	}
	
}



function view_auth_info(art_in, auth_det){
  
  $.get('/articles/view-author-info',{art_auth:auth_det, art_det:art_in },
    function(data){
      if(data.success=='yes'){

        $('#author_department').append(data.department)
        $('#author_contact_num').append(data.contact_num)
        $('#author_position_title').append(data.position_title)
        $('#author_email_add').append(data.email_add)
        $('#author_name').append(data.author_name)
        
        $("#view-auth-modal").modal("show");        
      }
      else{
        alert('Unable to retreive author info');
      }
  });
}

function art_auth_form(){
  $("#add-auth-modal").modal("show");
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


// Submit post on submit
$('#art-auth-form').on('submit', function(event){
   
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    add_art_author(this);
});

// AJAX for posting
function add_art_author(its) {
    console.log("add article author is working!") // sanity check
    $.ajax({
        url : its.action, // the endpoint
        type : its.type, // http method
        beforeSend:  function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        data : its.serialize(), // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#post-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results_form_auth').html("<div class='alert alert-danger alert-outline alert-dismissible fade in' role='alert' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

};
