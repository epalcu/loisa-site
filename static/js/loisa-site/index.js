$(document).on('click', '[id=post]', function(e) {
    e.preventDefault();
    
    return $.ajax({
        url: '/post/get', 
        type: 'POST',
        data: JSON.stringify({ 
            'post': $(this)['0']['attributes']['value']['value'] 
        }),
        contentType: 'application/json;charset=UTF-8',
        success: function(post) {
            return location.href = '/post';
        }
    });
});

$('#nextIndex').on('click', function(e) {
    e.preventDefault();
    
    $('#prevIndex')['0']['style']['display'] = 'block';
    
    return $.ajax({
        url: '/post/next',
        type: 'POST',
        data: JSON.stringify({ 
            'nextIndex' : $(this)['0']['attributes']['value']['value'],
            'source': location.pathname
        }),
        contentType: 'application/json;charset=UTF-8',
        success: function(posts) {
            if (parseInt(posts.nextIndex) >= posts.numPosts) $('#nextIndex').hide();

            $("#posts")['0']['innerHTML'] = posts.posts;
            $('#nextIndex')['0']['attributes']['value']['value'] = posts.nextIndex;
            $('#prevIndex')['0']['attributes']['value']['value'] = posts.prevIndex;
        }
    });
});

$('#prevIndex').on('click', function(e) {
    e.preventDefault();

    $('#nextIndex')['0']['style']['display'] = 'block';
    
    return $.ajax({
        url: '/post/prev',
        type: 'POST',
        data: JSON.stringify({ 
            'prevIndex' : $('#prevIndex')['0']['attributes']['value']['value'],
            'source': location.pathname
        }),
        contentType: 'application/json;charset=UTF-8',
        success: function(posts) {
            if (posts.prevIndex === '0') $('#prevIndex').hide();

            $("#posts")['0']['innerHTML'] = posts.posts;
            $('#nextIndex')['0']['attributes']['value']['value'] = posts.nextIndex;
            $('#prevIndex')['0']['attributes']['value']['value'] = posts.prevIndex;
        }
    });
});

instagramPhotos = async () => {
    // It will contain our photos' links
    const res = []
    
    try {
        const userInfoSource = await axios.get('https://www.instagram.com/loisapalcu/')
        
        // userInfoSource.data contains the HTML from Axios
        const jsonObject = userInfoSource.data.match(/<script type="text\/javascript">window\._sharedData = (.*)<\/script>/)[1].slice(0, -1)
        
        const userInfo = JSON.parse(jsonObject)

        // Retrieve only the first 10 results
        const mediaArray = userInfo.entry_data.ProfilePage[0].graphql.user.edge_owner_to_timeline_media.edges.splice(0, 6)
        for (let media of mediaArray) {
            const node = media.node
            
            // Process only if is an image
            if ((node.__typename && node.__typename !== 'GraphImage')) {
                continue
            }
            
            // Push the thumbnail src in the array
            res.push(node.thumbnail_src)
        }
    } catch (e) {
        console.error('Unable to retrieve photos. Reason: ' + e.toString())
    }
    
    return res
}
