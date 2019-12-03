$(document).ready(function(){
  var table = $('#myTable1').DataTable({
    stateSave: true,
    stateSaveCallback: function(settings,data) {
      localStorage.setItem( 'DataTables_' + settings.sInstance, JSON.stringify(data) )
    },
  stateLoadCallback: function(settings) {
    return JSON.parse( localStorage.getItem( 'DataTables_' + settings.sInstance ) )
    }
  });
});
    
$(document).ready(function() {
    // Setup - add a text input to each footer cell
    // $('#myTable2 thead tr').clone(true).appendTo( '#myTable2 thead ' );
    // $('#myTable2 thead tr:eq(1) th').each( function (i) {
    //     var title = $(this).text();
        
    //     if (i==2||i==4 || i==5 || i==6)

    //       $(this).html( '<input type="text" placeholder="Search" />' );
    //     if (i==12||i==7||i==8||i==9||i==10||i==11||i==0||i==1||i==3||i==13)
    //       $(this).html('<td</td>');   

    //     $( 'input', this ).on( 'keyup change', function () {
    //         if ( table.column(i).search() !== this.value ) {
    //             table

    //                 .column(i)
    //                 .search( this.value )
    //                 .draw();
    //         }
    //     } );
    // } );
 
    var table = $('#myTable2').DataTable( {
        orderCellsTop: true,
        ixedHeader: true,
         stateSave: true,
        stateSaveCallback: function(settings,data) {
          localStorage.setItem( 'DataTables_' + settings.sInstance, JSON.stringify(data) )
        },
        stateLoadCallback: function(settings) {
        return JSON.parse( localStorage.getItem( 'DataTables_' + settings.sInstance ) )
        }
    });
} );
 
$(document).ready(function(){
    $('#myTable2').on('click','.deactivateEmployee', function (event) {
    // $('.deactivateEmployee').click(function (event) {
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
  
   var confirmbox = confirm("Are you sure you want to Delete selected records?")
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

