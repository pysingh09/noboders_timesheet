$(document).ready( function (){
  $('#myTable1').DataTable();
});
    
$(document).ready(function(){
    $('.deactivateEmployee').click(function (event) {
        console.log("event", event)
             $(this).toggleClass('pressed');
        if (confirm(`Are you sure you want to ${event.target.id} this?`)) {
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


let csvRecoredArr =[];
// Case 1 : When Header Checkbox is ticked
$(document).on("click","#checkall",function(){
    var checked = $(this).prop('checked');
    $('.mychkboxs').find('input:checkbox').prop('checked', checked);
    // $('.attendence_datetime').find(':checkbox').each(function(){
    //     csvRecoredArr.push($(this).val());
    //     csvRecoredArr = _.uniq(csvRecoredArr)
    // })
}); 

// Case 2 : When Multiple Checkbox is ticked/unticked

$(document).on("click","#delrow",function(){
     $(".mychkboxs input[type=checkbox]:checked").each(function () {
        // $(".attendence_datetime").on('click',function(){
            
                csvRecoredArr.push(this.value);
                csvRecoredArr = _.uniq(csvRecoredArr)
                // csvRecoredArr.push({"date":$(this).data("checkeddate")});
            // })
        });

        let pk = csvRecoredArr;
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


