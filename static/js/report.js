function report(item_id) {
    if (window.confirm('Really go to another page?')) {
        window.location.href = '/report/' + item_id;
    }
}