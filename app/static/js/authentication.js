$(document).ready(function() {
    $('#loginForm').submit(function(e) {
        e.preventDefault();
        $("#email_error").html("")
        $("#password_error").html("")
        $(".loader").css('display', 'block');
        var email = $("#loginEmail").val();
        var password = $("#loginPassword").val();
        if(validation(email, password)){
            $.ajax({
                url: '/authentication',
                contentType: 'application/json', // Set content type explicitly
                dataType: 'json', // Specify data type expected from the server
                type: 'POST',
                data: JSON.stringify({ 'email': email, password : password }),
                success: function(response) {
                    $(".loader").css('display', 'none');
                    if(response.status == "success"){
                        window.location.replace(response.url);
                    }else{
                        $("#password_error").html(response.message) 
                    }
                   
                },
                error: function(xhr, status, error) {
                    $(".loader").css('display', 'none');
                    console.error(error);
                }
            });
        }else{
            $(".loader").css('display', 'none');
        }
    });


    function validation(email, password){
        var error = true
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            $("#email_error").html("Invalid Email")
            error = false
        }
        if(password.length == 0){
            $("#password_error").html("Password is Mandatory")
            error = false
        }
        return error;
    }


    $("#get_result_class").click(function(e){
        $("#error_text").css('display', 'none');
        $(".loader").css('display', 'block');
        // var question = $("#questions").val();
        var file_name = $("#file_name").val();
        //if(question.length != 0){
        $.ajax({
            url: '/get_file',
            contentType: 'application/json', // Set content type explicitly
            dataType: 'json', // Specify data type expected from the server
            type: 'POST',
            data: JSON.stringify({ 'question': 'develper', "file_name" : file_name }),
            success: function(response) {
                $(".loader").css('display', 'none');
                $("#response").css('display', 'block');
                $('#response').text(response.message);
                $("#get_result_class").css('display', 'none');
                $('#filedownload').attr('href', response.url);
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
        // }else{
        //     $("#error_text").css('display', 'block');
        // }
     
    });
});
