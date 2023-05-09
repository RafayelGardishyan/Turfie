let opengroupcreatemodal = function () {
    let groupmodal = document.getElementById("creategroupmodal");
    groupmodal.style.display = "block";

    document.getElementById("close").onclick = function () {
        groupmodal.style.display = "none";
    }
}