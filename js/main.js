// A local download demo: no details are sent to a server.
const form = document.querySelector('#contact-form');
const status = document.querySelector('#form-status');
const download = document.querySelector('#download');
let fileUrl;

// Prevent accidental native submission if JavaScript is unavailable.
form.addEventListener('submit', function (event) {
  event.preventDefault();
  const name = form.elements.name.value.trim();
  const message = form.elements.message.value.trim();
  download.hidden = true;

  if (name === '' || message.length < 10) {
    status.textContent = 'Enter your name and a message of at least 10 characters.';
    if (name === '') form.elements.name.focus();
    else form.elements.message.focus();
    return;
  }

  const text = 'FORYOU enquiry\nName: ' + name +
    '\nEmail: ' + form.elements.email.value +
    '\nTopic: ' + form.elements.topic.value + '\n\n' + message;
  if (fileUrl) URL.revokeObjectURL(fileUrl);
  fileUrl = URL.createObjectURL(new Blob([text], { type: 'text/plain' }));
  download.href = fileUrl;
  download.hidden = false;
  status.textContent = 'Your enquiry is ready to download. No message has been sent.';
});

form.addEventListener('input', function () {
  download.hidden = true;
  status.textContent = '';
});
form.querySelector('button').disabled = false;
