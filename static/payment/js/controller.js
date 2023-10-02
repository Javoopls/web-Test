// Get the container element
var btnContainer = document.getElementById("myDIV");

// Get all buttons with class="btn" inside the container
var btns = btnContainer.getElementsByClassName("pmbtn");

// Loop through the buttons and add the active class to the current/clicked button
for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function() {
        var current = document.getElementsByClassName("active");
        current[0].className = current[0].className.replace(" active", "");
        this.className += " active";
    });
}



// ----------------------------------------------------------------------------- 



//const BASE_URL = 'http://127.0.0.1:8000/';
const BASE_URL = 'https://www.payment.8pay.cl/';

function pay(method, paymentid){
    let requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };
    const url = BASE_URL+'pay/'+method+'/'+String(paymentid)+'/js';
    console.log(url);
    fetch(url, requestOptions)
    .then(response => response.text())
    .then(result => {
        switch(method){
            case "mach":
                initMach(result);
                break;
            case "webpay":
                initWebpay(result);
                break;
        }
    }).catch(error => console.log('error', error));
}

function initWebpay(result){
    window.open(BASE_URL+"payment/webpay/"+result);
}

function initMach(result){
    console.log(result);
    generateQRCode(result);
}

// function isWeb(){
//     return !(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent));
// }

function generateQRCode(data) {
    console.log('init qr code')

    let qrcode = document.getElementById("qrcodeid");

    var QR_CODE = new QRCode("qrcodecontainer", {
		width: 180,
		height: 180,
		colorDark: "#000000",
		colorLight: "#ffffff",
		correctLevel: QRCode.CorrectLevel.H,
	});
    QR_CODE.clear();

    document.getElementById("qrcodecontainer").className = "box-left text-center";
    document.getElementById("qrcodecontainerp").className = "fw-bold";
    qrcode.className = "svg-visa";
    qrcode.scr = QR_CODE.makeCode(data);
}