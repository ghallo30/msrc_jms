//elms hospital id auto gen
$('#gen_hospital_id_btn').click(function(){
    $.ajax({
  url : '/admission/generate_hospital_id',
  
  dataType : 'html',
  success : function(data){
      $("#patient_hospid").val(data);
  }
    });
});

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

}); //document ready

function art_nxt_form(t){
  // alert('aasd');
  // $('#tab-submission').tab('show');
  $('#tab-submission li:eq(1) a').tab('show')
}

function art_prev_form(t){
  // alert('aasd');
  // $('#tab-submission').tab('show');
  $('#tab-submission li:eq(1) a').tab('show')
}