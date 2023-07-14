
// require("select2.js")

const fetchSiOrgs = () => {
    // Fetching institution by type
    $("#institution_type").on('change', function(e) {
        var si_type = $("#institution_type").val();
        var csrftoken = $.cookie('csrftoken');
        var values = {'si_type': si_type, 'action': 2,
                      'csrfmiddlewaretoken': csrftoken };
        $('#institution_name').empty();
        $.ajax({
            type: "POST",
            data: values,
            dataType: "json",
            url: "/si/si_lookup/",
            success: function(data){
                var wards = data.centres;
                console.log(wards)
                //$('#working_in_ward').html("<option value=''>Please Select</option>");           
                $.each(wards, function(i, record) {
                    var ward_attribs = wards[i][0].split(",");
                    $('#institution_name')
                        .append($("<option></option>")
                        .attr("value", ward_attribs[0])
                        .text(ward_attribs[1]));
                 });
                $('#institution_name').select2();
            },
            error: function(){
                $('#messages').html("Error")
            }
        });
    });
}