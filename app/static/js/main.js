// Wrap each audio element with the MediaElementPlayer class
document.addEventListener("DOMContentLoaded", function () {
    const playerElements = document.getElementsByTagName("audio");

    for (let i = 0; i < playerElements.length; i++) {
        var player = new MediaElementPlayer(playerElements[i], {
            // List of features to enable for the player
            features: ['playpause', 'current', 'progress', 'duration', 'volume'],
            success: function (mediaElement, originalNode, instance) {
                // Callback function executed when the player is successfully initialized
                console.log("MediaElement", mediaElement); // The enhanced audio element
                console.log("originalNode", originalNode); // The original HTML5 <audio> element
                console.log("instance", instance); // The MediaElementPlayer instance
            }
        });
    }
});


// THANK YOU 
document.addEventListener('play', function (e) {
    var audios = document.getElementsByTagName('audio');
    for (var i = 0, len = audios.length; i < len; i++) {
        if (audios[i] != e.target) {
            audios[i].pause();
            reveal_stop();
        }
    }
}, true);

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

function fade() {
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

function check_if_playing() {
    var audio = document.getElementsByTagName('audio');
    var audio_players_count = audio.length;
    var total_count = 0
    for (var i = 0; i < audio.length; i++) {

        if (audio[i].paused) {
            total_count++
        }
    }
    if (total_count == audio_players_count) {
        hide_stop()
    }
}

function reveal_filter() {
    var filters = document.getElementsByClassName("select_episode");
    for (var i = 0; i < filters.length; i++) {
        filters[i].style.display = "inline-block"
    }
    var toggle_button = document.getElementById("filter_toggle")
    toggle_button.innerText = "TOGGLE"
    toggle_button.className = "btn btn-outline-primary"
}

// scroll to top of page
function scroll_to_top() {
    document.documentElement.scrollTop = 0
}

// if users scrolls down on page, enable arrow button

window.onscroll = function () { scrollFunction() };

function scrollFunction() {
    var pagePosition = 600;
    var mybutton = document.getElementById("up_arrow");
    if (document.body.scrollTop > pagePosition || document.documentElement.scrollTop > pagePosition) {
        mybutton.style.display = "block";
    } else {
        mybutton.style.display = "none";
    }
}