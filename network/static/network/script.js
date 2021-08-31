//Start with the first post
let counter = 0;

//Load posts 10 at a time
const quantity = 10;
//page number
let page=1;

document.addEventListener('DOMContentLoaded', () => {
    load();
    load_profile();
    load_following();

    document.addEventListener('click', event => {
        //find what is clicked on
        const element = event.target;
        //We check if the user clicked the like button
        if (element.className === 'like_button') {

            fetch(`/like/${element.dataset.id}`)
                .then(response => response.json())
                .then(data => {
                    contents = data.posts[0];

                    post_div = element.parentElement;

                    var old_date = contents.date;

                    var new_date = new Date(old_date);

                    var today = new_date;
                    var dd = today.getDate();

                    var mm = today.getMonth() + 1;
                    var yyyy = today.getFullYear();
                    var hours = today.getHours();
                    var minutes = today.getMinutes();

                    if (dd < 10) {
                        dd = '0' + dd;
                    }

                    if (mm < 10) {
                        mm = '0' + mm;
                    } 12
                    if (hours < 10) {
                        hours = '0' + hours;
                    }
                    if (minutes < 10) {
                        minutes = '0' + minutes;
                    }

                    date = mm + '-' + dd + '-' + yyyy + " " + "(" + hours + ":" + minutes + ")";
                    post_div.innerHTML = "";

                    //Code to see if post was liked or not 
                    found = false;
                    for (let i = 0; i < data.likes.length; i++) {

                        if (data.likes[i].user == data.user && contents.id == data.likes[i].post) {
                            found = true;
                            break;
                        }
                        else {
                            found = false;
                        }
                    }

                    let image = ""
                    if (found == true) {
                        image = "data:image/png;base64,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";
                    }
                    if (found == false) {
                        image = "https://pixy.org/src/442/4422490.png";
                    }

                    //Code to see if we add an edit button or not to the post
                    //If the post was created by the user then show. Else dont show.
                    if (contents.user == data.username) {
                        post_div.innerHTML = `<h4 id="post_username" class="post_username"><a href="profile/${contents.user}"  style="color:white;font-size:15px; font-weight:900;">${contents.user} </a></h4>
                        <h6 id="post_date">${date}</h6>
                        <h6 id="post_post" style="font-family:Segoe UI;">${contents.post}</h6>
                        <img class="like_button" data-id=${contents.id}  src=${image}>
                        <h6 id="likes_counter">${contents.likes}</h6>
                        <img class="post_profile_pic" src="../images/${contents.image}">
                        <img id="edit_button" data-id=${contents.id} src="../images/settings.jpg">
                        <p class="hidden" >Edit</p>`;
                    }
                    if (contents.user !=data.username) {
                        post_div.innerHTML = `<h4 id="post_username" class="post_username"><a href="profile/${contents.user}"  style="color:white;font-size:15px; font-weight:900;">${contents.user} </a></h4>
                                    <h6 id="post_date">${date}</h6>
                                    <h6 id="post_post" style="font-family:Segoe UI;">${contents.post}</h6>
                                    <img class="like_button" data-id=${contents.id}  src=${image}>
                                    <h6 id="likes_counter">${contents.likes}</h6>
                                    <img class="post_profile_pic" src="../images/${contents.image}">`;

                    }

                    profile_picture = "";

                    if (data.user == data.username) {
                        //Getting profile picture.
                        profile_picture = contents.image;
                        // Create new post
                        const profile_pic = document.createElement('div');
                        profile_pic.className = 'profile_pic';

                        const profile_pic1 = document.createElement('div');
                        profile_pic1.className = 'profile_pic1';

                        profile_pic.innerHTML = `<img class="profile_pic" src="images/${profile_picture}">`;
                        profile_pic1.innerHTML = `<img class="profile_pic1" src="images/${profile_picture}">`;

                        document.querySelector("#profile_pic").append(profile_pic);
                        document.querySelector("#profile_pic1").append(profile_pic1);
                    }

                })
        }
        if (element.id === 'edit_button') {
            fetch(`/edit/${element.dataset.id}`)
                .then(response => response.json())
                .then(data => {
                    contents = data.posts[0];

                    post_div = element.parentElement;

                    var old_date = contents.date;

                    var new_date = new Date(old_date);

                    var today = new_date;
                    var dd = today.getDate();

                    var mm = today.getMonth() + 1;
                    var yyyy = today.getFullYear();
                    var hours = today.getHours();
                    var minutes = today.getMinutes();

                    if (dd < 10) {
                        dd = '0' + dd;
                    }

                    if (mm < 10) {
                        mm = '0' + mm;
                    } 12
                    if (hours < 10) {
                        hours = '0' + hours;
                    }
                    if (minutes < 10) {
                        minutes = '0' + minutes;
                    }

                    date = mm + '-' + dd + '-' + yyyy + " " + "(" + hours + ":" + minutes + ")";
                    post_div.innerHTML = "";

                    //Code to see if post was liked or not 
                    found = false;
                    for (let i = 0; i < data.likes.length; i++) {

                        if (data.likes[i].user == data.user && contents.id == data.likes[i].post) {
                            found = true;
                            break;
                        }
                        else {
                            found = false;
                        }
                    }

                    let image = ""
                    if (found == true) {
                        image = "data:image/png;base64,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";
                    }
                    if (found == false) {
                        image = "https://pixy.org/src/442/4422490.png";
                    }
                    


                    post_div.innerHTML = `<h4 id="post_username" class="post_username"><a href="profile/${contents.user}"  style="color:white;font-size:15px; font-weight:900;">${contents.user} </a></h4>
                    <h6 id="post_date">${date}</h6>
                    <input id="re_post_button" type="submit" value="Re-post"  data-id="${contents.id} "class="btn btn-primary">
                    <img class="post_profile_pic" style="top:-40%; left:-15%;"src="../images/${contents.image}">
                    <textarea name="content" id="edit_textarea" style="font-family:Segoe UI"; placeholder="${contents.post}"></textarea>`;

                    document.querySelector("#edit_textarea").innerHTML=`${contents.post}`;
                    



                    profile_picture = "";

                    if (data.user == data.username) {
                        //Getting profile picture.
                        profile_picture = contents.image;
                        // Create new post
                        const profile_pic = document.createElement('div');
                        profile_pic.className = 'profile_pic';

                        const profile_pic1 = document.createElement('div');
                        profile_pic1.className = 'profile_pic1';

                        profile_pic.innerHTML = `<img class="profile_pic" src="images/${profile_picture}">`;
                        profile_pic1.innerHTML = `<img class="profile_pic1" src="images/${profile_picture}">`;

                        document.querySelector("#profile_pic").append(profile_pic);
                        document.querySelector("#profile_pic1").append(profile_pic1);
                    }

                })
        }
        if (element.id === 're_post_button'){
            new_post = document.querySelector("#edit_textarea").value;
            elem_id = element.dataset.id;
            elem_id = elem_id.slice(0,-1);

            fetch(`/repost/${elem_id}/${new_post.trim()}`)
                .then(response => response.json())
                .then(data => {
                    contents = data.posts[0];

                    post_div = element.parentElement;

                    var old_date = contents.date;

                    var new_date = new Date(old_date);

                    var today = new_date;
                    var dd = today.getDate();

                    var mm = today.getMonth() + 1;
                    var yyyy = today.getFullYear();
                    var hours = today.getHours();
                    var minutes = today.getMinutes();

                    if (dd < 10) {
                        dd = '0' + dd;
                    }

                    if (mm < 10) {
                        mm = '0' + mm;
                    } 12
                    if (hours < 10) {
                        hours = '0' + hours;
                    }
                    if (minutes < 10) {
                        minutes = '0' + minutes;
                    }

                    date = mm + '-' + dd + '-' + yyyy + " " + "(" + hours + ":" + minutes + ")";
                    post_div.innerHTML = "";

                    //Code to see if post was liked or not 
                    found = false;
                    for (let i = 0; i < data.likes.length; i++) {

                        if (data.likes[i].user == data.user && contents.id == data.likes[i].post) {
                            found = true;
                            break;
                        }
                        else {
                            found = false;
                        }
                    }

                    let image = ""
                    if (found == true) {
                        image = "data:image/png;base64,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";
                    }
                    if (found == false) {
                        image = "https://pixy.org/src/442/4422490.png";
                    }
                    


                    post_div.innerHTML = `<h4 id="post_username" class="post_username"><a href="profile/${contents.user}"  style="color:white;font-size:15px; font-weight:900;">${contents.user} </a></h4>
                    <h6 id="post_date">${date}</h6>
                    <h6 id="post_post" style="font-family:Segoe UI;">${contents.post}</h6>
                    <img class="like_button" data-id=${contents.id}  src=${image}>
                    <h6 id="likes_counter">${contents.likes}</h6>
                    <img class="post_profile_pic" src="../images/${contents.image}">
                    <img id="edit_button" data-id=${contents.id} src="../images/settings.jpg">
                    <p class="hidden" >Edit</p>`;
                    



                    profile_picture = "";

                    if (data.user == data.username) {
                        //Getting profile picture.
                        profile_picture = contents.image;
                        // Create new post
                        const profile_pic = document.createElement('div');
                        profile_pic.className = 'profile_pic';

                        const profile_pic1 = document.createElement('div');
                        profile_pic1.className = 'profile_pic1';

                        profile_pic.innerHTML = `<img class="profile_pic" src="images/${profile_picture}">`;
                        profile_pic1.innerHTML = `<img class="profile_pic1" src="images/${profile_picture}">`;

                        document.querySelector("#profile_pic").append(profile_pic);
                        document.querySelector("#profile_pic1").append(profile_pic1);
                    }

                })
        }
        if (element.id ==='post_follow_button'){
            fetch(`/follow/${element.dataset.id}`)
                .then(response => response.json())
                .then(data => {
                    contents = data.posts[0];

                    //Here we check if the user follows the person from the post so we can decide if we
                    //want to show the follow button or not.
                    follow_found = false;
                    for(let i =0;i<data.follows.length;i++){
                       

                        if(data.follows[i].user== data.username && contents.user == data.follows[i].following){
                            follow_found =true;
                            break;
                        }
                        else {
                            follow_found = false;
                        }
                    }
                       //Now that we know if the current user follows the profile clicked on we 
                        //Can display the follow or unfollow button accordingly
                        const follow_button = document.createElement('div');
                    

                        //Only show button if profile clicked on is not the same as the current user

                        if(follow_found==true){
                            follow_button.innerHTML=`<button id="post_follow_button" data-id=${contents.id}>Unfollow</button>`;
                            document.querySelector('#follow_div').append(follow_button);
                        }
                        if(follow_found==false){
                            follow_button.innerHTML=`<button id="post_follow_button" data-id=${contents.id}>Follow</button>`;
                            document.querySelector('#follow_div').append(follow_button);
                        
                        }

                        //Update Following and Followers count respectively
                        document.querySelector("#following_counter").innerHTML=`${data.following} Following`;
                        document.querySelector("#followers_counter").innerHTML=`${data.followers} Followers`;
        


                })
            
        }
        if(element.id ==='prev'){
            
            document.querySelector("#posts_container").innerHTML="";
            // Set start and end post numbers, and update counter
            const start = counter;
            const end = start + quantity;
            
            if(page-1!=0){
                page-=1;
            }
            
            // Get new posts and add posts
            fetch(`/post?page=${page}`)
            
                .then(response => response.json())
                .then(data => {
                    for (let i = 0; i < data.posts.length; i++) {
                        
                        add_post(data.posts[i], data.likes, data.user, data.username, data.user_image,data.totalpages)
                    }

                })
        }
        if(element.id ==='next'){
            document.querySelector("#posts_container").innerHTML="";
            
            let total_pages = document.querySelector("#home_total_pages").innerHTML;
            page+=1;
           
            if(page>parseInt(total_pages)){
                page--;
            }
            console.log(page);
            console.log(total_pages);
            
            // Get new posts and add posts
            fetch(`/post?page=${page}`)
            
                .then(response => response.json())
                .then(data => {
                    for (let i = 0; i < data.posts.length; i++) {
                        
                        add_post(data.posts[i], data.likes, data.user, data.username, data.user_image, data.totalpages,data.currentpage)
                    }

                })
        }
        if(element.id =='user_next'){
            document.querySelector("#profile_posts_container").innerHTML="";
            
            let total_pages = parseInt(document.querySelector("#user_total_pages").innerHTML);
            page+=1;
            if(page>total_pages){
                page-=1;
            }
            
            // Get new posts and add posts
            fetch(`/user/${user_clicked}?page=${page}`)
                .then(response => response.json())
                .then(data => {
                    for (let i = 0; i < data.posts.length; i++) {
                        profile_add_post(data.posts[i], data.likes, data.user, data.username, data.user_image,data.follows,data.following,data.followers,data.totalpages,data.currentpage)
                    }
        
            })
        }
        if(element.id =='user_prev'){
            document.querySelector("#profile_posts_container").innerHTML="";
            
            if(page-1!=0){
                page-=1;
            }
            
            
            // Get new posts and add posts
            fetch(`/user/${user_clicked}?page=${page}`)
                .then(response => response.json())
                .then(data => {
                    for (let i = 0; i < data.posts.length; i++) {
                        profile_add_post(data.posts[i], data.likes, data.user, data.username, data.user_image,data.follows,data.following,data.followers,data.totalpages,data.currentpage)
                    }
        
            })
        }
        if(element.id =='follow_next'){
            document.querySelector("#follow_posts_container").innerHTML="";
            
            let total_pages = document.querySelector("#follow_total_pages").innerHTML;

            page+=1;
            if(page>total_pages){
                page-=1;
            }
            
            // Get new posts and add posts
            fetch(`following?page=${page}`)
                .then(response => response.json())
                .then(data => {
                    for (let i = 0; i < data.posts.length; i++) {
                        follow_add_post(data.posts[i], data.likes, data.user, data.username, data.user_image,data.follows,data.following,data.followers,data.totalpages,data.currentpage)
                        
                    }
        
            })
        }
        if(element.id =='follow_prev'){
            document.querySelector("#follow_posts_container").innerHTML="";
            
            if(page-1!=0){
                page-=1;
            }
            
            
            // Get new posts and add posts
            fetch(`following?page=${page}`)
                .then(response => response.json())
                .then(data => {
                    for (let i = 0; i < data.posts.length; i++) {
                        follow_add_post(data.posts[i], data.likes, data.user, data.username, data.user_image,data.follows,data.following,data.followers,data.totalpages,data.currentpage)
                    }
        
            })
        }
    });

});


