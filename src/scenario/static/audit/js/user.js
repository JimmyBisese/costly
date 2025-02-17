
// users_audit.js is loaded in to C:\inetpub\wwwdjango\gsicosttool\src\gsicosttool\templates\audit\users.html

$(function () {

    var is_superuser = false;
    var table;

    var simple_checkbox = function ( data, type, full, meta ) {
        var is_checked = data === true ? "checked" : "";
        if (data === true) {
            return '<span title="Active" class="glyphicon glyphicon-ok-sign-green"></span>';
        }
        else {
            return '<span title="Not Active" class="glyphicon glyphicon-remove-sign-red"></span>';
        }

    };

    /* Binding */
    $(document).ready(function() {

        var inputDom = document.getElementById('is_superuser');

        is_superuser = (inputDom) ? true : false;

        loadTable();
    });

    var loadTable = function() {

        var export_columns = [0, 1, 2, 3, 4, 5, 6, 7, 8];

        var options = {
          "serverSide": false,
          "ajax": SETTINGS.URLS.audit_user_data + '?format=datatables',
          "paging": false,
          "info": false,
          "dom": 'Bfrtip',
          "buttons": [
              'copy',
              {
                  'extend': 'csv',
                  'exportOptions': {'columns': export_columns}
              },
              'excel',
              'pdf',
              'print'
          ],
          "columns": [
              {"data": "id", "searchable": false},
               {'data': 'name', },
               {'data': 'organization_tx', "sortable": true},
               {'data': 'job_title', "sortable": true},
               {'data': 'profile.user_type', "sortable": true},
               {'data': 'email', },
               {'data': 'phone_tx', },

{               'data': 'is_active', "sortable": true, "render": simple_checkbox, },
               {'data': 'date_joined', "sortable": true},
               {'data': 'last_login', "sortable": true},
          ],
          "columnDefs": [
              {
                    "searchable": false,
                    "orderable": false,
                    "targets": 0
              },
          ],
          "order": [[ 1, 'asc' ]]
        };

        table = $('#users-table').DataTable(options);

        table.on( 'order.dt search.dt', function () {
            table.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
                cell.innerHTML = i+1;
            } );
        } ).draw();
    };







});
