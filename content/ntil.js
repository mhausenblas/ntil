var BASE_URL = "http://" + window.location.host;
var updates_timer;

// main event loop
$(document).ready(function() {
    console.info('Setting target date and topic …')
    getTargetDate();
    getTargetUpdates();
    
    $("#countdown").click(function(event) {
         getTargetTopic();
    });
    
    $("#updates").click(function(event) {
         $("#updates").fadeOut(500);
         getTargetUpdates();
    });
    
});

function getTargetDate() {
    var apicall = BASE_URL + '/service/target';
    $.getJSON(apicall, function(d) {
        $("#countdown").html(d.date);
        console.debug("GET " + apicall);
        console.debug(d);
        countDownTimer(d.date, 'countdown');
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

function getTargetUpdates() {
    var apicall = BASE_URL + '/service/updates';
    $.getJSON(apicall, function(d) {
        $("#updates").html("");
        for(u in d.update){
            $("#updates").append('<p>' + d.update[u] + '</p');
        }
        
        console.debug("GET " + apicall);
        console.debug(d);
        $("#updates").fadeIn(1000);
    });
}


// lifted from http://stackoverflow.com/questions/9335140/how-to-countdown-to-a-date
function countDownTimer(dt, id){
   var end = new Date(dt);
   var _second = 1000;
   var _minute = _second * 60;
   var _hour = _minute * 60;
   var _day = _hour * 24;
   var timer;

   function showRemaining() {
       var now = new Date();
       var distance = end - now;
       if (distance < 0) {
           clearInterval(timer);
           document.getElementById(id).innerHTML = 'EXPIRED!';
           return;
       }
       var days = Math.floor(distance / _day);
       var hours = Math.floor((distance % _day) / _hour);
       var minutes = Math.floor((distance % _hour) / _minute);
       var seconds = Math.floor((distance % _minute) / _second);

       document.getElementById(id).innerHTML = days + 'd ';
       document.getElementById(id).innerHTML += hours + 'h ';
       document.getElementById(id).innerHTML += minutes + 'm ';
       document.getElementById(id).innerHTML += seconds + 's';
   }

   timer = setInterval(showRemaining, 1000);
}