function load() {
    // Set start and end post numbers, and update counter
    const start = counter;
    const end = start + quantity;
    //counter = end + 1;
    page=1;
    // Get new posts and add posts
    fetch(`/post?page=${page}`)
        .then(response => response.json())
        .then(data => {
            for (let i = 0; i < data.posts.length; i++) {
                add_post(data.posts[i], data.likes, data.user, data.username, data.user_image,data.totalpages,data.currentpage)
                
            }

        })
};
function load_following() {
    

    // Get new posts and add posts
    fetch(`/following?page=${page}`)
        .then(response => response.json())
        .then(data => {
            for (let i = 0; i < data.posts.length; i++) {
                follow_add_post(data.posts[i], data.likes, data.user, data.username, data.user_image,data.following,data.followers,data.totalpages,data.currentpage)
            }

        })
};

function load_profile() {
    
    //Getting the  value of the current url to be able
    //to see which username the current user clicked.
    current_link = window.location.href
    user_clicked = current_link.slice(30, current_link.length)


    // Get new posts and add posts
    fetch(`/user/${user_clicked}?page=${page}`)
        .then(response => response.json())
        .then(data => {
            for (let i = 0; i < data.posts.length; i++) {
                profile_add_post(data.posts[i], data.likes, data.user, data.username, data.user_image,data.follows,data.following,data.followers,data.totalpages,data.currentpage)
            }
            
        })

};
// Add a new post with given contents to DOM
function add_post(data_post, data_likes, user, username, user_image,totalpages,currentpage) {
    // Create new post
    const post = document.createElement('div');
    post.className = 'post_div';
    var old_date = data_post.date
    var new_date = new Date(old_date)

    var today = new_date;
    var dd = today.getDate();

    var mm = today.getMonth() + 1;
    var yyyy = today.getFullYear();
    var hours = today.getHours();
    var minutes = today.getMinutes();

    if (dd < 10) {
        dd = '0' + dd;
    }

    if (mm < 10) {
        mm = '0' + mm;
    } 12
    if (hours < 10) {
        hours = '0' + hours;
    }
    if (minutes < 10) {
        minutes = '0' + minutes;
    }

    date = mm + '-' + dd + '-' + yyyy + " " + "(" + hours + ":" + minutes + ")";
    //Code to see if post was liked or not 
    found = false;
    for (let i = 0; i < data_likes.length; i++) {

        if (data_likes[i].user == user && data_post.id == data_likes[i].post) {
            found = true;
            break;
        }
        else {
            found = false;
        }
    }
    let image = ""
    if (found == true) {
        image = "data:image/png;base64,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";
    }
    if (found == false) {
        image = "https://pixy.org/src/442/4422490.png";
    }

  
    //Code to see if we add an edit button or not to the post
    //If the post was created by the user then show. Else dont show.
    if (data_post.user == username) {
        post.innerHTML = `<h4 id="post_username" class="post_username"><a href="profile/${data_post.user}"  style="color:white;font-size:15px; font-weight:900;">${data_post.user} </a></h4>
        <h6 id="post_date">${date}</h6>
        <h6 id="post_post" style="font-family:Segoe UI;">${data_post.post}</h6>
        <img class="like_button" data-id=${data_post.id}  src=${image}>
        <h6 id="likes_counter">${data_post.likes}</h6>
        <img class="post_profile_pic" src="images/${data_post.image}">
        <img id="edit_button" data-id=${data_post.id} src="../images/settings.jpg">
        <p class="hidden" >Edit</p>`;
    }
    if (data_post.user != username) {
        
        post.innerHTML = `<h4 id="post_username" class="post_username"><a href="profile/${data_post.user}"  style="color:white;font-size:15px; font-weight:900;">${data_post.user} </a></h4>
                    <h6 id="post_date">${date}</h6>
                    <h6 id="post_post" style="font-family:Segoe UI;">${data_post.post}</h6>
                    <img class="like_button" data-id=${data_post.id}  src=${image}>
                    <h6 id="likes_counter">${data_post.likes}</h6>
                    <img class="post_profile_pic" src="images/${data_post.image}">`;
       
    }
    document.querySelector("#home_total_pages").innerHTML=`${totalpages}`;



    // Add post to DOM
    document.querySelector('#posts_container').append(post);
    profile_picture = "";

    //Getting profile picture.
    profile_picture = user_image;
    // Create new post
    const profile_pic = document.createElement('div');
    profile_pic.className = 'profile_pic';

    const profile_pic1 = document.createElement('div');
    profile_pic1.className = 'profile_pic1';

    profile_pic.innerHTML = `<img class="profile_pic" src="images/${profile_picture}">`;
    profile_pic1.innerHTML = `<img class="profile_pic1" src="images/${profile_picture}">`;

    document.querySelector("#profile_pic").append(profile_pic);
    document.querySelector("#profile_pic1").append(profile_pic1);


    //Page num
    document.querySelector("#pagenum").innerHTML=`${page} of ${totalpages}`;
    

};

