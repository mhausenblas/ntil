var BASE_URL = "http://" + window.location.host;

// main event loop
$(document).ready(function() {
    console.info('Setting target date and topic …')
    getTargetDate();
    getTargetTopic();
    $("#updates").fadeOut(6000);
    
    $("#countdown").click(function(event) {
         $("#updates").fadeIn(1000);
         $("#updates").fadeOut(6000);
    });
});

function getTargetDate() {
    var apicall = BASE_URL + '/service/target';
    $.getJSON(apicall, function(d) {
        $("#countdown").html(d.date);
        console.debug("GET " + apicall);
        console.debug(d);
    });
}

function getTargetTopic() {
    var apicall = BASE_URL + '/service/topic';
    $.getJSON(apicall, function(d) {
        $("#updates").html('<p>Watching topic <em>' + d.topic + '</em> on Twitter.</p>');
        console.debug("GET " + apicall);
        console.debug(d);
    });
}