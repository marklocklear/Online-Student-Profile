function refreshVisits(page) {
    $.get(base_url + 'visit/' + student_id + '/all/' + page + '/',
          function(data) {
        $('#visits').fadeOut('fast', function() {
            $(this).html(data);
            $(this).fadeIn('fast');
        });
    });
}

$(function() {
    $('#visit-paging a').live('click', function() {
        refreshVisits($(this).data('page'));
    });

    $('#view-visit-window').dialog(default_window_options);
    $('#log-visit-window').dialog(default_window_options);
    $('#log-visit-window').dialog('option', 'buttons', [
        {
            text: 'Submit',
            click: function() {
                var data = $('#visit-form').serializeArray();
                $.post(base_url + 'visit/' + student_id + '/log/',
                       data,
                       function(data) {
                    if(data.status == 'success') {
                        refreshVisits(1);
                        $('#log-visit-window').dialog('close');
                    } else if(data.status == 'fail') {
                        $('#log-visit-window').html(data.template);
                        applyNotificationStyles();
                    }
                }, 'json');
            }
        }
    ]);

    $('#log-visit').click(function() {
        $.get(base_url + 'visit/' + student_id + '/log/', function(data) {
            $('#log-visit-window').html(data);
            $('#log-visit-window').dialog('open');
        });
    });

    $('.view-visit').live('click', function() {
        $.get(base_url + 'visit/' + student_id + '/view/' +
              $(this).data('visit') + '/',
              function(data) {
            $('#view-visit-window').html(data);
            applyNotificationStyles();
            $('#view-visit-window').dialog('open');
        });
    });

    $('a.modal').each(function() {
      if($(this).attr('ref') == 'learning-style-window') {
        $('#learning-style-window').dialog(default_window_options).load(base_url + 'assessment/learning-style/results/' + latest_learning_style_result.id + '/');
      } else if($(this).attr('ref') == 'personality-type-window') {
        $('#personality-type-window').dialog(default_window_options).load(base_url + 'assessment/personality-type/results/' + latest_personality_type_result_id + '/');
      } else if($(this).attr('ref') == 'survey-window') {
        $('#survey-window').dialog(default_window_options).load(base_url + 'survey/results/' + $(this).data('result-id') + '/');
      }
    });

    $('a.modal').click(function() {
        $('#' + $(this).attr('ref')).dialog('open');
    });
});

if (latest_personality_type_result_id !== '' || latest_learning_style_result.id !== '') {
    google.load('visualization', '1', {packages: ['corechart']});
    google.setOnLoadCallback(drawCharts);
}

