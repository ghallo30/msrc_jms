
// $("#author-name").keyup(function() {
//         var dInput = $(this).val();
//         if($(this).val().length>0)
//           check_if_name_exist();
// });

// $("#author-mname").keyup(function() {
//         var dInput = $(this).val();
//         if($(this).val().length>0)
//           check_if_name_exist();
// });
// $("#author-lname").keyup(function() {
//         var dInput = $(this).val();
//         if($(this).val().length>0)
//           check_if_name_exist();
// });

// function check_if_name_exist(){
//   $.get('/admission/check_names',{fname:$("#patient-name").val(),mname:$("#patient-mname").val(), lname:$("#patient-lname").val()},
//     function(data){
//       if(data.exist=='no'){
//         $("#signup-button").prop('disabled',false);
//         $("#error_center").remove();
//       }else if(data.exist=='yes'){

//         $("#signup-button").prop('disabled',true);
//         $("#error_div").html("<center id='error_center' > <h5 class='alert alert-danger' id='error_messge' > Patient name already exist</h5>  </center>");
//       }
//     });
// }

// changed attribute for patient_field
$(document).ready(function() {

  if ($('#signup_form_page').val()){
    $("#signupForm").validate({
      errorElement: "em",
      errorPlacement: function(error, element) {
        $(element.parent("div").addClass("form-animate-error"));
        error.appendTo(element.parent("div"));
      },
      success: function(label) {
        $(label.parent("div").removeClass("form-animate-error"));
      },
      rules: {
        validate_firstname: "required",
        validate_lastname: "required",
        validate_username: {
          required: true,
          minlength: 4
        },

        validate_password: {
          required: true,
          minlength: 5
        },
        validate_confirm_password: {
          required: true,
          minlength: 5,
          equalTo: "#validate_password"
        },
        validate_email: {
          required: true,
          email: true
        },
        validate_agree: "required"
      },
      messages: {
        validate_firstname: "Please enter your firstname",
        validate_lastname: "Please enter your lastname",
        validate_username: {
          required: "Please enter a username",
          minlength: "Your username must consist of at least 4 characters"
        },
        validate_password: {
          required: "Please provide a password",
          minlength: "Your password must be at least 5 characters long"
        },
        validate_confirm_password: {
          required: "Please provide a password",
          minlength: "Your password must be at least 5 characters long",
          equalTo: "Please enter the same password as above"
        },
        validate_email: "Please enter a valid email address",
        validate_agree: "Please accept our policy"
      }
    });
  }
 
}); //document ready

function search_article() {
  dets=$('#search_msrc_content').val();
  
  if(dets.length>0){
    // alert('Searching');  
    window.location.replace("/msrc/search_article?search_text="+dets);
  }
  else{
    alert('Empty Field');
  }
  // window.replace.
}

function printArticle(){
  alert("printArticle");
  // $('#article_pdf').printArea();
  
}

