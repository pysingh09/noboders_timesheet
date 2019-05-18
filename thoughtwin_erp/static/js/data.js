$(document).ready( function () {
  $('#myTable1').DataTable();
});


$(document).ready(function(){
  $("button").click(function(){
    $.ajax({url: "demo_test.txt", success: function(result){
      $("#div1").html(result);
    }});
  });
});
function GetProductByManufacturerID(value) { 
  $.ajax({
    type: "POST",
    url: "add_rebate_by_quat_volume.php",
    data: { manufacturer_id: value, op:"" },
    beforeSend: function() { 
      
      $("#product_id").html('<option> Loading ...</option>');
      $("#search").prop('disabled', true);
    },
  });
}
