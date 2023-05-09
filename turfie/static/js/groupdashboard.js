let openmodal = function (userid) {
    let modal = document.getElementById('turffor-' + userid);
    modal.style.display = 'block';
    document.getElementById("close-" + userid).addEventListener("click", function () {
        let modal = document.getElementById('turffor-' + userid);
        modal.style.display = 'none';
    });
}

let copyInviteLink = function (groupid) {
    navigator.clipboard.writeText('127.0.0.1:5000/join/' + groupid); 
    document.getElementById("inviteButton").innerHTML = "Copied!";

    setTimeout(function () {
        document.getElementById("inviteButton").innerHTML = "Invite others";
    }, 2000);
}