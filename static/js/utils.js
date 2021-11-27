function timeOffsetToHHMM(offset) {
    hours = Math.round(offset / 3600);
    mins = offset - hours * 3600;

    return `${hours.toString().padStart(2, 0)}:${mins.toString().padStart(2, 0)}`;
}

function timestampToHHMM(timestamp, gmtOffset = +8) {
    var offsetSeconds = gmtOffset * 3600
    var dt = new Date((timestamp - offsetSeconds) * 1000);
    return `${dt.getHours().toString().padStart(2, 0)}:${dt.getMinutes().toString().padStart(2, 0)}`
}

function timestampToHHMMAMPM(timestamp, gmtOffset = +8) {
    var offsetSeconds = gmtOffset * 3600
    var dt = new Date((timestamp - offsetSeconds) * 1000);

    var ampm = dt.getHours() > 12 ? "PM" : "AM"
    var hours = dt.getHours() > 12 ? dt.getHours() - 12 : dt.getHours()

    return `${hours}:${dt.getMinutes().toString().padStart(2, 0)} ${ampm}`
}

function HHMMtotimestamp(hhmm) {
    var hhmmSplit = hhmm.split(":");
    var hours = parseInt(hhmmSplit[0], 10);
    var mins = parseInt(hhmmSplit[1], 10);


    return 3600 * hours + 60 * mins;
}