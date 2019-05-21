$(document).ready( function () {
  $('#myTable1').DataTable();
});


$("#div1").click((function loadDoc() {
  var loadForm = function GetEmployeeId(value) {
    $.ajax({
      url: btn.attr("employee_list.html"),
      type: 'post',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-popup").modal("show");
      },
      success: function (data) {
        $("#modal-popup. modal-content").html(data.html_form);
      }
    });
  };

var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#myTable1").html(data.emp_list);
          $("#modal-popup").modal("hide");
        }
        else {
          $("#modal-popup .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };
}

$("#myTable1").on("click", ".js-deactivate-employee", loadForm);
$("#modal-popup").on("submit", ".js-employee-deactivate-form", saveForm);