function follow_add_post(data_post, data_likes, user, username, user_image,following,followers,totalpages,currentpage) {
    
    // Create new post
    const post = document.createElement('div');
    post.className = 'post_div';
    var old_date = data_post.date
    var new_date = new Date(old_date)

    var today = new_date;
    var dd = today.getDate();

    var mm = today.getMonth() + 1;
    var yyyy = today.getFullYear();
    var hours = today.getHours();
    var minutes = today.getMinutes();

    if (dd < 10) {
        dd = '0' + dd;
    }

    if (mm < 10) {
        mm = '0' + mm;
    } 12
    if (hours < 10) {
        hours = '0' + hours;
    }
    if (minutes < 10) {
        minutes = '0' + minutes;
    }

    date = mm + '-' + dd + '-' + yyyy + " " + "(" + hours + ":" + minutes + ")";
    //Code to see if post was liked or not 
    found = false;
    for (let i = 0; i < data_likes.length; i++) {

        if (data_likes[i].user == user && data_post.id == data_likes[i].post) {
            found = true;
            break;
        }
        else {
            found = false;
        }
    }
    let image = ""
    if (found == true) {
        image = "data:image/png;base64,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";
    }
    if (found == false) {
        image = "https://pixy.org/src/442/4422490.png";
    }

    

  
    //Code to see if we add an edit button or not to the post
    //If the post was created by the user then show. Else dont show.
    if (data_post.user == username) {
        post.innerHTML = `<h4 id="post_username" class="post_username"><a href="profile/${data_post.user}"  style="color:white;font-size:15px; font-weight:900;">${data_post.user} </a></h4>
        <h6 id="post_date">${date}</h6>
        <h6 id="post_post" style="font-family:Segoe UI;">${data_post.post}</h6>
        <img class="like_button" data-id=${data_post.id}  src=${image}>
        <h6 id="likes_counter">${data_post.likes}</h6>
        <img class="post_profile_pic" src="images/${data_post.image}">
        <img id="edit_button" data-id=${data_post.id} src="../images/settings.jpg">
        <p class="hidden" >Edit</p>`;
    }
    if (data_post.user != username) {
        
        post.innerHTML = `<h4 id="post_username" class="post_username"><a href="profile/${data_post.user}"  style="color:white;font-size:15px; font-weight:900;">${data_post.user} </a></h4>
                    <h6 id="post_date">${date}</h6>
                    <h6 id="post_post" style="font-family:Segoe UI;">${data_post.post}</h6>
                    <img class="like_button" data-id=${data_post.id}  src=${image}>
                    <h6 id="likes_counter">${data_post.likes}</h6>
                    <img class="post_profile_pic" src="images/${data_post.image}">`;
       
    }

    if(document.querySelector("#follow_total_pages").innerHTML=="0"){
        document.querySelector("#follow_total_pages").innerHTML=`${totalpages}`;
    };

    // Add post to DOM
    document.querySelector('#follow_posts_container').append(post);
    profile_picture = "";

    //Getting profile picture.
    profile_picture = user_image;
    // Create new post
    const profile_pic = document.createElement('div');
    profile_pic.className = 'profile_pic';

    const profile_pic1 = document.createElement('div');
    profile_pic1.className = 'profile_pic1';

    profile_pic.innerHTML = `<img class="profile_pic" src="images/${profile_picture}">`;
    profile_pic1.innerHTML = `<img class="profile_pic1" src="images/${profile_picture}">`;

    document.querySelector("#profile_pic").append(profile_pic);
    document.querySelector("#profile_pic1").append(profile_pic1);


   
    
    document.querySelector("#pagenum").innerHTML=`${page} of ${document.querySelector("#follow_total_pages").innerHTML}`;
    
};


