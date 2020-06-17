let fadeOutInterval = null;

displayFlashMessage = async(id, m) => {
    let message = "";
    console.log(m)
    if (m['response']['statusCode'] === 200) message = '<div class="alert alert-success"><i class="fa fa-check fa-fw"></i> ' + m['response']['message'] + '</div>';
    else message = '<div class="alert alert-danger"><i class="fa fa-times fa-fw"></i> ' + m['response']['message'] + '</div>';     
        
    id["0"]["innerHTML"] = message;
    console.log()
    clearInterval(fadeOutInterval);

    id['0']['style']['visibility'] = 'visible';
    
    fadeOutInterval = setInterval(function() {
        id['0']['style']['visibility'] = 'hidden';
    }, 4000);
}

$('#contactForm').submit(function(e) {
    e.preventDefault();
    
    let data = {
        'name': $('#name').val(),
        'email': $('#email').val(),
        'message': $('#message').val(),
        'emailSubscription': document.getElementById('emailSubscription').checked
    }

    return $.ajax({
        url: '/contact/message', 
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json;charset=UTF-8',
        success: function(response) {
            console.log(response)
            displayFlashMessage($("#messageStatus"), response);

            $("#divName").load(document.URL + ' #divName');
            $("#divEmail").load(document.URL + ' #divEmail');
            $("#divMessage").load(document.URL + ' #divMessage');
            $("#divEmailSubscription").load(document.URL + ' #divEmailSubscription');
        }
    });
})

$('form#contact').submit(function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    // Add to formData the button which was pressed
    formData.append('button', $(document.activeElement).attr('id'));

    return $.ajax({
        url: '/contact/update',
        type: 'POST',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        complete: function(m) {
            return window.location.href='/contact';
        }
    });
})