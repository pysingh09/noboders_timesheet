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



let valueArr =[]

function checkClicked(e){
    if(e.checked == true){
        valueArr.push(e.value);
        e.setAttribute("checked","checked");
        debugger
        valueArr = _.uniq(valueArr)
    }else{
        e.removeAttribute("checked");
        valueArr.pop(e.value);
        debugger
    }
}

$(document).on("click","#checkall",function (e){
    $(this).closest('table').find('td input:checkbox').prop('checked', this.checked);
    var is_checked = $(this).prop('checked');
    if (is_checked == true){
        var records= $(e.target).closest('table');
        $('td input:checkbox').each(function(){
            $(this).attr('checked',true);
            // valueArr = [];
            // debugger
            valueArr.push($(this).val());
            valueArr = _.uniq(valueArr)
        });
    }
    else{
        valueArr = []; 
        $('td input:checkbox').each(function(){
            $(this).attr('checked',false);

        });
    }
});

$(document).ready(function(){
    $('.delete-row').click(function(){
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
});