function profile_add_post(data_post, data_likes, user, username, user_image,data_follows,following,followers,total_pages,currentpage) {
    // Create new post
    const post = document.createElement('div');
    post.className = 'post_div';
    var old_date = data_post.date
    var new_date = new Date(old_date)

    var today = new_date;
    var dd = today.getDate();

    var mm = today.getMonth() + 1;
    var yyyy = today.getFullYear();
    var hours = today.getHours();
    var minutes = today.getMinutes();

    if (dd < 10) {
        dd = '0' + dd;
    }

    if (mm < 10) {
        mm = '0' + mm;
    } 12
    if (hours < 10) {
        hours = '0' + hours;
    }
    if (minutes < 10) {
        minutes = '0' + minutes;
    }

    date = mm + '-' + dd + '-' + yyyy + " " + "(" + hours + ":" + minutes + ")";
    //Code to see if post was liked or not 
    found = false;
    for (let i = 0; i < data_likes.length; i++) {

        if (data_likes[i].user == user && data_post.id == data_likes[i].post) {
            found = true;
            break;
        }
        else {
            found = false;
        }
    }
    let image = ""
    if (found == true) {
        image = "data:image/png;base64,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";
    }
    if (found == false) {
        image = "https://pixy.org/src/442/4422490.png";

    }

    //Code to see if we add an edit button or not to the post
    //If the post was created by the user then show. Else dont show.
    if (data_post.user == username) {
        post.innerHTML = `<h4 id="post_username" class="post_username"><p  style="color:white;font-size:15px; font-weight:900;">${data_post.user} </p></h4>
        <h6 id="post_date">${date}</h6>
        <h6 id="post_post" style="font-family:Segoe UI;">${data_post.post}</h6>
        <img class="like_button" data-id=${data_post.id}  src=${image}>
        <h6 id="likes_counter">${data_post.likes}</h6>
        <img class="post_profile_pic" src="../images/${data_post.image}">
        <img id="edit_button" data-id=${data_post.id} src="../images/settings.jpg">
        <p class="hidden" >Edit</p>`;
    }
    if (data_post.user != username) {
        post.innerHTML = `<h4 id="post_username" class="post_username"><p  style="color:white;font-size:15px; font-weight:900;">${data_post.user} </p></h4>
                      <h6 id="post_date">${date}</h6>
                      <h6 id="post_post" style="font-family:Segoe UI;">${data_post.post}</h6>
                      <img class="like_button" data-id=${data_post.id}  src=${image}>
                      <h6 id="likes_counter">${data_post.likes}</h6>
                      <img class="post_profile_pic" src="../images/${data_post.image}">`;

    }
    document.querySelector("#user_total_pages").innerHTML=`${total_pages}`;

    // Add post to DOM
    document.querySelector('#profile_posts_container').append(post);
    profile_picture = "";

    //Getting profile picture.
    profile_picture = user_image;
    // Create new post
    const profile_pic = document.createElement('div');
    profile_pic.className = 'profile_pic';

    const profile_pic1 = document.createElement('div');
    profile_pic1.className = 'profile_pic1';

    profile_pic.innerHTML = `<img class="profile_pic" src="../images/${profile_picture}">`;
    profile_pic1.innerHTML = `<img class="profile_pic1" src="../images/${profile_picture}">`;

    document.querySelector("#profile_pic").append(profile_pic);

    //Code to implement follow or unfollow buttons
    //Looping through the data_follows array to see if the current user follows 
    //the profile clicked on
    found=false;
    if(data_follows.length==0){
        found=false;
    }
    
    for(let i=0;i<data_follows.length;i++){
      

        if(username== data_follows[i].user && data_post.user == data_follows[i].following){
            found=true;
            break;
        }
    }

    //Now that we know if the current user follows the profile clicked on we 
    //Can display the follow or unfollow button accordingly
    const follow_button = document.createElement('div');
  

    //Only show button if profile clicked on is not the same as the current user
   
    if(username!==data_post.user){
        if(found==true){
            follow_button.innerHTML=`<button id="post_follow_button" data-id=${data_post.id}>UnFollow</button>`;
            document.querySelector('#follow_div').append(follow_button);
        }
        if(found==false){
            follow_button.innerHTML=`<button id="post_follow_button" data-id=${data_post.id}>Follow</button>`;
            document.querySelector('#follow_div').append(follow_button);
        }
        
    }
    //Code to get the Following and Followers Counter

    document.querySelector("#following_counter").innerHTML=`${following} Following`;
    document.querySelector("#followers_counter").innerHTML=`${followers} Followers`;
 

    //Page num
    document.querySelector("#pagenum").innerHTML=`${currentpage} of ${total_pages}`;

    
};


