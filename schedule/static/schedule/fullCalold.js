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
            events:[
                {
                    title: "Elements of Software Construction",
                    start: "2019-02-25 10:00", //YYYY-MM-DD
                    end: "2019-02-25 11:30",
                    description: "Prof",
                    location: "LT"
                },
                {
                    title: "Probs and Stats",
                    start: "2019-04-01 08:00",
                    end: "2019-04-01 09:40",
                    description: "Prof",
                    location: "CC13"
                }
            ],
            color: 'yellow',
            textColor: 'black',

            eventRender: function(objEvent, element, view) {
                if (view.name === "agendaWeek" || view.name === "agendaDay"){
                 element.find(".fc-content").append(objEvent.location + "</br>" + objEvent.description);
                 //element.find(".fc-title").empty().append('<div class="fc-title"><b>Probs and Stats<b></div>')
                }},

            eventAfterAllRender: function (view, element) {
                //The title isn't rendered until after this callback, so we need to use a timeout.
                if(view.type === "agendaWeek"){
                    // tried to use flex to align, didn't work out well
                    window.setTimeout(function(){
                        $("#calendar").find('#calendar-additions').remove();
                        $("#calendar").find('.fc-toolbar').append(
                            "<div id='calendar-additions'>"+
                            "<li><select class='selectpicker' multiple data-actions-box='true' title='Filter'>"+
                            "<option>Course 1</option>"+
                            "<option>Course 2</option>"+
                            "</select></li>"+
                            "<li><button class='button-submit'>&#x21B5;"+
                            // '<svg viewBox="0 0 124.73 153.14"><g><g><path d="M124.73,115.17H42.05c10.59,11.91,18.19,24.56,22.78,37.97H54.7C41.58,134.02,23.34,120.19,0,111.66v-6.89c23.34-8.53,41.58-22.36,54.7-41.48h10.12c-4.59,13.5-12.19,26.2-22.78,38.11h68.77V0h13.92V115.17z"/></g></g></svg>'+
                            "</button></li>"+
                            "<li><button id='export-button'>"+
                            '<i class="far fa-share-square"></i>'+
                            "<p id='export_text'>Export</p>"+
                            "</button></li>"+
                            "<div id='blank_row'></div>"+
                            "</div>"
                        );
                        $('.selectpicker').selectpicker();
                    },0);
                }
            },
        });
    });


