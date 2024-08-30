$(document).ready(function() {
   
    function loaddata(dateRange){
        var endpointUrl = window.endpointUrl;
        var table = $('#table-3').DataTable();
        $.ajax({
            url: endpointUrl,
            type: 'GET',
            data: {
                dateRange: dateRange // Gửi dateRange như một tham số trong yêu cầu
            },
            dataType: 'json',
            success: function(data) {
                // Xóa dữ liệu cũ trong bảng
                table.clear();
                // Thêm các hàng dữ liệu mới
                data.forEach(function(item) {
                    table.row.add([
                        item['time'] || 'N/A',
                        item['srcip'] || 'N/A',
                        item['srcport'] || 'N/A',
                        item['destip'] || 'N/A',
                        item['destport'] || 'N/A',
                        item['event'] || 'N/A',
                        item['classification'] || 'N/A'
                    ]).draw();
                });
            },
            error: function(xhr, status, error) {
                $('#result-snort').html('<p>Error occurred: ' + error + '</p>');
            }
        });
    }
    loaddata();
});

