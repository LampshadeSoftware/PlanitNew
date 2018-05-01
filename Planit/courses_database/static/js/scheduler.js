

let scheduleIndex = 0;  // Used to display what schedule the user is currently viewing
let numSchedules = 0;  // Is the number of schedules for the given filters
let creditCounts = [];  // The numbers of credits for each scheduleIndex
let schedules = [[{}]];  // this will be used by FullCalendar so keep this format

// General course info. Doesn't change based on schedule index
let coursesInfo = {};  // Is a dictionary that maps "subject+course_id" to an info dict for that course

$(document).ready( function () {
    // localStorage.clear();

    // SETS UP CALENDAR
    calendarInit();

    // SETS UP TABLES
    tablesInit();

    // SETS UP FILTERS WITH MULTIPLE SELECT
    filtersInit();

    // DEALS WITH THE TABS FEATURE
    $(".nav-tabs a").click(function(){
        $(this).tab('show');
    });

    // SLIDERS INIT
    slidersInit();

    // CALLS THE UPDATE LAST
    updateSchedules(false);
} );

// =================================================================
// MARK: UPDATE FUNCTIONS (FUNCTIONS THAT UPDATE THE UI IN SOME WAY)
// =================================================================

function updateSchedules(is_async) {
    if (typeof(is_async)==='undefined') is_async = true;
    let wishList = JSON.parse(localStorage.getItem("wishList")) || {};
    let filters = $('#wishListFilters').serializeArray().reduce(function(obj, item) {
        obj[item.name] = item.value;
        return obj;
    }, {});

    filters["daysOff"] = String($("#daysOff").multipleSelect("getSelects"));
    filters["attr"] = String($("#attributes").multipleSelect("getSelects"));


    // Ajax gets the schedules data in the background (or not in the background if async is false)
    $.ajax({
        url: get_schedules_url,
        method: 'POST',
        data: {
            "wishList": wishList,
            "filters": filters,
            "csrfmiddlewaretoken": csrf_token
            },
        dataType: 'json',
        async: is_async,
        success: function (data) {
            creditCounts = [];
            coursesInfo = data["coursesInfo"];
            let raw_schedules = data["schedules"];
            if (raw_schedules.length > 0){
                schedules = [];

                // parses the schedules dictionary into a FullCalendar-readable format
                for (let i in raw_schedules){
                    creditCounts.push(raw_schedules[i]["total_credits"]);
                    let schedule = [];
                    let sections = raw_schedules[i]["sections"];
                    for (let j in sections){
                        let section = sections[j];

                        let subject = section["subject"];
                        let courseId = section["course_id"];
                        let sectionNum = section["section_num"];
                        let title = section["title"];
                        let numCredits = section["num_credits"];
                        for(let t in section["times"]){
                            let time = section["times"][t];
                            let day = time["day"];
                            let startHour = time["start_hour"];
                            let startMinute = time["start_minute"];
                            let endHour = time["end_hour"];
                            let endMinute = time["end_minute"];
                            schedule.push({
                                "title": "[" + numCredits + "] " + subject + " " + courseId + " " + sectionNum + " - " + title,
                                "start": "2018-01-0" + day + 'T' + startHour + ":" + startMinute,
                                "end": "2018-01-0" + day + 'T' + endHour + ":" + endMinute,
                                "color": coursesInfo[subject+courseId]["color"]
                            });
                        }
                    }
                    schedules.push(schedule);
                }
                numSchedules = schedules.length;
            } else {
                schedules = [[{}]];
                numSchedules = 0
            }

            scheduleIndex = 0;
            updateCalendar();
            updateWishListVisuals();
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("Status: " + textStatus); alert("Error: " + errorThrown);
        }
    });
}

