/**
 * Created with PyCharm.
 * User: arthur
 * Date: 7/07/13
 * Time: 10:16 AM
 * To change this template use File | Settings | File Templates.
 */

$(document).ready(function () {
    $('a[rel]').overlay({
        fixed: false
    });

    $('#slideshow').cycle({
        fx: 'fade',
        speed: 2500
    });

    /**
     * PayPal setting adjustments.
     */
    $('#payment_options').hide();
    $('select[name="booking_type"]').change(function () {
        var selected = $(this).val();
        if (selected == 1) {
            $('#payment_options').show();
            $('input[name="item_name"]').val('Report Only');
            $('input[name="amount"]').val('100');
            $('input[name="shipping"]').val('10');
        }
        else if (selected == 2) {
            $('#payment_options').show();
            $('input[name="item_name"]').val('Report & Consultation');
            $('input[name="amount"]').val('198');
            $('input[name="shipping"]').val('0');
        }
        else {
            $('#payment_options').hide();
            $('input[name="item_name"]').val('');
            $('input[name="amount"]').val('0');
            $('input[name="shipping"]').val('0');
        }
    });

    /**
     * Postcode validation.
     */
    $('#id_postcode').bind('input', function () {
        if ($(this).val().length == 4 && $(this).val()[0] != '2') {

        }
        else {

        }
    });

    /**
     * Conflicting items go below this line.
     */
    $.noConflict();
    $('#id_appointment_date').datepicker({
        dateFormat: 'dd/mm/yy'
    });
});
