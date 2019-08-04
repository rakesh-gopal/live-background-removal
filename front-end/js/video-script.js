var green_ratio_threshold = 0.72;
var red_blue_ratio = 0.4;
var blue_red_ratio = 0.6;
var nt = 4;

jQuery(function() {

    var canvas = document.getElementById("mainCanvas");
    var context = canvas.getContext("2d");
    var cw, ch;

    var v = document.getElementById('tutor-video');

    v.addEventListener("loadedmetadata", function(e) {
        cw = canvas.width = v.videoWidth;
        ch = canvas.height = v.videoHeight;

        v.addEventListener('play', function() {
            requestAnimationFrame(animate);
        }, false);

    }, false);

    setTimeout(function() {
        cw = canvas.width = v.videoWidth;
        ch = canvas.height = v.videoHeight;

        v.addEventListener('play', function() {
            requestAnimationFrame(animate);
        }, false);

    }, 1000);

    function pixIndex(row, col) {
        if (row < 0 || col < 0 || row >= ch || col >= cw) {
            return -1;
        }
        return ((row * cw) + col) * 4;
    }

    function isSimilarColor(img, i, j) {
        var iRed = img[i];
        var iGreen = img[i + 1];
        var iBlue = img[i + 2];

        var jRed = img[j];
        var jGreen = img[j + 1];
        var jBlue = img[j + 2];

        if ((iRed == 0 && iGreen == 0 && iBlue == 0) || (jRed == 0 && jGreen == 0 && jBlue == 0)) {
            return true;
        }

        return Math.abs(iRed-jRed) < nt && Math.abs(iGreen-jGreen) < nt && Math.abs(iBlue-jBlue) < nt;
    }

    function growRegion(img, row, col, dx, dy) {
        var queue = [];
        var set = {};
        var cur = {row: row, col: col, i: pixIndex(row, col)};
        while (cur != null) {
            var i = cur.i;
            if (img[i+3] == 0 || i in set) {
                cur = queue.pop();
                continue;
            }
            img[i + 3] = 0;
            set[i] = true;

            var j = pixIndex(cur.row, cur.col+dx);
            if (j > 0 && isSimilarColor(img, i, j)) {
                queue.push({row: cur.row, col: cur.col + dx, i: j});
            }
            j = pixIndex(cur.row+dy, cur.col);
            if (j > 0 && isSimilarColor(img, i, j)) {
                queue.push({row: cur.row+dy, col: cur.col, i: j});
            }
            var j = pixIndex(cur.row, cur.col-dx);
            if (j > 0 && isSimilarColor(img, i, j)) {
                queue.push({row: cur.row, col: cur.col-dx, i: j});
            }
            j = pixIndex(cur.row-dy, cur.col);
            if (j > 0 && isSimilarColor(img, i, j)) {
                queue.push({row: cur.row-dy, col: cur.col, i: j});
               
            }

            cur = queue.pop();
        }
    }

    function animate(time) {

        if (v.paused || v.ended) {
            return;
        }

        // draw the 1 current video frame on the canvas
        context.drawImage(v, 0, 0, cw, ch);

        var imgData = context.getImageData(0, 0, cw, ch);
        var data = imgData.data;

        // growRegion(data, 10, 163, 1, 1);
        growRegion(data, 0, 0, 1, 1);
        growRegion(data, 0, cw-1, -1, 1);

        context.putImageData(imgData, 0, 0);

        // also draw your image on the canvas
        // context.drawImage(img,0,0);

        // request another loop 
        setTimeout(function() {
            requestAnimationFrame(animate);
        }, 50);
    }


    $("#btn-play").click(function() {
        $('#screencast-cont').css({opacity: 1.0});
        v.play();
        $('#screencast-video')[0].play();
        $(this).hide(1000);
    });

    function getQueryStringValue (key) {  
        return decodeURIComponent(window.location.search.replace(new RegExp("^(?:.*[&\\?]" + encodeURIComponent(key).replace(/[\.\+\*]/g, "\\$&") + "(?:\\=([^&]*))?)?.*$", "i"), "$1"));  
    }  
    
    setTimeout(function() {
        var src = 'media/video-out' + getQueryStringValue('outid') + '.mp4'; //'media/video-out.mp4';
        console.log(src);
        v.src = src;
        v.load();
        setTimeout(function(){
            $('#btn-play').css({opacity: 1.0});
        }, 2000)
    }, 100);

});