function drawCharts() {
    if (latest_personality_type_result_id !== '') {
        // Extraverted/Introverted Chart
        var personality_type_data_1 = new google.visualization.DataTable();

        personality_type_data_1.addColumn('string', 'Category');
        personality_type_data_1.addColumn('number', 'Score');

        personality_type_data_1.addRows(2);
        personality_type_data_1.setValue(0, 0, 'Extraverted');
        personality_type_data_1.setValue(1, 0, 'Introverted');

        if (personality_type_scores[0][0] == 'E') {
            personality_type_data_1.setValue(0, 1, personality_type_scores[0][1]);
            personality_type_data_1.setValue(1, 1, personality_type_scores[0][2]);
        } else {
            personality_type_data_1.setValue(0, 1, personality_type_scores[0][2]);
            personality_type_data_1.setValue(1, 1, personality_type_scores[0][1]);
        }

        var personality_type_chart_1 = new google.visualization.PieChart(document.getElementById('personality-type-chart-1'));
        personality_type_chart_1.draw(personality_type_data_1, {width: 175, height: 175, legend: 'bottom', backgroundColor: '#ededee'});

        // Sensing/Intuitive Chart
        var personality_type_data_2 = new google.visualization.DataTable();

        personality_type_data_2.addColumn('string', 'Category');
        personality_type_data_2.addColumn('number', 'Score');

        personality_type_data_2.addRows(2);
        personality_type_data_2.setValue(0, 0, 'Sensing');
        personality_type_data_2.setValue(1, 0, 'Intuitive');

        if (personality_type_scores[1][0] == 'S') {
            personality_type_data_2.setValue(0, 1, personality_type_scores[1][1]);
            personality_type_data_2.setValue(1, 1, personality_type_scores[1][2]);
        } else {
            personality_type_data_2.setValue(0, 1, personality_type_scores[1][2]);
            personality_type_data_2.setValue(1, 1, personality_type_scores[1][1]);
        }

        var personality_type_chart_2 = new google.visualization.PieChart(document.getElementById('personality-type-chart-2'));
        personality_type_chart_2.draw(personality_type_data_2, {width: 175, height: 175, legend: 'bottom', backgroundColor: '#ededee'});

        // Thinking/Feeling Chart
        var personality_type_data_3 = new google.visualization.DataTable();

        personality_type_data_3.addColumn('string', 'Category');
        personality_type_data_3.addColumn('number', 'Score');

        personality_type_data_3.addRows(2);
        personality_type_data_3.setValue(0, 0, 'Thinking');
        personality_type_data_3.setValue(1, 0, 'Feeling');

        if (personality_type_scores[2][0] == 'T') {
            personality_type_data_3.setValue(0, 1, personality_type_scores[2][1]);
            personality_type_data_3.setValue(1, 1, personality_type_scores[2][2]);
        } else {
            personality_type_data_3.setValue(0, 1, personality_type_scores[2][2]);
            personality_type_data_3.setValue(1, 1, personality_type_scores[2][1]);
        }

        var personality_type_chart_3 = new google.visualization.PieChart(document.getElementById('personality-type-chart-3'));
        personality_type_chart_3.draw(personality_type_data_3, {width: 175, height: 175, legend: 'bottom', backgroundColor: '#ededee'});

        // Judging/Perceiving Chart
        var personality_type_data_4 = new google.visualization.DataTable();

        personality_type_data_4.addColumn('string', 'Category');
        personality_type_data_4.addColumn('number', 'Score');

        personality_type_data_4.addRows(2);
        personality_type_data_4.setValue(0, 0, 'Judging');
        personality_type_data_4.setValue(1, 0, 'Perceiving');

        if (personality_type_scores[3][0] == 'J') {
            personality_type_data_4.setValue(0, 1, personality_type_scores[3][1]);
            personality_type_data_4.setValue(1, 1, personality_type_scores[3][2]);
        } else {
            personality_type_data_4.setValue(0, 1, personality_type_scores[3][2]);
            personality_type_data_4.setValue(1, 1, personality_type_scores[3][1]);
        }

        var personality_type_chart_4 = new google.visualization.PieChart(document.getElementById('personality-type-chart-4'));
        personality_type_chart_4.draw(personality_type_data_4, {width: 175, height: 175, legend: 'bottom', backgroundColor: '#ededee'});
    }

    if (latest_learning_style_result.id !== '') {
        // Learning Styles Chart
        var learning_style_data = new google.visualization.DataTable();

        // Data table columns
        learning_style_data.addColumn('string', 'Style');
        learning_style_data.addColumn('number', 'Score');

        // Data table rows
        learning_style_data.addRows(3);
        learning_style_data.setValue(0, 0, 'Auditory');
        learning_style_data.setValue(1, 0, 'Kinesthetic');
        learning_style_data.setValue(2, 0, 'Visual');

        // Add learning style scores to data table
        learning_style_data.setValue(0, 1, latest_learning_style_result.auditory_score);
        learning_style_data.setValue(1, 1, latest_learning_style_result.kinesthetic_score);
        learning_style_data.setValue(2, 1, latest_learning_style_result.visual_score);

        // Draw bar chart for learning style
        var learning_style_chart = new google.visualization.BarChart(document.getElementById('learning-style-chart'));
        learning_style_chart.draw(learning_style_data, {width: 400, height: 200, legend: 'none', backgroundColor: '#ededee'});
    }
}
