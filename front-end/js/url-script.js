$('#btn-submit').click(function() {
    $.get("http://localhost:8081/", {
        vidurl: $('#txt-url')[0].value
    }, function() {
        setTimeout(function() {
            window.location = '/video.html';
        }, 1000);
    });
});