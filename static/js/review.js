
// changed attribute for patient_field
$(document).ready(function() {
  
  PNotify.prototype.options.styling = "bootstrap3";

  
  $("button#send_review_request").on('click', function() {
     send_reviewer_request(); 
  });



  $("button#is_send_email").on('click', function() {
		$("#email_temp_form").show();
		$("#chk_if_send_btn").hide();
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

function submit_review(revs_id){

  inurl='/reviews/submit_review';
  revs=$('#reviewer_decision').val();
  $.get(inurl, { revs_info:revs_id, recommend_val:revs}, function(data){  
        if(data.success=='yes'){
          
          new PNotify({
            title: 'Review Submitted',
            text: 'Your review is successfully submitted.',
            type: 'success',
            delay: 3000,
            addclass: 'translucent',
          });

          $('#reviewer_recommend_panel div').remove();
          $('#reviewer_recommend_panel').append(
            data.recommend+'<br/><p> Date Review Submitted: '+data.recommend_date +'</p>'
          );
          
        } else {
          new PNotify({
            title: 'Error!',
            text: 'Unable to submit Review. Try to resubmit recommendation.',
            type: 'error',
            delay: 3000,
            addclass: 'translucent',
          });
        }
      } );
}