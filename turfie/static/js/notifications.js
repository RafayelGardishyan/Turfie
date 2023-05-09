let removenotification = function (notificationid) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "notification/read/" + notificationid, true);
    xhttp.send();
    // refresh page
    setTimeout(function () {
        location.reload();
    }, 1000);
}