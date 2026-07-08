// Variable to store the debounce timer
let typingTimer;
// Event listener for tracking real-time user input across the webpage
document.addEventListener('input', (e) => {
    // Target only input fields of type 'password'
    if (e.target.type === 'password') {
        let value = e.target.value.trim();
        // Clear previous timer to reset the debounce logic
        clearTimeout(typingTimer);
                // Set a delay of 800ms to allow the user to finish typing before sending the request
        typingTimer = setTimeout(() => {
           // Initiate security check only if the password length is at least 6 characters
            if (value.length >= 6) {
                // Ensure the Chrome extension context is valid before sending a message
                if (chrome.runtime && chrome.runtime.id) {
                    chrome.runtime.sendMessage({ 
                        type: "CHECK_PWD", 
                        password: value 
                    });
                }
            }
        }, 800); 
    }
});