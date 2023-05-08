let openmodal = function (userid) {
    let modal = document.getElementById('turffor-' + userid);
    modal.style.display = 'block';
    document.getElementById("close-" + userid).addEventListener("click", function () {
        let modal = document.getElementById('turffor-' + userid);
        modal.style.display = 'none';
    });
}