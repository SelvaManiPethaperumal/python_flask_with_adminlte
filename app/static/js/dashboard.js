
$(document).ready(function() {
   
   listData = []
   empIDData = []
   pagenumsstart = 0
   currentpage = 0
   lastPage=0
   getData(1)
   $("#selectData").click(function(e){
    getData(1)
   })

   $('#search').keydown(function (e) {
    if (e.keyCode == 13) {
       getData(1)
    }
})
//Logout the function
$("#Logout").click(function(e){
$.ajax({
    url: '/out',
    contentType: 'application/json', // Set content type explicitly
    dataType: 'json', // Specify data type expected from the server
    type: 'POST',
    data: JSON.stringify({ 'page': 1}),
    success: function(response) {
        window.location.replace(response.url);
    }
});
});
});

//Set page Number and call getData api
function setPage(page){
    getData(page)
}

//Search and call getData api
function searchdata(){
    getData(1)
}

//Get the data fro dashbaord
function getData(page){
    $('#cover-spin').show();
    empid = $('#selectData').val();
    if(empid == null){
        empid = "all"
    }
    search = $("#search").val()
    $.ajax({
        url: '/get_data',
        contentType: 'application/json', // Set content type explicitly
        dataType: 'json', // Specify data type expected from the server
        type: 'POST',
        data: JSON.stringify({ 'page': page, 'empid' : empid, 'search' : search}),
        success: function(response) {
            $(".loader").css('display', 'none');
            if(response.status == "success"){
                $("#downloadLink").attr('href', response.base_url+ 'download')
                if(response.employee_details.length != 0 && $('#selectData').val() == null ){
                    var selectcontent = '<option value=all > All </option>'
                    $.each(response.employee_details, function(selectIndex, selectValue){
                        selectcontent = selectcontent + '<option value='+selectValue+'>'+selectValue+'</option>'
                    })
                    $("#selectData").html(selectcontent)
                }
                
                
                $.each(response.count_details, function(index, value) {
                    $("#id_"+index).html(value)                        
                })

                $.each(response.data, function(index, value){

                    
                    if(index == 'items'){
                        var tableText = ''
                        $.each(value, function(tableIndex, tableValue){
                            id = tableIndex + 1
                            tableText = tableText+'<tr class="align-middle"> <td>'+id+'</td><td>'+tableValue['question']+'</td> <td>'+tableValue['response']+'</td><td>'+tableValue['empid']+'</td><td>'+tableValue['raw_question']+'</td><td>'+tableValue['date']+'</td><td>'+tableValue['isliked']+'</td></tr>'
                        })
                        $("#tableHtml").html(tableText)
                        if(value.length == 0){
                            $("#tableHtml").html('<tr class="align-middle"><td></td><td></td><td></td><td>No Record found</td></tr>')
                        }
                    }

                    if(index == 'pages'){
                        lastPage=value
                    }
                    if(index == 'current_page'){
                        currentpage=value
                    }

                })

                var pageContent =''
                pageContent = pageContent+ '<li class="page-item"> <a class="page-link" href="#" onclick="setPage(1)">&laquo;</a> </li>'
                for (var i = 1; i <= lastPage; i++) {
                    style = ''
                    if(currentpage == i){
                        style = 'style="background-color: #dbe0e8;"'
                    }
                    pageContent = pageContent+ '<li class="page-item"> <a class="page-link" href="#" onclick="setPage('+i+')"   '+style+' >'+i+'</a> </li>'
                   
                }
                pageContent = pageContent+ '<li class="page-item"> <a class="page-link" href="#" onclick="setPage('+lastPage+')">&raquo;</a> </li>'
                
                $("#pageContent").html(pageContent)
            }else{
                $("#tableHtml").html(response.message)
            }

            
            $('#cover-spin').hide(); 
        },
        error: function(xhr, status, error) {
            $('#cover-spin').hide();
            $(".loader").css('display', 'none');
            console.error(error);
        }
    });
}
