$(document).ready(
    function () {
        $('#question_form').on('submit', function (e) {
            e.preventDefault();
            verify_question($(this));
        });

        function verify_question(form) {
            var answer = $('input[name=answer]:checked').val();
            $.ajax({
                url: $(form).prop('action'),
                type: 'POST',
                data: $(form).serialize(),
                success: function (data) {
                    var $result_p = $('.answer_result');
                    $result_p.html(data['text']).fadeIn();

                    $('.result_area').show();
                    $('#submit').hide();
                    $(form).find('input[name=answer]').prop('disabled', 'disabled');
                    $('.result_area input[name=answer]').val(answer);
                    if (data.is_correct) {
                        $('.result_p').html('You are Correct :)');
                        $result_p.addClass('green').removeClass('error');
                    } else {
                        $('.result_p').html('Sorry :(');
                        $result_p.addClass('error').removeClass('green');
                    }
                    $('input[name=answer]').each(function () {
                        if (data.right_answer == $(this).val()) {
                            $(this).parent('li').addClass('highlight');
                        }
                    });

                },
                error: function () {
                    $('.next_question').hide();
                    $('.answer_result').fadeOut();
                }
            })
        }

        // This function gets cookie with a given name
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        var csrftoken = getCookie('csrftoken');

        /*
         The functions below will create a header with csrftoken
         */

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        function sameOrigin(url) {
            // test that a given url is a same-origin URL
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                    // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        $('#categories_form').on('submit', function (e) {
            if ($('input[name=categories]:checked').length < 3) {
                alert('Please select at least 3 categories!');
                e.preventDefault();
                return false;
            }
            $(".loader").show();
            return true;
        });


        $('#add_more').on('click', function() {
            var text_html = '<div><input type="text" name="keys" style="width: 40%; margin-left: 104px;"/></div>';
            $('#key_fields').append(text_html);
        })
    }
);

