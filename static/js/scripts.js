$(function() {

    $('.pagination').addClass('flex space-x-4');
    
    $('#department_tbl tbody #edit_department').on('click',function() {

        var data = [];

        $(this).closest('tr').find('td').each(function() {
            data.push($(this).text());
        });

        $('#form_department').attr('action', '/department/'+ data[0] +'/update/')
        $('#id_name').val(data[1]).focus();
        $('#id_description').val(data[2]);
        $('#btn_department').text('Update');

        $('#toggle_view_department_btn').show().attr('href', data[0] + '/read');
        $('#toggle_clear_department_btn').show();
        $('#view_department_btn').attr('href', data[0] + '/read');

        var maxlength = $('#id_description').attr("maxlength");
        var currentLength = $('#id_description').val().length;
        $('#char_count').text(maxlength - currentLength + " characters left");
    });

    $('#employee_tbl tbody #edit_employee').on('click',function() {
        var data = [];

        $(this).closest('tr').find('td').each(function() {
            data.push($(this).text());
        });

        $('#form_employee').attr('action', '/employee/'+ data[0] +'/update/')
        $('#id_name').val(data[1]).focus();
        $('#id_department').find("option:contains("+data[2]+")").attr('selected', true);
        $('#btn_employee').text('Update');

        $('#toggle_view_employee_btn').show().attr('href', data[0] + '/read');
        $('#toggle_clear_employee_btn').show();
        $('#view_employee_btn').attr('href', data[0] + '/read');
    });

    $('#id_description').on("input propertychange", function(){
        var maxlength = $(this).attr("maxlength");
        var currentLength = $(this).val().length;
    
        if( currentLength >= maxlength ){
            $('#char_count').text("You have reached the maximum number of characters.");
        } else {
            $('#char_count').text(maxlength - currentLength + " characters left");
        }
    });
});
