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
                        item['Timestamp'] || 'N/A',
                        item['Src MAC'] || 'N/A',
                        item['Dst MAC'] || 'N/A',
                        item['Dst IP'] || 'N/A',
                        item['Src IP'] || 'N/A'
                    ]).draw();
                });
            },
            error: function(xhr, status, error) {
                $('#result').html('<p>Error occurred: ' + error + '</p>');
            }
        });
    }
    loaddata();
    $('#send-data').click(function(event) {
        event.preventDefault();
        var dateRange = $('input[name="daterange-with-time"]').val(); // Lấy giá trị từ input
        loaddata(dateRange);
    });
});