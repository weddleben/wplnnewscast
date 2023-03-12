function toggleOnOff() {
    var checkboxes = document.getElementsByName("day");
    var yes = 0
    var no = 0
    // loop over them all
    for (var i = 0; i < checkboxes.length; i++) {
        // And stick the checked ones onto an array...
        if (checkboxes[i].checked) {
            yes++
        } else {
            no++
        }
    }
    if (yes > no) {
        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].checked) {
                // do nothing
            } else {
                checkboxes[i].click()
                stop_all()
            }
        }
    }
    if (yes < no) {
        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].checked) {
                checkboxes[i].click()
            }
        }
    }
    if (yes == checkboxes.length) {
        for (var i = 0; i < checkboxes.length; i++) {
            checkboxes[i].click()
            stop_all();
        }
    } else {
        for (var i = 0; i < checkboxes.length; i++) {
            checkboxes[i].click()
        }
    }
}