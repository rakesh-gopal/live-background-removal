var green_ratio_threshold = 0.72;
var red_blue_ratio = 0.4;
var blue_red_ratio = 0.6;
var nt = 5;

jQuery(function() {

    var canvas = document.getElementById("mainCanvas");
    var context = canvas.getContext("2d");
    var cw, ch;

    var v = document.getElementById('mainVideo');

    v.addEventListener("loadedmetadata", function(e) {

        cw = canvas.width = v.videoWidth;
        ch = canvas.height = v.videoHeight;

        v.addEventListener('play', function() {
            requestAnimationFrame(animate);
        }, false);

    }, false);

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

        growRegion(data, 0, 0, 1, 1);
        growRegion(data, ch-1, cw-1, -1, -1);
        growRegion(data, ch-1, 0, 1, -1);
        growRegion(data, 0, cw-1, -1, 1);

        // enumerate all pixels
        // each pixel's r,g,b,a datum are stored in separate sequential array elements

        // for (var row = 0; row < ch; row++) {
        //     for (var col = 0; col < cw; col++) {
        //         var i = pixIndex(row, col)
        //         if(data[i + 3] == 0) continue;
        //         var i = pixIndex(row, col);
        //         var red = data[i];
        //         var green = data[i + 1];
        //         var blue = data[i + 2];

        //         if (green / (red + blue) > green_ratio_threshold &&
        //             red / blue > red_blue_ratio &&
        //             blue / red > blue_red_ratio) {
        //             data[i + 3] = 0;
        //         }
        //     }
        // }

        context.putImageData(imgData, 0, 0);

        // also draw your image on the canvas
        // context.drawImage(img,0,0);

        // request another loop 
        setTimeout(function() {
            requestAnimationFrame(animate);
        }, 50);
    }


    $("#btn-play").click(function() {
        v.play();
    });

});
