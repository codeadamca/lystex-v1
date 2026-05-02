
document.addEventListener("DOMContentLoaded", () => {
  
    document.getElementById('contactForm').addEventListener('submit', async function(e) {

    e.preventDefault();

        let valid = true;
        // Clear previous error styles
        document.getElementById('name').style.border = '';
        document.getElementById('email').style.border = '';
        document.getElementById('message').style.border = '';

    // Name validation
    const nameInput = document.getElementById('name');
    const name = nameInput.value.trim();
    if (!name) {
        nameInput.style.border = '2px solid red';
        valid = false;
    }

    // Email validation
    const emailInput = document.getElementById('email');
    const email = emailInput.value.trim();
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email) {
        emailInput.style.border = '2px solid red';
        valid = false;
    } else if (!emailPattern.test(email)) {
        emailInput.style.border = '2px solid red';
        valid = false;
    }

    // Message validation
    const messageInput = document.getElementById('message');
    const message = messageInput.value.trim();
    if (!message) {
        messageInput.style.border = '2px solid red';
        valid = false;
    }

    if (!valid) {
        return;
    }

    // If valid, send fetch POST request
    try {
        const response = await fetch('https://tools.brickmmo.com/email/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                name: name,
                email: email,
                subject: "LYSTEX Contact Form Submission"
            })
        });
        if (response.ok) {
            // Remove the form and show thank you message
            const form = document.getElementById('contactForm');
            const thankYou = document.createElement('h3');
            thankYou.textContent = 'Thank you! Your request has been submitted!';
            form.parentNode.replaceChild(thankYou, form);
        } else {
            // alert('There was an error sending your message.');
        }
    } catch (error) {
        // alert('There was an error sending your message.');
    }
    });

});
