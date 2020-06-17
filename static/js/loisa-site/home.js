let getInstagramFeed = async() => {
    $.ajax({
        url: '/instagramFeed', 
        type: 'POST',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({
            'posts': await instagramPhotos()
        }),
        success: function(post) {
            $('#instagramFeed')['0']['innerHTML'] = post;
        }
    });
};

let getYoutubeFeed = async() => {
    let screenWidth = (+window.getComputedStyle(document.body).width.replace(/px/,''));

    $.ajax({
        url: '/youtubeFeed', 
        type: 'POST',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({
            'screenWidth': screenWidth
        }),
        success: function(post) {
            $('#youtubeFeed')['0']['innerHTML'] = post;
        }
    });
};

window.onload = async () => {
    videoIndex = 0;

    await getYoutubeFeed();

    await getInstagramFeed();
}

window.onresize = async () => {
    videoIndex = 0;
    
    await getYoutubeFeed();

    await getInstagramFeed();
}

$(document).on('click', '[id=carouselPost]', function(e) {
    e.preventDefault();
    
    return $.ajax({
        url: '/post/get', 
        type: 'POST',
        data: JSON.stringify({ 
            'carouselPost': $(this)['0']['attributes']['value']['value'] 
        }),
        contentType: 'application/json;charset=UTF-8',
        success: function(post) {
            return location.href = '/post';
        }
    });
});

$('form#carousel').submit(function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    // Add to formData the button which was pressed
    formData.append('button', $(document.activeElement).attr('id'));

    return $.ajax({
        url: '/carousel',
        type: 'POST',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        complete: function(m) {
            return window.location.href='/home';
        }
    });
})

let videoIndex = 0;
    
$(document).on('click', 'a#prevVideo', function(e) {
    e.preventDefault();

    let frames = document.querySelectorAll('*[id=video]');

    if (videoIndex > 0)  {
        let prevFrame = frames[videoIndex];

        videoIndex -= 1;
        
        let frame = frames[videoIndex];

        prevFrame.style.display = 'none';
        frame.style.display = 'inline-block';
        $('#nextVideo')['0'].style.color = 'rgba(158, 206, 116, 0.659)';
        if (videoIndex == 0) $('#prevVideo')['0'].style.color = 'silver';
    }
    else $('#prevVideo')['0'].style.color = 'silver';
});

$(document).on('click', 'a#nextVideo', function(e) {
    e.preventDefault();

    let frames = document.querySelectorAll('*[id=video]');
    
    if (videoIndex < (frames.length - 1)) {
        let prevFrame = frames[videoIndex];
        
        videoIndex += 1;
        
        let frame = frames[videoIndex];

        prevFrame.style.display = 'none';
        frame.style.display = 'inline-block';
        $('#prevVideo')['0'].style.color = 'rgba(158, 206, 116, 0.659)';
        if (videoIndex == (frames.length - 1)) $('#nextVideo')['0'].style.color = 'silver';
    }
    else $('#nextVideo')['0'].style.color = 'silver';
});