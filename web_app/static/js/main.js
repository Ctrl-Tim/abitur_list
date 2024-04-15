(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner(0);


    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 45) {
            $('.navbar').addClass('sticky-top shadow-sm');
        } else {
            $('.navbar').removeClass('sticky-top shadow-sm');
        }
    });


    // Hero Header carousel
    $(".header-carousel").owlCarousel({
        animateOut: 'slideOutDown',
        items: 1,
        autoplay: true,
        smartSpeed: 1000,
        dots: false,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
    });


    // International carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        items: 1,
        smartSpeed: 1500,
        dots: true,
        loop: true,
        margin: 25,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ]
    });

    // testimonial carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        center: true,
        dots: true,
        loop: true,
        margin: 25,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsiveClass: true,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:1
            },
            768:{
                items:1
            },
            992:{
                items:1
            },
            1200:{
                items:1
            }
        }
    });



   // Back to top button
   $(window).scroll(function () {
    if ($(this).scrollTop() > 300) {
        $('.back-to-top').fadeIn('slow');
    } else {
        $('.back-to-top').fadeOut('slow');
    }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


})(jQuery);

function copyString(e) {
    navigator.clipboard.writeText(e.target.text);
    var delay = alertify.get('notifier','delay');
    alertify.set('notifier','delay', 1);
    alertify.success('Скопировано в буфер обмена!');
    alertify.set('notifier','delay', delay);
}

$(document).ready(function() {
    $('#table_results').DataTable({
        pagingType: 'simple_numbers',

        dom: "<'row'<'col-sm-4'l><'col-sm-4 text-center'B><'col-sm-4'f>>" +
              "<'row'<'col-sm-12'tr>>" +
              "<'row'<'col-sm-5'i><'col-sm-7'p>>",

        "ordering": true,

        columnDefs: [{
          orderable: false,
          targets: "no-sort"
        }],

        language: {
            "lengthMenu":       "Отобразить _MENU_ записей на одной странице",
            "zeroRecords":      "Ничего не найдено :(",
            "info":             "Страница _PAGE_ из _PAGES_",
            "infoEmpty":        "Не нашлось ни одного абитуриента",
            "infoFiltered":     "(Отфильтровано _MAX_ записей)",
            "loadingRecords":   "Загрузка...",
            "search":           "Поиск:",
            "paginate": {
                            "first":      "Начало",
                            "last":       "Конец",
                            "next":       ">",
                            "previous":   "<"
                        },
            },

        buttons: [
            {
                extend: 'excel',
                className: 'btn btn-dark rounded-0',
                text: '<i class="far fa-file-excel"></i> Excel',
                exportOptions: {
                    columns: ':not(:last-child)'
                },
            },
            {
                extend: 'pdf',
                className: 'btn btn-dark rounded-0',
                text: '<i class="far fa-file-pdf"></i> Pdf',
                exportOptions: {
                    columns: ':not(:last-child)'
                },
            },
            {
                extend: 'csv',
                className: 'btn btn-dark rounded-0',
                text: '<i class="fas fa-file-csv"></i> CSV',
                exportOptions: {
                    columns: ':not(:last-child)'
                },
            },
            {
                extend: 'print',
                className: 'btn btn-dark rounded-0',
                text: '<i class="fas fa-print"></i> Печать',
                exportOptions: {
                    columns: ':not(:last-child)'
                },
            }
        ],
    });
});

