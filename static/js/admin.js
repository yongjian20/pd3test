$(document).ready(function() {
      $('#dataTable').DataTable();
});

function ban(item_id) {
    if (confirm('Confirm Ban?')) {
        alert('Item has been successfully banned.');
        window.location.href = '/ban/' + item_id;
    }
}