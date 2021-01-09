document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);


  // By default, load the inbox
  load_mailbox('inbox');
  });


function send_email(event) {
  event.preventDefault();

  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: document.querySelector("#compose-recipients").value,
      subject: document.querySelector("#compose-subject").value,
      body: document.querySelector("#compose-body").value,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      console.log(result);
      load_mailbox('sent');
    })
    .catch((error) => console.log(error));
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function compose_reply(email) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = email["sender"];
  document.querySelector('#compose-subject').value = 'Re: ' + email["subject"];
  document.querySelector('#compose-body').value =
  'On ' + email["timestamp"] + ', ' + email["sender"] + ' wrote: '
   + email["body"]
  ;
}

function load_mailbox(mailbox) {

if(mailbox === "inbox"){
  fetch('/emails/inbox')
    .then(response => response.json())
    .then(emails => {
    console.log(emails);
    emails.forEach((email) => {
      if(email["archived"]){
        return;
      }
      const emaildiv = document.createElement("div");
      emaildiv.setAttribute("class", "inboxstyle");
      if(email["read"]){
        emaildiv.style.backgroundColor = "grey";
      }
      emaildiv.innerHTML = `
        <div class="inboxstyletext">${email["sender"]}  </div>
        <div class="inboxstyletext">${email["subject"]}</div>
        <div class="inboxstyletext">${email["timestamp"]}</div>
      `;
       document.querySelector('#emails-view').append(emaildiv);
      emaildiv.addEventListener('click', () => {
        fetch(`/emails/${email["id"]}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: true
          })
        })
        load_email(email["id"])
      });
    })

});
}

if(mailbox === "sent"){
  fetch('/emails/sent')
    .then(response => response.json())
    .then(emails => {
    console.log(emails);
    emails.forEach((email) => {
      const emaildiv = document.createElement("div");
      emaildiv.setAttribute("class", "inboxstyle");
      if(email["read"]){
        emaildiv.style.backgroundColor = "grey";
      }
      emaildiv.innerHTML = `
        <div class="inboxstyletext">${email["sender"]} <button</div>
        <div class="inboxstyletext">${email["subject"]}</div>
        <div class="inboxstyletext">${email["timestamp"]}</div>
      `;
      document.querySelector('#emails-view').append(emaildiv);
      emaildiv.addEventListener('click', () => {
        fetch(`/emails/${email["id"]}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: true
          })
        })
        load_email(email["id"])
      });
    })

});
}

if(mailbox === "archive"){
  fetch('/emails/archive')
    .then(response => response.json())
    .then(emails => {
    console.log(emails);
    emails.forEach((email) => {
      const emaildiv = document.createElement("div");
      emaildiv.setAttribute("class", "inboxstyle");
      if(email["read"]){
        emaildiv.style.backgroundColor = "grey";
      }
      emaildiv.innerHTML = `
        <div class="inboxstyletext">${email["sender"]} <button</div>
        <div class="inboxstyletext">${email["subject"]}</div>
        <div class="inboxstyletext">${email["timestamp"]}</div>
      `;
       document.querySelector('#emails-view').append(emaildiv);
       emaildiv.addEventListener('click', () => {
         fetch(`/emails/${email["id"]}`, {
           method: 'PUT',
           body: JSON.stringify({
             read: true
           })
         })
         load_email(email["id"])
       });
    })

});
}


  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function load_email(emailid){
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#email-view').innerHTML = ``;

  console.log(emailid);

  fetch(`/emails/${emailid}`)
    .then(response => response.json())
    .then(email => {
      console.log(email);
      const emaildiv = document.createElement("div");
      emaildiv.setAttribute("class", "fullemail");
      emaildiv.innerHTML = `
        <div class="emailstyle1">From: ${email["sender"]} <button</div>
        <div class="emailstyle1">To: ${email["recipients"]}</div>
        <div class="emailstyle1">When: ${email["timestamp"]}</div>
        <div class="emailstyle1">Subject: ${email["subject"]}</div>
        <hr>
        <div class="emailstyle2">${email["body"]}</div>
        <br><br>
        <button id="reply">Reply</button>
        <button id="archive" value="Archive">${email["archived"] ? "Unarchive" : "Archive"}</button>
      `;
      document.querySelector('#email-view').append(emaildiv);
      document.querySelector('#archive').addEventListener('click', () => {
        fetch(`/emails/${emailid}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: !email["archived"]
          })
        })
        .then(() => load_mailbox("inbox"));
        });
        document.querySelector('#reply').addEventListener('click', () => {
          compose_reply(email);
          });

    });

}
