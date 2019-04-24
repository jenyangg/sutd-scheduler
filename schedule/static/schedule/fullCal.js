$(document).ready(function(){


        // $('.selectpicker').selectpicker();
        $('#calendar').fullCalendar({
            //hiddenDays:[0,6], same as below


            weekends: false,
            header : {
                left: "month,agendaWeek,agendaDay", //space leaves a gap between buttons
                center: "title",
                right:"today, prev,next"
            },
            aspectRatio:1.5,
            defaultView: 'agendaWeek',
            // themeSystem: 'bootstrap4',
            allDaySlot: false,
            height: 'auto',
            timezone: 'Asia/Singapore',
            /* Min and Max time on calendar */
            minTime: "08:00:00",
            maxTime: "20:00:00",
            // events:[
            //     {
            //         title: "Elements of Software Construction",
            //         start: "2019-02-25 10:00", //YYYY-MM-DD
            //         end: "2019-02-25 11:30",
            //         assigned_professors: "Prof",
            //         location: "LT"
            //     },
            //     {
            //         title: "Probs and Stats",
            //         start: "2019-04-01 08:00",
            //         end: "2019-04-01 09:40",
            //         assigned_professors: "Prof",
            //         location: "CC13"
            //     }
            // ],
            // color: 'yellow',
            // textColor: 'black',
            eventSources:[
                {
                url: '/return_data', // use the `url` property
                }
            ],
            eventRender: function(objEvent, element, view) {
                if (view.name === "agendaWeek" || view.name === "agendaDay"){
                 element.find(".fc-content").append(objEvent.location + "</br>" + objEvent.assigned_professors);
                 //element.find(".fc-title").empty().append('<div class="fc-title"><b>Probs and Stats<b></div>')
                }},
        });

    });


