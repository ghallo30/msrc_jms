
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
  
  PNotify.prototype.options.styling = "bootstrap3";

  // $("#add_reivewer_modal").on('hidden.bs.modal', function () {

  // });
  

  $("#rev_end_week").keypress(function (e){
		var charCode = (e.which) ? e.which : e.keyCode;
		if (charCode > 31 && (charCode < 48 || charCode > 57)) {
			return false;
		}
	});

	$("button#send_review_request").on('click', function() {
     send_reviewer_request(); 
  });

  $("#email_temp_form").hide();

  $("button#is_send_email").on('click', function() {
		$("#email_temp_form").show();
		$("#chk_if_send_btn").hide();
  });

  $("#info_message").hide();
  
  $("#reviewer_field").keyup(function() {   
        var dInput = $(this).val();
        if($(this).val().length>0)
          search_for_reviewer(dInput); 
  });

  $("#editor_field").keyup(function() {   
        var dInput = $(this).val();
        if($(this).val().length>0)
          search_for_editor(dInput); 
  });

  $("#author-lname").keyup(function() {
        var dInput = $(this).val();
        if($(this).val().length>0)
          check_if_name_exist();
  });

}); //document ready

// function get_assign_email_template(art_det, assoc_edit){ 
//   // alert('Note this will remove the said author on the list');
//   // alert(assoc_editor+"---"+art_det);
//   $.get('/joumsy/assign_submission_editor',{assoc_editor:assoc_edit, sub_info:art_det , tempform:'assign_editor'},
//     function(data){
//       if(data.success=='yes'){
//       }
//       else{
//       }
//   });
// }

function view_select_issue(art_det, art_title){

  $("#article_curr_info").val(art_det);
  $("#art_title_issue h3").remove();
  $("#art_title_issue").append("<h3>"+art_title+"</h3>");
  $('#assign_issue_modal').modal('show');

}

function publish_issue(issue_det, iss_det){

  
  var inurl ='/joumsy/publish_issue'
  
  $.get(inurl, { issue_info:issue_det }, function(data){  
    if (data=='yes'){
      alert(iss_det+ ' has been published. ');
    }
    else if(data=='no_article'){
      
      alert(' No article is assigned on this issue. '); 

    }
    
  } );
}

function assign_issue_publish(){

  var issue_art=$('#issue_select').val();
  var art=$('#article_curr_info').val();
  var inurl ='/joumsy/assign_issue_publish'
  
  $.get(inurl, { art_det:art, issue_det:issue_art }, function(data){  

    $('#assign_issue_modal').modal('hide');  
    window.location.replace("joumsy/submission/published/");
  } );
}

function get_review_response(review_res ){

	inurl='/joumsy/view_reviewer_response';
	
	$.get(inurl, { review_det:review_res }, function(data){
		
		$('#reviewer_form_response').html(data);

		$('#view_reivewer_response').modal('show');  
	} );
}

function initial_reject_submission(art_in, sub_info){

  inurl='/joumsy/reject_submission';
  sub = sub_info
  $.get(inurl, { art_det:art_in }, function(data){
    if(data.success=='yes'){
      new PNotify({
            title: 'Submission Rejected',
            text: 'Submission <i>'+ data.submit_info+'</i> - has been moved to archieved.',
            type: 'success',
            delay: 3000,
            addclass: 'translucent',
      });  
      
      $('#editor_box').remove()
      $('#dec_mensahe').append('Submission Rejected ');
    } else{
      new PNotify({
            title: 'Error Processing.',
            text: 'Unable to reject the submission <i>'+sub+'</i>  ',
            type: 'error',
            delay: 3000,
            addclass: 'translucent',
      });
    } 
    
  });
}


function accept_assoc_editor(assoc_editor, art_det){
  // alert('Note this will remove the said author on the list');
  // alert(assoc_editor+"---"+art_det);
  $.get('/joumsy/accept_submission_editor',{ass_editor:assoc_editor},
    function(data){
      if(data.success=='yes'){
        alert('Editor - ' + data.ass_edit + ' has been assigned to '+ data.art_title);
        
        $('#editor_box div').remove();
        
        window.location.replace("/joumsy/sub_info/"+data.art_ident+"/review/");

      }
      else{
        $('#editor_box').append(
          ' <p>'+data.message+'<p>'
        );
      }
  });
}


