// $(document).ready(function(){ 
//   $("#no_record_in_table").hide();
//     $('#myTable1').DataTable({
//        pagingType: "simple",
//        fnInitComplete : function() {
//        if ($(this).find('tbody tr').length<=1) {
//          $(this).parent().hide();
//          $(".no_record_in_table").text("No records available").show();
//       }
//    }
//   });
// });


$(document).ready(function(){
  $('#myTable1').DataTable({
    // "paging": false,
    //  "lengthChange": true, // for show length change
    // "paging": false,  // for paging length

    
  });
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
                        
                        location.reload();
                }
            });
        }
    });
});

let csvRecoredArr =[];

    function delrow() {
     
        if (!$("input:checkbox").is(":checked"))  {
            alert("Please tick checkbox if you want to delete");
            location.reload();
            return false;
        }
        else($(".mychkboxs input[type=checkbox]:checked")).each(function () {
            csvRecoredArr.push($(this).val())
          });
      
           var confirmbox = confirm("Are you sure you want to Deleted selected records?")
           if (confirmbox == true)// confirm box
           {
              let pk = csvRecoredArr;
              $.ajax({
              'url': '/delete_record/',
              'type': "post",
              'dataType': 'json',
              'data': {
                  'data': pk,
                  'csrfmiddlewaretoken': '{{ csrf_token }}',
               },
               success: function(response) {
                   if(response.status=="success"){
                       location.reload();
                      }

                   }
               })
            }//end of conform box
            
    }

