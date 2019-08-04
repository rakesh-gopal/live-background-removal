$('#btn-submit').click(function() {
    var outid = parseInt(Math.random() * 100000).toString();
    $.get("http://localhost:8081/", {
        vidurl: $('#txt-url')[0].value,
        outid: outid
    }, function() {
        setTimeout(function() {
            window.location = '/video.html?outid=' + outid;
        }, 1000);
    });
});