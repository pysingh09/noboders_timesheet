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

// let csvRecoredArr =[];
// // Case 1 : When Header Checkbox is ticked
// // $(document).on("click","#checkall",function(){
// //    var checked = $(this).prop('checked');
// //    $('.mychkboxs').find('input:checkbox').prop('checked', checked);

// //        // csvRecoredArr.push($(this).val());
// //        // csvRecoredArr = _.uniq(csvRecoredArr)
// // });

// // Case 2 : When Multiple Checkbox is ticked/unticked
// // data = {};
// // data.update({'emp_id':'122','date':'12-12-12'});

// $(document).on("click","#delrow",function(){
//     // e.preventDefault();
//     $(".mychkboxs input[type=checkbox]:checked").each(function () {
//            // csvRecoredArr.push(this.value);
//            // csvRecoredArr = _.uniq(csvRecoredArr);
//            // $(".attendence-datetime").on('click',function(){
//                // debugger
//                var date = $(this).data('date');
//                // var emp_id = $(this).data('employee-id');
//                // data.update({'date':'date','emp_id':'emp_id'})
//                debugger
//                csvRecoredArr.push(date)
//                // csvRecoredArr.push(emp_id)
//                csvRecoredArr = _.uniq(csvRecoredArr);
//                // csvRecoredArr.push({"date":$(this).data('date')});
//            // })
//        // });
//        debugger
//        let pk = csvRecoredArr;
//        // var date = $(this).data('date');
//        // var emp_id = $(this).data('employee-id');
//        // let emp_id = emp_id
//        // let date = date;
//        $.ajax({
//        'url': '/delete_record/',
//        'type': "POST",
//        'dataType': 'json',
//        'data': {

//            'pk': pk,
//            // 'emp_id' : emp_id,
//            // 'date':date,
//            // 'csvRecoredArr':csvRecoredArr,
//            'csrfmiddlewaretoken': '{{ csrf_token }}',
//        },
//        success: function(response) {
//            if(response.status=="success"){
//                // alert("All record is Successfully Deleted!")
//                alert("Are you sure you want to Deleted selected records?")
//                location.reload();
//                }

//            }
//        })
//    });

//   });

let csvRecoredArr =[];
// Case 1 : When Header Checkbox is ticked
$(document).on("click","#checkall",function(){
   var checked = $(this).prop('checked');
   $('.mychkboxs').find('input:checkbox').prop('checked', checked);
});

$(document).on("click","#delrow",function(){
    $(".mychkboxs input[type=checkbox]:checked").each(function () {
         
               var date = $(this).data('date');
               var emp_id = $(this).data('employee-id');
               csvRecoredArr.push(date)
               csvRecoredArr.push(emp_id)
               csvRecoredArr = _.uniq(csvRecoredArr);
       });
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
               alert("Are you sure you want to Deleted selected records?")
               location.reload();
               }

           }
       })
   });