/*
Template Name: Osahan Land - Bootstrap 4 Light Real Estate Theme
Author: Askbootstrap
Author URI: https://themes.getbootstrap.com/
Version: 1.0
*/
/*
	-- Hover Nav
	-- Select2
*/
$(document).ready(function() {
    "use strict";

    // ===========Hover Nav============	
	$('.navbar-nav li.dropdown').hover(function() {
	  $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeIn(500);
	}, function() {
	  $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeOut(500);
	});
	
	// ===========Select2============	
	$(document).ready(function() {
      $('.select2').select2();
    });
	var imported = document.createElement('script');imported.src = 'https://www.googletagmanager.com/gtag/js?id=UA-120909275-1';document.head.appendChild(imported);window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}gtag('js', new Date());gtag('config', 'UA-120909275-1');
});