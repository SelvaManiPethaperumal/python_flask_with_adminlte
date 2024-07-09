$(document).ready(function() {
    $('#uploadForm').submit(function(e) {
        e.preventDefault();
        
        var formData = new FormData();
        formData.append('file', $('#file')[0].files[0]);
        formData.append('is_company_po', $('#is_company_po').prop('checked'));
        $(".loader").css('display', 'block');
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                $(".loader").css('display', 'none');
                $('#response').text(response.message);
                $("#file_name").val(response.file_name)
                $("#get_result_class").css('display', 'block');
                $("#get_result").css('display', 'block');
            },
            error: function(xhr, status, error) {
                $(".loader").css('display', 'none');
                console.error(error);
            }
        });
    });


    $("#is_company_po").click(function(e){
        $("#error_text").css('display', 'none');
        $("#response").css('display', 'none');
        $("#get_result_class").css('display', 'none');
        $("#get_result").css('display', 'none');
    })

    $("#file").click(function(e){
        $("#error_text").css('display', 'none');
        $("#response").css('display', 'none');
        $("#get_result_class").css('display', 'none');
        $("#get_result").css('display', 'none');
    })


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
