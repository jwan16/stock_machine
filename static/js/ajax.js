$(document).ready(function(){
    $('#filter').change(function(){
        $.ajax({
            type: "POST",
            url: '/search/',
            data: {
                'PE_operator': $('.PE_operator').val(),
                'PE_number': $('.PE_number').val(),
                'QuickRatio_operator': $('.QuickRatio_operator').val(),
                'QuickRatio_number': $('.QuickRatio_number').val(),
                'CurrentRatio_operator': $('.CurrentRatio_operator').val(),
                'CurrentRatio_number': $('.CurrentRatio_number').val(),
                'PEG_operator': $('.PEG_operator').val(),
                'PEG_number': $('.PEG_number').val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            },
            success: function(data){
                 $('#search-results').html(data);
            },
            dataType: 'text',
        });
    });
});



function searchSuccess(data, textStatus, jqXHR){
    $('#search-results').html(data);
}