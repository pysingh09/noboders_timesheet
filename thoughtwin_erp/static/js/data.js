// $(document).ready( function () {
//   $('#myTable1').DataTable();
// });


// $(document).ready(function(){
//   $("button").click(function(){
//     $.ajax({url: "employee_list.html", success: function(result){
//       $("#div1").html(result);
//     }});
//   });
// });
 // alert("The paragraph was clicked.");
// $(document).ready(function(){
//     $("#btnid").click((function() {
//   var loadForm = function GetEmployeeId(value) {
//     $.ajax({
//       url: "deactivtae.html",
//       type: 'POST',
//       beforeSend: function() {
//         $("#modal-popup").modal("show");
//       },
//       success: function (data) {
//         $("#modal-popup. modal-content").html(data.html_form);
//       }
//     });
//   };
// });
// })

$(document).ready(function(){

    $('.deactivateEmployee').click(function (event) {

        if (confirm('Are you sure you want to delete this?')) {
            var pk = parseInt($(this).val());

            $.ajax({
                'url': '/deactivate/'+pk+'/',
                'type': "POST",
                'dataType': 'json',
                'data': {
                    'pk': pk,
                    'csrfmiddlewaretoken': '{{ csrf_token }}',
                },
                success: function (res) {

                    console.log(data)

                  // does some stuff here...
                }
            });
        }
    });
});

// var saveForm = function () {
//     var form = $(this);
//     $.ajax({
//       url: form.attr("action"),
//       data: form.serialize(),
//       type: form.attr("method"),
//       success: function (data) {
//         if (data.form_is_valid) {
//           $("#myTable1").html(data.emp_list);
//           $("#modal-popup").modal("hide");
//         }
//         else {
//           $("#modal-popup .modal-content").html(data.html_form);
//         }
//       }
//     });
//     return false;
//   };

// var saveForm = function () {
//     var form = $(this);
//     $.ajax({
//       url: form.attr("action"),
//       data: form.serialize(),
//       type: form.attr("method"),
//       dataType: 'json',
//       success: function (data) {
//         if (data.form_is_valid) {
//             $("#myTable1").html(data.emp_list);
//             $("#modal-popup").modal("hide");
//         }
//         else {
//           $("#modal-book .modal-content").html(data.html_form);
//         }
//       }
//     });
  //   return false;
  // };