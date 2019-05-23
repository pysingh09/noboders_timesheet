$(document).ready( function () {
  $('#myTable1').DataTable();
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

$(document).ready(function(){
    $('#delrow').click(function(){
        // debugger
        var pk = $('.action-select').is(":checked")
        // debugger
            $.ajax({
                'url': '/delete_record/'+pk+'/',
                'type': "POST",
                'dataType': 'json',
                'data': {
                    'pk': pk,
                    'csrfmiddlewaretoken': '{{ csrf_token }}',
                },
                success: function(response) {
                        if(response.status=="success")
                            location.reload();
                            
                
        }           
    });
    });
});

// $("table tbody").find('input[name="record"]').each(function(){
//                     if($(this).is(":checked")){
//                         $(this).parents("tr").remove();
//         }
//             });