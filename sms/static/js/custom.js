jQuery(document).ready(function ($) {

    /*------------------------------------------------
                DECLARATIONS
    ------------------------------------------------*/

    var loader = $('#loader');
    var loader_container = $('#preloader');
    var menu_toggle = $('#masthead .menu-toggle');
    var primary_menu = $('#masthead ul.nav-menu');

    /*------------------------------------------------
                PRELOADER
    ------------------------------------------------*/

    loader_container.delay(1000).fadeOut();
    loader.delay(1000).fadeOut("slow");

    /*------------------------------------------------
                NAVIGATION
    ------------------------------------------------*/

    menu_toggle.click(function () {
        primary_menu.slideToggle();
        $(this).toggleClass('active');
        $('#masthead .main-navigation').toggleClass('menu-open');
        $('.menu-overlay').toggleClass('active');

    });

    /*------------------------------------------------
                Login Popup
    ------------------------------------------------*/

    $('.login-page').click(function (event) {
        event.preventDefault();
        $('body').addClass('show-login');
        $('.menu-overlay').addClass('active');
    });

    $('.signup-link a').click(function (event) {
        event.preventDefault();
        $('body').addClass('show-signup');
        $('.menu-overlay').addClass('active');
    });

    $('.signin-link a').click(function (event) {
        event.preventDefault();
        $('body').addClass('show-login');
        $('body').removeClass('show-signup');
    });

    $('.menu-overlay').on('click', function () {
        $('body').removeClass('show-login show-signup');
        $('.menu-overlay').removeClass('active');
    });


    /*------------------------------------------------
                Tab Filter
    ------------------------------------------------*/

    $('ul.tabs li').click(function (event) {
        event.preventDefault();

        var tab_id = $(this).attr('data-tab');

        $('ul.tabs li').removeClass('active');
        $(this).addClass('active');

        $('.tab-content').hide();
        $("#" + tab_id).fadeIn('slow');
    });




    /*------------------------------------------------
                    Dashboard
    ------------------------------------------------*/

    $(".suspend-btn").click(function () {
        alert("Suspending subscription.");
        $(this).text("Suspended");
    });

    // Action for Notify College button
    $(".notify-btn").click(function () {
        alert("Sending notification to the college regarding expired subscription.");
        $(this).text("Notified");
        $(this).prop("disabled", true);
    });


    // Toggle Sidebar and Overlay on hamburger click
    $(".hamburger-menu").click(function () {
        $(".sidebar").toggleClass("active"); // Toggle sidebar visibility
        $(".overlay").toggle(); // Toggle overlay visibility
    });

    // Close sidebar when close button in sidebar is clicked
    $(".sidebar .close-sidebar-btn").click(function () {
        $(".sidebar").removeClass("active"); // Hide sidebar
        $(".overlay").hide(); // Hide overlay
    });

    // Close sidebar when overlay is clicked
    $(".overlay").click(function () {
        $(".sidebar").removeClass("active"); // Hide sidebar
        $(".overlay").hide(); // Hide overlay
    });

    $(".sidebar .tabs li").click(function () {
        if ($(window).width() < 992) {
            $(".sidebar").removeClass("active"); // Remove active class from sidebar on smaller screens
            $(".overlay").hide(); // Hide overlay
        }
    });


    $(".add-btn").click(function () {
        $("body").addClass("adding-college");
    });
    
    $(".edit-btn").click(function () {
        $("body").addClass("editing-college");
    });

    $(".close-modal-btn").click(function () {
        $("body").removeClass("adding-college");
        $("body").removeClass("editing-college");
    });


    /*------------------------------------------------
                    END JQUERY
    ------------------------------------------------*/

});