function updateWishListVisuals(){
    let wishList = JSON.parse(localStorage.getItem("wishList")) || {};

    let wishListButtons = document.getElementById("wishListButtonsHolder");
    wishListButtons.innerHTML = "";

    if (Object.keys(wishList).length === 0){
        let noButtons = document.createElement("p");
        noButtons.innerHTML = "Go to the search classes tab to add classes.";
        wishListButtons.appendChild(noButtons);
    }



    // Creates the wish list buttons
    Object.keys(wishList).forEach(function(key) {

        let subject = wishList[key]["subject"];
        let course_id = wishList[key]["course_id"];
        let title = wishList[key]["title"];
        let required = !wishList[key]["optional"];

        let button = document.createElement("button");
        button.innerHTML = subject + " " + course_id;

        if (required) {
            button.innerHTML += "<sup>*</sup>";
        }

        if (coursesInfo[subject+course_id]["color"]) {
            button.style.background = coursesInfo[subject+course_id]["color"];
            button.style.color = "white";
        }
        button.style.borderRadius = "7px";
        button.style.height = "50px";
        button.style.width = "100px";

        button.addEventListener("click", function () {
            document.getElementById("courseInfo").style.display = "inline";

            let courseTitle = document.getElementById("courseTitle");
            courseTitle.innerHTML = subject + " " + course_id + " - " + title;

            let requiredBox = document.getElementById("required");

            requiredBox.checked = required;
            requiredBox.onclick = function() {
                setCourseOptional(subject, course_id, !requiredBox.checked);
                updateWishListVisuals();
                updateSchedules();
            };

            let description = document.getElementById("courseDescription");
            description.innerHTML = coursesInfo[subject+course_id]["description"];

            let addDropButton = document.getElementById("addDropButton");
            let newAddDrop = addDropButton.cloneNode(true);
            addDropButton.parentNode.replaceChild(newAddDrop, addDropButton);
            newAddDrop.addEventListener("click", function () {
                removeFromWishList(subject, course_id);
            })

        });
        wishListButtons.appendChild(button);
    });
}

function updateCalendar() {
    let calendar = $('#calendar');
    calendar.fullCalendar('removeEvents');
    calendar.fullCalendar('addEventSource', schedules[scheduleIndex]);
    calendar.fullCalendar('rerenderEvents');
    if (numSchedules === 0){
        document.getElementById("scheduleDisplay").innerHTML = "0/0";
    } else {
        document.getElementById("scheduleDisplay").innerHTML = (scheduleIndex+1).toString() + "/" + numSchedules.toString()
            + " (" + creditCounts[scheduleIndex] + " credits)";
    }

}

function filterCourses() {
    let subjectInput =$("#subjectInput").val();
    let inputString = subjectInput.toUpperCase();

    let table = document.getElementById("courses");
    let tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (let i = 0; i < tr.length; i++) {
        let td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            let found = td.innerHTML.toUpperCase();
            if (found.indexOf(inputString) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}
// =======================================================================
// MARK: USER INTERACTIONS (FUNCTIONS THAT RUN WHEN A USER CLICKS A BUTTON
// =======================================================================

function addToWishList(subject, course_id, title) {
    let newWishListEntry = {"subject": subject, "course_id": course_id, "title": title, "optional": true};
    let wishList = JSON.parse(localStorage.getItem("wishList")) || {};

    if (!(subject+course_id in wishList)) {
        wishList[subject + course_id] = newWishListEntry;
        localStorage.setItem("wishList", JSON.stringify(wishList));

        $.notify(
            "Added " + subject + " " + course_id + " to wish list.", "success",
            {position: "top"}
        );
        updateSchedules();
    } else {
        $.notify(
            "You've already added " + subject + " " + course_id + " to your wish list.",
            {position: "top right"}
        );
    }
}

function removeFromWishList(subject, course_id) {
    let wishList = JSON.parse(localStorage.getItem("wishList")) || {};
    delete wishList[subject+course_id];
    localStorage.setItem("wishList", JSON.stringify(wishList));

    $.notify(
        "Removed " + subject + " " + course_id + " from wish list.", "success",
        { position:"top" }
    );

    updateSchedules();
}

function scheduleLeft() {
    scheduleIndex -= 1;
    if (scheduleIndex < 0){
        if (numSchedules === 0){
            scheduleIndex = 0;
        } else {
            scheduleIndex = numSchedules-1;
        }
    }
    updateCalendar();
}

function scheduleRight() {
    scheduleIndex += 1;
    if (scheduleIndex >= numSchedules){
        scheduleIndex = 0;
    }
    updateCalendar();
}

function setCourseOptional(subject, course_id, value) {
    let wishList = JSON.parse(localStorage.getItem("wishList")) || {};

    wishList[subject+course_id]["optional"] = value;

    localStorage.setItem("wishList", JSON.stringify(wishList));
}
