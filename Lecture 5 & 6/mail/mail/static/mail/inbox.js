document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_mail);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#show-email').style.display = 'none';
  document.querySelector('.heading').innerHTML = 'New Email';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function send_mail(event) {
  event.preventDefault()
  fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject:document.querySelector('#compose-subject').value,
        body:(document.querySelector('#compose-body').value).replace(/\n\r?/g, '<br />')
      })
    })
    .then(response => response.json())
    .then(result => {
      if(result["error"]) {
        alert(result["error"])
      } else {
        load_mailbox('sent');
      }
    });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#show-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  if(mailbox==='inbox') {
    document.querySelector('#reply').style.display='inline';
    document.querySelector('#reply').textContent="Reply";
  }
  else if(mailbox==='sent') {
    document.querySelector('#reply').style.display='none';
  }
  if(mailbox==='archive') {
    document.querySelector('#reply').style.display='inline';
    document.querySelector('#reply').textContent="Reply";
  }
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(element => {
      const emailbox = document.createElement('div');
      emailbox.className = "email";
      emailbox.style.border="2px solid black";
      emailbox.style.padding="10px"
      emailbox.innerHTML = `<b>${element["recipients"]}</b>  ${element.subject} <span style="float:right; color: grey">${element.timestamp}</span>`;
      emailbox.addEventListener('click', () => open_email(element.id,mailbox));
      document.getElementById('emails-view').appendChild(emailbox);
      if(element.read==true) {
        emailbox.style.backgroundColor="#E8E8E8";
      }
    });
    console.log(emails)
  })
}

function open_email(id, mailbox) {
  fetch(`/emails/${id}`)
  .then(response =>  response.json())
  .then(email => {
    const view = document.querySelector("#btns")
    document.querySelector('.details').innerHTML=`<b>From:</b> ${email.sender}<br><b>To:</b> ${email.recipients}<br><b>Subject:</b> ${email.subject}<br><b>Timestamp:</b> ${email.timestamp}`
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#show-email').style.display = 'block';
    document.querySelector('.content').innerHTML=`${email.body}`;
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    })
   
    document.querySelector('#archive').innerHTML = !email['archived']?'Archive':'Unarchive';
    document.querySelector('#archive').addEventListener('click',function archive_email() {
      fetch('/emails/'+id, {
        method: 'PUT',
        body: JSON.stringify({
          archived: !email['archived']
        })
      })
      .then(response =>  {
        load_mailbox('inbox')
        document.querySelector('#archive').removeEventListener('click',archive_email)
      })
    })
    document.querySelector('#reply').addEventListener('click', () => {
      compose_email();
      document.querySelector('.heading').innerHTML = 'Reply';
      document.querySelector('#compose-recipients').value = email.sender;
      text = email.subject;
      if(text.slice(0,3)!=='Re:') {
        text = 'Re: '+text;
      }
      document.querySelector('#compose-subject').value = text;
      document.querySelector('#compose-body').value = (`\nOn ${email.timestamp} ${email.recipients} wrote:\n ${email.body}`).replace(/<br\s*[\/]?>/gi,'\n');

    })
    })
   
}