function assign_assoc_editor(assoc_editor, art_det, is_him){    
  // alert('Note this will remove the said author on the list');
  // alert(assoc_editor+"---"+art_det);
  $.get('/joumsy/assign_submission_editor',{ass_editor:assoc_editor, art_curr:art_det},
    function(data){
      if(data.success=='yes'){
        
        if(is_him){
        	alert('Editor - ' + data.ass_edit + ' has been assigned to '+ data.art_title);
        }
        window.location.replace("/joumsy/sub_info/"+data.art_ident+"/review/");

        $('#editor_box div').remove();
        
        $('#editor_box').append(
          '<h4>'+data.ass_edit+'</h4> <p>You must assign Reviewer(s) to complete peer-reiview process.<p>'
        );
      }
      else{
        $('#info_message div div').remove();

        $('#info_message div').append(
          '<div class="alert alert-danger alert-outline alert-dismissible fade in" role="alert">'
			+'<button type="button" class="close" data-dismiss="alert" aria-label="Close">'+
			+'<span aria-hidden="true" style="font-size:1.5em; color:#000000;"><strong>×</strong></span></button>'
			+'	    	<strong>Oops!</strong> '+data.message+
				    +'</div>'
        );
      }
  });
}

/** continue this... add alert on email template if template does not exist**/
function send_reviewer_request(a_curr, rev){
  var inurl;
  inurl='/joumsy/assign_submission_reviewer';

  $("#to_user").val();
  $("#email_subject").val();
  $("#email_content").val();
   alert("processing assgin review");
  $.get(inurl, { assigned_reviewer:rev, sub_info:a_curr }, function(data){  
        if(data.success=='yes'){
        	
        	new PNotify({
        		title: 'Assigned Reviewer',
        		text: 'Reviewer '+ data.submit_reviewer+'has been invited to review the submission ',
        		type: 'success',
        		delay: 3000,
        		addclass: 'translucent',
        	});

        	$('#invite_reivewer_modal').modal('hide');
        	$('#reviewer_table').append('<tr><td>'+data.submit_reviewer +'</td><td>Waiting for confirmation.</td></tr>')
        } else {

          new PNotify({
            title: 'Error',
            text: '<p>Unable to assign reviewer </p>'+ data.message,
            type: 'error',
            delay: 3000,
            addclass: 'translucent',
          });
        }

      } ); 
}

function invite_reviewer_form(rev, a_curr){
  var inurl;
  inurl='/joumsy/invite_email';
  
  $.get(inurl, {assigned_reviewer:rev, sub_info:a_curr, tempform:'invite_reviewer' }, 
    function(data){      
          $('#email_temp_form').html(data);
          $("#invite_reivewer_modal").modal("show");
          

          // $( '#email_content' ).ckeditor().replace()
          CKEDITOR.replace( 'email_content' )
          // alert(data.email_content)
          // $( '#email_content' ).val(data.email_content );
      } );

  
}


function art_auth_form(){
  $("#add-auth-modal").modal("show");
}

// view_select_issue

function search_for_reviewer(textfield){
  var search_text;
  var itemSelect;
  var ins;
  var inurl;
  search_text = textfield;
  g=$("#article_curr_info").val();
  inurl='/joumsy/search_reviewer';

  // alert(search_text);
  var pathname = window.location.pathname;

  $.get(inurl, {  search_text:search_text, art:g },
    function(data){
        $('#reviewer_search_results').html(data);  
      }
  );
}

function search_for_editor(textfield){
  var search_text;
  var itemSelect;
  var ins;
  var inurl;
  search_text = textfield;
  g=$("#article_curr_info").val();

  inurl='/joumsy/search_editor';
  var pathname = window.location.pathname;

  $.get(inurl, {  search_text:search_text, art:g },
    function(data){
        $('#editor_search_results').html(data);  
      }
  );
}


function editor_decision_form(decs_id){
  $('#editor_decision_modal').modal('show');
}

function submit_decision(decs_id){

  inurl='/joumsy/submit_decision';
  revs=$('#editor_decision').val();
  ed_note=$('decision_note').val();

  $.get(inurl, { art_det:decs_id, recommend_val:revs, eddie_note:ed_note }, function(data){  
        if(data.success=='yes'){
          
          new PNotify({
            title: 'Success',
            text: 'Your decision is successfully submitted.<br/>' + data.recommend_date,
            type: 'success',
            delay: 3000,
            addclass: 'translucent',
          });

          $('#eddie_recommend div').remove();
          $('#eddie_recommend').append(
            data.recommend+'<br/><p> Date Review Submitted: '+data.recommend_date +'</p>'
          );

          $('#editor_decision_modal').modal('hide');
          
        } else {
          new PNotify({
            title: 'Error!',
            text: 'Unable to submit Decision. Try to resubmit decision.',
            type: 'error',
            delay: 3000,
            addclass: 'translucent',
          });
        }
      } );
}
