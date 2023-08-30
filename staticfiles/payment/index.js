var stripe = Stripe(STRIPE_PUBLISHABLE_KEY);

var submitButton = document.getElementById('submit');
clientSecret = submitButton.getAttribute('data-secret');

var elements = stripe.elements();
var style = {
    base: {
        color: "#000",
        lineHeight: "2.4",
        fontSize: "16px"
    }
};
var card = elements.create("card", { style: style });
card.mount("#card-element");

card.on('change', function(event) {
    var displayError = document.getElementById('card-errors')
    if (event.error) {
        displayError.textContent = event.error.message;
        $('#card-errors').addClass('alert alert-info');
    } else {
        displayError.textContent = '';
        $('#card-errors').removeClass('alert alert-info');
    }
});

var form = document.getElementById('payment-form');

form.addEventListener('submit', function(event) {
    event.preventDefault();

    var city = document.getElementById("city").value;
    var country = document.getElementById("country").value;
    var address1 = document.getElementById("address1").value;
    var address2 = document.getElementById("address2").value;
    var postcode = document.getElementById("postcode").value;
    var email = document.getElementById("email").value;
    var firstname = document.getElementById("firstname").value;
    var lastname = document.getElementById("lastname").value;
    var phoneNumber = document.getElementById("phone-number").value;

    $.ajax({
        type: "POST",
        url: 'https://web-production-e9c3b.up.railway.app/orders/add/',
        data: {
            full_name: firstname + ' ' + lastname,
            phone_number: phoneNumber,
            address1: address1,
            address2: address2,
            country: country,
            city: city,
            post_code: postcode,
            order_key: clientSecret,
            csrfmiddlewaretoken: CSRF_TOKEN,
            action: "post",
        },
        success: function (json) {
            console.log(json.success)

            stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        address: {
                            city: city,
                            country: country,
                            line1: address1,
                            line2: address2,
                            postal_code: postcode,
                        },
                        email: email,
                        name: firstname + ' ' + lastname,
                        phone: phoneNumber,
                    },
                }
            }).then(function(result) {
                if (result.error) {
                    console.log('payment error')
                    console.log(result.error.message)
                } else {
                    if (result.paymentIntent.status === 'succeeded') {
                        console.log('payment processed')
                        // There's a risk of the customer closing the window before callback
                        // execution. Set up a webhook or plugin to listen for the
                        // payment_intent.succeeded event that handles any business critical
                        // post-payment actions.
                        window.location.replace("https://web-production-e9c3b.up.railway.app/payment/orderplaced/");
                    }
                }
            });
        },
        error: function (xhr, errmsg, err) {},
    });
});
