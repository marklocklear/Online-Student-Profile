var default_window_options = {
    autoOpen: false,
    width: 750,
    height: 450,
    modal: true,
    resizable: false
}

function applyNotificationStyles() {
    $('.error').each(function() {
        $(this).addClass('ui-state-error ui-corner-all');
        $(this).prepend('<span class="ui-icon ui-icon-alert"></span>');
    });
    $('.notification').each(function() {
        $(this).addClass('ui-state-highlight ui-corner-all');
        $(this).prepend('<span class="ui-icon ui-icon-info"></span>');
    });
}

$(function() {
    // Hard-coded paths aren't great... Maybe re-work this in the future
    var divider = "url('" + media_url + "img/navigation_divider.png')";

    $('#navigation ul.menu li:has(ul.submenu)').hover(function() {
        $(this).addClass('has-submenu');
        $(this).children('a.menu-link').css('background-image', 'none');
        $(this).prev('li').children('a.menu-link').css('background-image', 'none');
        $(this).children('ul').show();
    }, function() {
        $(this).removeClass('has-submenu');
        $(this).children('a.menu-link').css('background-image', divider);
        $(this).prev('li').children('a.menu-link').css('background-image', divider);
        $(this).children('ul').hide();
    });
    
    $('#navigation ul.submenu a').click(function() {
        $(this).parents('ul.submenu').hide();
    });

    // Style form buttons
    $('input[type=button], input[type=submit], input[type=reset]').button();

    // Style error and notification messages
    applyNotificationStyles();
});
