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
// Case 1 : When Header Checkbox ticked
$(document).on("click","#checkall",function(){ 
    $('.mychkboxs').find(':checkbox').each(function(){
        valueArr.push($(this).val());
        $(this).prop("checked",true);
    })

});

// Case 2 : When Multiple Checkbox is ticked
// $(document).on("click",".action-select",function(){    
//     //push the value only if it is checked
//     //Check if this is checked or not
    
//     var is_checked = $(this).is(':checked');
//     if (is_checked === true){
//         valueArr.push($(this).val());
//         console.log(valueArr);
//     }
//     else{
//         valueArr.pop($(this).val());
//         console.log(valueArr);
//     }

// });

// Case 3 : When Header Checkbox is unticked




$(document).on("click","#delrow",function(){  

     $(".mychkboxs input[type=checkbox]:checked").each(function () {
                debugger
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
                alert("All record is Successfully Deleted!")
                location.reload();
                }                                   
            }         
        })           
    });     


