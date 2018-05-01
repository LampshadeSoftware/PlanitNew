let coursesDataTable;
function tablesInit(){
    // "dom": "<'row'<'col-sm-6'f>>" + "t"
    coursesDataTable = $('#courses').DataTable({searching: true, dom: 'lrtp', "lengthChange": false});
    //$('.dataTables_filter').addClass('pull-left');
    $('#subjectInput').on( 'keyup', function () {
        filterCourseTable(this, 0);
    });
    $('#coursenumInput').on( 'keyup', function () {
        filterCourseTable(this, 1);
    });
    $('#titleInput').on( 'keyup', function () {
        filterCourseTable(this, 2);
    });

    // Add event listener for opening and closing details
    $('#courses tbody').on('click', function () {
        let tr = $(this).closest('tr');
        let row = coursesDataTable.row( tr );

        // alert(row);
    } );
}

function filterCourseTable(element, column) {
    coursesDataTable
        .columns( column )
        .search( element.value )
        .draw();
}

function filtersInit(){
    // DAYS OFF FILTER
    $('#daysOff').multipleSelect({
        onClick: function(view) {
            updateSchedules();
        },
        onCheckAll: function() {
            updateSchedules();
        },
        onUncheckAll: function() {
            updateSchedules();
        }
    });
    // ATTRIBUTES FLTER
    $('#attributes').multipleSelect({
        filter: true,
        onClick: function(view) {
            updateSchedules();
        },
        onCheckAll: function() {
            updateSchedules();
        },
        onUncheckAll: function() {
            updateSchedules();
        }
    });
}

function calendarInit(){
    $('#calendar').fullCalendar({
        defaultDate: moment('2018-01-01'),
        weekends: false,
        defaultView: 'agendaWeek',
        columnHeaderFormat: 'dddd',
        minTime: "08:00:00",
        maxTime: "23:59:00",
        height: "auto",
        eventColor: '#29B89B',
        header:false,

        contentHeight: 600,
        allDaySlot: false,

        events: [{}]
    });
}

function slidersInit() {
    let timeSlider = document.getElementById('timeSlider');
    noUiSlider.create(timeSlider, {
        connect: true,
        behaviour: 'tap',
        start: [480, 1020],
        step: 30,
        range: {
            'min': 480,
            'max': 1320
        }
    });

    let startTime = document.getElementById('startTime');
    let endTime = document.getElementById('endTime');

    startTime.addEventListener('change', function(){
        timeSlider.noUiSlider.set([this.value, null]);
    });

    endTime.addEventListener('change', function(){
        timeSlider.noUiSlider.set([null, this.value]);
    });

    timeSlider.noUiSlider.on('update', function( values, handle ) {

        let value = values[handle];

        if ( handle ) { // right handle
            endTime.value = Math.round(value);
        } else {  // left handle
            startTime.value = Math.round(value);
        }
        //updateSchedules();
    });
    timeSlider.noUiSlider.on('change', function() {
        updateSchedules();
    });


    // MIN/MAX CREDITS INIT
    let creditSlider = document.getElementById('creditSlider');
    noUiSlider.create(creditSlider, {
        connect: true,
        behavior: 'tap',
        start: [12, 18],
        step: 1,
        range: {
            'min': 1,
            'max': 20
        }
    });

    let minCredits = document.getElementById('minCredits');
    let maxCredits = document.getElementById('maxCredits');

    minCredits.addEventListener('change', function() {
        creditSlider.noUiSlider.set([this.value, null]);
    });
    maxCredits.addEventListener('change', function() {
        creditSlider.noUiSlider.set([null, this.value]);
    });

    creditSlider.noUiSlider.on('update', function (values, handle ) {
        let value = values[handle];

        if ( handle ) {
            maxCredits.value = Math.round(value);
        } else {
            minCredits.value = Math.round(value);
        }
        //updateSchedules();
    });
    creditSlider.noUiSlider.on('change', function() {
        updateSchedules();
    });
}
