var BASE_URL = "http://" + window.location.host;

// main event loop
$(document).ready(function() {
    init(); 
});

function init() {
    var apicall = BASE_URL + '/service/target';
    $.getJSON(apicall, function(d) {
        $("#countdown").html(d.date);
        console.log("GET " + apicall);
    });
}