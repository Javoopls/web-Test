//const BASE_URL = 'http://127.0.0.1:8000/';
//const BASE_URL = 'https://www.payment.8pay.cl/';
const total_amount = document.getElementById('total_amount');
const form = document.getElementById('createPayment');
const button = document.getElementById('button');
const loading_icon = document.getElementById('loading_icon');

//EXPERIMENTACION
data = JSON.parse(data.innerHTML)
const ticket_id = data.ticket_id;
const business_name = data.business_name;

let products = {};
let total = 0;

total_amount.innerHTML = '$0';
loading_icon.style.display = "none";

function modifyAmount(e, id, precio) {
    if (e.checked) {
        total += parseInt(precio);
        products[id] === undefined ? products[id] = 1 : products[id] += 1;
    } else {
        total -= parseInt(precio);
        products[id] - 1 === 0 ? delete products[id] : products[id] -= 1
    }

    total_amount.innerHTML = `$${total}`;
}

form.addEventListener('submit', (ev) => {
    ev.preventDefault();

    const paymentRequest = {
        total_amount: total,
        ticket: {
            id: ticket_id,
            productos: products
        },
        business_order_number: parseInt(ticket_id),
        title: 'Boleta ' + business_name,
        description: ticket_id,
        return_url: '-'
    }

    button.setAttribute('disabled', 'true')
    loading_icon.style.display = "block"

    fetch(location.href, {
        method: 'POST',
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: JSON.stringify(paymentRequest)
    })
    .then(response => {
        if (response.status == 200) {
            window.location.href = response.url;
        }else{
            button.setAttribute('disabled', 'false')
            loading_icon.style.display = "none"
        }
    })
    .catch(error => {
        button.setAttribute('disabled', 'false')
        loading_icon.style.display = "none"
    });
});