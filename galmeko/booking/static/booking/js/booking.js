var loc = window.location;
var server_url = "" + loc.protocol + "//" + loc.host + '/';


$(document).ready(function () {
    var user_types = $("#id_booking_type").val();
    if (user_types != '') {
        get_userType_ById(user_types);
        $('.field-user').show();

    } else {
        $('.field-user').hide();
    }

    $(document).on('change', '#id_booking_type', function () {
        var user_type = this.value;
        if (user_type != '') {
            get_userType_ById(user_type);
        } else {
            $('.field-user').hide();
        }

    });

    function get_userType_ById(user_type) {
        if($('#id_user').val()){
            var user_id = $('#id_user').val();
        }else{
            user_id = ''
        }
        var token = $('input[name="csrfmiddlewaretoken"]').attr('value')
        var formData = {
            'user_type': user_type,
            'csrfmiddlewaretoken': token
        }
        $.ajax({
            method: "POST",
            url: server_url + 'admin/get_user_data/',
            data: formData,
            cache: false,
            success: function (data) {
                $('.field-user').css('display', 'block');
                var selectbox = $('#id_user');
                selectbox.empty();
                var list = '';
                var selected ='';
                if (data.status == true) {
                    $.each(data.data, function (k, v) {
                        if(v.id == user_id){
                           var selected = 'selected';
                        }else{
                            var selected = '';
                        }
                        var name = v['first_name'] + ' ' + v['last_name'];
                        list += "<option  class='cur_user_" + v.id + "' value='" + v.id + "' "+selected+">" + name + "</option>";
                    })
                } else { 
                    list += "<option value=''>" + data.data + "</option>";
                }
                selectbox.html(list);
            }
        });
    }

    // On Vehicle select get details
    $("<div class='vehicle_info'></div>").insertAfter("#add_id_vehicle");
    var vehicleId = $("#id_vehicle").val();
    if (vehicleId != '') {
        get_vehicleDetaile_ById(vehicleId);

    } else {
        $('.vehicle_info').hide();
    }
    $(document).on('change', '#id_vehicle', function () {
        var vehicleId = this.value;
        if (vehicleId != '') {
            $('.vehicle_info').show();
            get_vehicleDetaile_ById(vehicleId);
        } else {
            $('.vehicle_info').hide();
        }
    });

})

function get_vehicleDetaile_ById(vehicleId) {

    var token = $('input[name="csrfmiddlewaretoken"]').attr('value')
    var formData = {
        'vehicleId': vehicleId,
        'csrfmiddlewaretoken': token
    }
    $.ajax({
        method: "POST",
        url: server_url + 'admin/get_vehicle_detail/',
        data: formData,
        cache: false,
        success: function (data) {
            obj = data.data[0]
            html = '<span><b>Vehicle No :</b> <a href="javascript:void():">' + obj.vehicle_no + '</a> | <b>Mileage :</b> <span style="color:#007bff">' + obj.mileage + '</span> | <b>Chassis No :</b> <span style="color:#007bff">' + obj.chassis_no + '</span></span>';
            $('.vehicle_info').html(html);
        }
    });
}

// Google Map Autocomplete Code
function initAutocomplete() {
    new google.maps.places.Autocomplete(
        (document.getElementById('id_origin')),
        { types: ['geocode'], componentRestrictions: { country: 'IN' }, }

    );

    new google.maps.places.Autocomplete(
        (document.getElementById('id_destination')),
        { types: ['geocode'], componentRestrictions: { country: 'IN' }, }

    );
}

$(document).ready(function () {

    $('#id_origin ,#id_destination').blur(function () {
        origin = $('#id_origin').val();
        destination = $('#id_destination').val();
        if (origin != '' && destination != '') {
            get_lat_long(origin, destination);
        }
    });

})

function get_lat_long(origin, destination) {
    var token = $('input[name="csrfmiddlewaretoken"]').attr('value')
    var formData = {
        'origin': origin,
        'destination': destination,
        'csrfmiddlewaretoken': token
    }
    $.ajax({
        method: "POST",
        url: server_url + 'admin/get_lat_long/',
        data: formData,
        cache: false,
        success: function (data) {
            var origin = data.origin;
            var destination = data.destination;
            $('#id_origin_geocode').val(origin);
            $('#id_destination_geocode').val(destination);

        }
    });
}