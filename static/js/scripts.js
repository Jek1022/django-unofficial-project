$(function() {

    $('.pagination').addClass('flex space-x-4');
    
    $('#department tbody tr').on('click',function() {

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
});