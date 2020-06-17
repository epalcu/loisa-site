$('form#blogPost').submit(function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    // Add to formData the button which was pressed
    formData.append('button', $(document.activeElement).attr('id'));

    return $.ajax({
        url: '/myPosts/update',
        type: 'POST',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        complete: function(m) {
            return window.location.href='/myPosts';
        }
    });
})