$(document).ready(function () {
    $("[data-toggle=offcanvas]").click(function () {
        $(".row-offcanvas").toggleClass("active");
    });

    $(".custom-select").each(function () {
        var classes = $(this).attr("class"),
            id = $(this).attr("id"),
            name = $(this).attr("name");
        var template = '<div class="' + classes + '">';
        template +=
            '<span class="custom-select-trigger">' +
            $(this).attr("placeholder") +
            "</span>";
        template += '<div class="custom-options">';
        $(this)
            .find("option")
            .each(function () {
                template +=
                    '<span class="custom-option ' +
                    $(this).attr("class") +
                    '" data-value="' +
                    $(this).attr("value") +
                    '">' +
                    $(this).html() +
                    "</span>";
            });
        template += "</div></div>";

        $(this).wrap('<div class="custom-select-wrapper"></div>');
        $(this).hide();
        $(this).after(template);
    });
    $(".custom-option:first-of-type").hover(
        function () {
            $(this)
                .parents(".custom-options")
                .addClass("option-hover");
        },
        function () {
            $(this)
                .parents(".custom-options")
                .removeClass("option-hover");
        }
    );
    $(".custom-select-trigger").on("click", function () {
        $("html").one("click", function () {
            $(".custom-select").removeClass("opened");
        });
        $(this)
            .parents(".custom-select")
            .toggleClass("opened");
        event.stopPropagation();
    });
    $(".custom-option").on("click", function () {
        $(this)
            .parents(".custom-select-wrapper")
            .find("select")
            .val($(this).data("value"));
        $(this)
            .parents(".custom-options")
            .find(".custom-option")
            .removeClass("selection");
        $(this).addClass("selection");
        $(this)
            .parents(".custom-select")
            .removeClass("opened");
        $(this)
            .parents(".custom-select")
            .find(".custom-select-trigger")
            .text($(this).text());
    });


     $('.checkbox-action').click(function (e) {
//         e.preventDefault()
         if ($(this).children('input[name="checkbox"]').is(":not(:checked)")) {
             $('.content , .admin-right-banner').css('display', 'none');
             $('.new_content, .new_button, .checkbox-active , .analyze-tab').css('display', 'block');
         }
     });

    $('.select-file').click(function (e) {
        e.preventDefault()
        if ($(this).children('input[name="checkbox"]').is(":not(:checked)")) {
            $('.content , .admin-right-banner').css('display', 'none');
            $('.new_content, .new_button, .checkbox-active , .analyze-tab').css('display', 'block');
        }
    });

    (function () {
        'use strict';
        $('.input-file').each(function () {
            var $input = $(this),
                $label = $input.next('.js-labelFile'),
                labelVal = $label.html();

            $input.on('change', function (element) {
                var fileName = '';
                if (element.target.value) fileName = element.target.value.split('\\').pop();
                fileName ? $label.addClass('has-file').find('.js-fileName').html(fileName) : $label.removeClass('has-file').html(labelVal);
            });
        });

    })();

});

$(document).ready(function () {
    $(".forgot-psw").click(function () {
        $("#login").css("display", "none");
    });
    $(".sign-up-details").click(function () {
        $("#login").css("display", "none");
    });
    $(".reset-psw-btn").click(function () {
        $("#forgot-psw").css("display", "none");
    });
    $(".signup-btn").click(function () {
        $("#reset-psw").css("display", "none");
    });
    $(".login-btn").click(function () {
        $("#login").css("display", "block");

    });
    $('.select-file ').on('click', function () {
        $('.upload-files , .analyze-dropdown-right').css('display', 'none');
        $('.map-banner , .documents').css('display', 'block');
    });

    $('.back').on('click', function () {
        $('.map-banner , .new_button').css('display', 'none');
        $('.new_content').css('display', 'block');
    });

    $('.analyze-list ').on('click', function () {
        $('.content , .admin-right-banner').css('display', 'none');
        $('.new_content , .analyze-tab , .new_button , .analyze-dropdown-right , .checkbox-active').css('display', 'block');
    });

    $('.geo-tag').on('click', function () {
        $('.new_content , .new_button').css('display', 'none');
        $('.upload-files').css('display', 'block');
    });
    $('.select-file').on('click', function () {
        $('.analyze-dropdown-right').css('display', 'none');
        $('.documents').css('display', 'block');
    });

});

$(document).ready(function(){
    $(".fav-icon").click(function(){
        // Change src attribute of image
        $(this).attr("src", "/static/images/fill-favorite.png");
    });
});
