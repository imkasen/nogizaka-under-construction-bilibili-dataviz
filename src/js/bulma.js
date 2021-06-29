"use strict";

$(document).ready(function () {
    // Check for click events on the navbar burger icon
    $(".navbar-burger").click(function () {

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");

    });

    // change nav bar color
    $(window).scroll(
        function () {
            if ($("#fix-navbar").offset().top > 500) {
                $("#fix-navbar").addClass("is-primary");
                $("#nav-title").removeClass("has-text-primary").addClass("has-text-light");
                $(".nav-text").removeClass("has-text-primary").addClass("has-text-light");
                $("#nav-button").addClass("is-inverted");
            } else {
                $("#fix-navbar").removeClass("is-primary");
                $("#nav-title").removeClass("has-text-light").addClass("has-text-primary");
                $(".nav-text").addClass("has-text-primary").removeClass("has-text-light");
                $("#nav-button").removeClass("is-inverted");
            }
        }
    );
});
