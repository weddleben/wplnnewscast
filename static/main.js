/*
controls the TOGGLE button. called when button is clicked
*/
function toggleOnOff() {
    // this is so ugly and i'm sorry
    var checkboxes = document.getElementsByName("day");
    var yes = 0
    var no = 0
    for (var i = 0; i < checkboxes.length; i++) {
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
                // stop_all()
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
            // stop_all();
        }
    } else {
        for (var i = 0; i < checkboxes.length; i++) {
            checkboxes[i].click()
            // stop_all()
        }
    }
}
/*
toggle episodes on/off. called by the toggle button, or the individual checkboxes.
*/
function episodes_by_time(a) {
    var episodes = document.getElementsByClassName(a);
    for (var i = 0; i < episodes.length; i++) {
        if (episodes[i].style.display === "none") {
            episodes[i].style.display = ""
        } else {
            episodes[i].style.display = "none"
        }
    }
    update_count()
}


/*
update episode count at top of page. called when episodes are toggled on/off
*/

function update_count() {
    var something = document.getElementsByClassName("episode");
    var number = 0
    for (var i = 0; i < something.length; i++) {
        if (window.getComputedStyle(something[i]).display != "none") {
            number++
        }
    }
    document.getElementById("episode_count").innerHTML = `<em> showing ${number} newscasts`
}

// fade in elements on start

function fade(){
    var to_fade = document.getElementsByClassName('to_fade1');
    for (var i = 0; i < to_fade.length; i++) {
        to_fade[i].classList.add('to_fade2')
    }
}

 /*
 stop all audio players
 */ 
 function stop_all() {
    var audios = document.getElementsByTagName('audio');
    for (var i = 0, len = audios.length; i < len; i++) {
            audios[i].pause();
    }
}

function reveal_stop() {
    stop_button = document.getElementById("stop_button");
    stop_button.style.display = "block"
}

function hide_stop() {
    stop_button = document.getElementById("stop_button");
    stop_button.style.display = "none"
}
