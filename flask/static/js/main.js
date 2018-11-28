// custom scripts

//navbar collapse
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, {});
  });


document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems, {});
  });




$(document).ready( function() {
     $('.edit').click(function() {
        const $row = $(this).closest("tr"),
        $tds = $row.find("td");

        const id = $row.find("input").val();
        const name=$($tds[0]).text();
        const address=$($tds[1]).text();
        const cod=$($tds[2]).text();
        const city=$($tds[3]).text();
        const phone=$($tds[4]).text();




        $.ajax({
                url: "/edit",
                method: "GET",
                data: {
                    edit_id: id,
                    name:name,
                    address:address,
                    cod:cod,
                    city:city,
                    phone:phone,
                }
            }).done(function() {
                console.log('Success');
            }).fail(function() {
                console.log('Something went Wrong');
            });


        });

     $(".numberedit").keypress(function(e) {
    if (isNaN(String.fromCharCode(e.which))) e.preventDefault();

    });

 });


