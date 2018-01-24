function conectarArduino() {
	$.ajax({
        type: "GET",
        url: "Arduino",
    });
}

function pegarTemperatura() {
	$.ajax({
        type: "GET",
        url: "Temperatura",
        success: callbackFunc
    });
}

function callbackFunc(response) {
	$("#temperatura").text(response + "ºC");
    console.log(response);
}