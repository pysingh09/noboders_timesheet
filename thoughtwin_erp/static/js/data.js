$(document).ready( function () {
  $('table').DataTable();
});
    
$(document).ready(function(){
    $('.deactivateEmployee').click(function (event) {
             $(this).toggleClass('pressed');
        if (confirm('Are you sure you want to deactivate this?')) {
            var pk = parseInt($(this).val());
            $.ajax({
                'url': '/deactivate/'+pk+'/',
                'type': "POST",
                'dataType': 'json',
                'data': {
                    'pk': pk,
                    'is_active':$(this).data('is_active'),
                    'csrfmiddlewaretoken': '{{ csrf_token }}',
                },
                success: function(response) {
                    if(response.status=="success")
                        
                         // $(".deactivateEmployee").attr("disabled", false);
                        location.reload();
                }
            });
        }
    });
});




let valueArr =[];
// Case 1 : When Header Checkbox is ticked
$(document).on("click","#checkall",function(){ 
    var checked = $(this).prop('checked');
    $('.mychkboxs').find('input:checkbox').prop('checked', checked);
    
});

// Case 2 : When Multiple Checkbox is ticked/unticked

$(document).on("click","#delrow",function(){  

     $(".mychkboxs input[type=checkbox]:checked").each(function () {
                valueArr.push(this.value);
            });

        let pk = valueArr;
        $.ajax({
        'url': '/delete_record/',
        'type': "post",
        'dataType': 'json',
        'data': {
            'pk': pk,
            'csrfmiddlewaretoken': '{{ csrf_token }}',
        },
        success: function(response) {
            if(response.status=="success"){
                // alert("All record is Successfully Deleted!")
                alert("Are you sure you want to Deleted selected records?")
                location.reload();
                }

            }         
        })           
    });     


