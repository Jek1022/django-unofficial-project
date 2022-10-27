$(function() {

    $('.pagination').addClass('flex space-x-4');
    
    $('#department_tbl tbody tr').on('click',function() {

        var data = [];

        $('#form_department').removeAttr('action')

        $(this).closest('tr').find('td').each(function() {
            data.push($(this).text());
        });

        $('#id_name').val(data[1]).focus();
        $('#id_description').val(data[2]);
        $('#form_department').attr('action', data[0])
        $('#btn_department').text('Update');
    });

    $('#employee_tbl tbody tr').on('click',function() {
        var data = [];

        $('#form_employee').removeAttr('action')

        $(this).closest('tr').find('td').each(function() {
            data.push($(this).text());
        });

        $('#id_name').val(data[1]).focus();
        $('#id_department').find("option:contains("+data[2]+")").attr('selected', true);
        $('#form_employee').attr('action', data[0])
        $('#btn_employee').text('Update');

        $('#toggle_view_employee_btn').show().attr('href', data[0] + '/read');
        $('#view_employee_btn').attr('href', data[0] + '/read');
    });
});