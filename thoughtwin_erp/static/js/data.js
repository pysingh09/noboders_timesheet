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



// let valueArr =[]
// function checkClicked(e){

//     valueArr.push(e.value)
// }



let valueArr =[]
function checkClicked(e){
    valueArr.push(e.value)
}

$(document).ready(function(){
    $('.delete-row').click(function(){
        // debugger
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
                        if(response.status=="success")
                            location.reload();
                        
                            
                }         
        })           
    });     
    });
