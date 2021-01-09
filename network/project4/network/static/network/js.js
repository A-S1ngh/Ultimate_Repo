function edit(post_id) {
  var edit_button = document.querySelector(`#editbutton${post_id}`);
  var post_body = document.querySelector(`#editbody${post_id}`);
  edit_button.style.display = "block";
  post_body.style.display = "block";

  edit_button.addEventListener('click', () => {
    fetch('/edit/' + post_id, {
            method: 'PUT',
            body: JSON.stringify({
                body: post_body.value
            })
    });
    edit_button.style.display = "none";
    post_body.style.display = "none";
    document.querySelector(`#post${post_id}`).innerHTML = post_body.value;
  })
}

function like(id) {
  var like_btn = document.querySelector(`#likebutton${id}`);
  var like_ct = document.querySelector(`#likecount${id}`);

   like_btn.addEventListener('click', () => {

       if (like_btn.style.backgroundColor == 'white') {
           fetch('/like/' + id, {
               method: 'PUT',
               body: JSON.stringify({
                   like: true
               })
             })

           like_btn.style.backgroundColor = 'red';

           fetch('/like/'+ id)
           .then(response => response.json())
           .then(post => {

               like_ct.innerHTML = post.likecount;
           });
       }
       else {
           fetch('/like/' + id, {
               method: 'PUT',
               body: JSON.stringify({
                   like: false
               })
             });

           like_btn.style.backgroundColor = 'white';

           fetch('/like/'+`${id}`)
           .then(response => response.json())
           .then(post => {
               like_ct.innerHTML = post.likecount;
           });
       }
       return false;
   });
}
