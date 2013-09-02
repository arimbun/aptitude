/**
 * Created with PyCharm.
 * User: arthur
 * Date: 7/07/13
 * Time: 10:16 AM
 * To change this template use File | Settings | File Templates.
 */

$(document).ready(function () {
    /**
     * Twitter bootstrap compatibility.
     */
    $('label').attr('class', 'control-label');
    $('input').wrap('<div class="controls" />');
    $('select').wrap('<div class="controls" />');
    $('textarea').wrap('<div class="controls" />');

    /**
     * Overlays.
     */
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
    var environment = $('input[name="environment"]').val();
    if (environment == 'production') {
        $('input[name="env"]').val('www');
        $('input[name="business"]').val('info@aptitudeworld.com.au');
        $('input[name="notify_url"]').val('http://aptitude.herokuapp.com/email_confirmation');
        $('form[class="paypal-button"]').attr('action', 'https://www.paypal.com/cgi-bin/webscr');
    }


    $('input[name="book_submit"]').click(function () {

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
        dateFormat: 'dd/mm/yy',
        altField: '#id_appointment_date_post',
        altFormat: 'yy-mm-dd',
        minDate: 2
    });
});

/**
 * Checks if terms and conditions are agreed.
 */
function validateTocAgreed() {
    var toc_agreed = $('input[name="toc_agreement"]').is(':checked');
    if (!toc_agreed) {
        alert('You must agree to the terms and conditions');
        return false;
    }
    else {
        return true;
    }
}