function openform(){
    document.getElementById("myform").style.display="block";  
}
function closeform(){
    document.getElementById("myform").style.display="none";
};

function isLeapYear(y) {
    return ((y % 4 == 0) && (y % 100 != 0)) || (y % 400 == 0);
}

$(document).ready(function() {
    var today = new Date();
    var first = new Date();
    first.setDate(1);

    // Today
    $(".days span").eq(today.getDate() - 1).addClass("today");

    // First day of month
    var bodyClass = "day" + first.getDay();

    // Days in month
    bodyClass += " month" + first.getMonth();

    // Leap year
    bodyClass += isLeapYear(today.getFullYear()) ? " leap" : "";

    $("body").addClass(bodyClass);

});