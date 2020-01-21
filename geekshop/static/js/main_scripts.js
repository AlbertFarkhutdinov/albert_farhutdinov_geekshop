$(document).on('click', '.products_sheet a', function (event) {
    if (event.target.hasAttribute('href')) {
        var link = event.target.href + 'ajax/';
        var link_array = link.split('/');
        if (link_array[4] == 'category') {
            $.ajax({
                url: link, 
                success: function (data) {
                    $('.products_sheet').html(data.result);
                }, 
            });
            event.preventDefault();
        }
    }
});