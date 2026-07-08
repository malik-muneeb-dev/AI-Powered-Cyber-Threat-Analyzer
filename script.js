document.addEventListener('DOMContentLoaded', () => {
    // Select all UI elements for easy access
    const ui = {
        section: document.getElementById('results-section'),
        btn: document.getElementById('scan-button'),
        input: document.getElementById('password-input'),
        badge: document.getElementById('ai-strength-badge'),
        strengthText: document.getElementById('strength-text'),
        nlpDiv: document.getElementById('nlp-results'),
        breachText: document.getElementById('breach-count'),
        progressBar: document.querySelector('.progress-bar'),
        crackDisplay: document.querySelector('.crack-time-value'),
        dial: document.querySelector('.progress-dial'),
        genDiv: document.getElementById('generated-passwords')
    };

    // Ensure the results section is visible on load
    if (ui.section) ui.section.style.display = 'grid';

    if (ui.btn) {
        // Main Scan Button Event
        ui.btn.addEventListener('click', async () => {
            // Update UI to "Loading" state
            ui.btn.innerText = "SCANNING...";
            ui.btn.style.opacity = "0.7";
            ui.strengthText.innerText = "CALCULATING...";

            try {
                // Send password to the Python backend for analysis
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ password: ui.input.value }),
                });
                
                const data = await response.json();

                // Reset button state
                ui.btn.innerText = "SCAN PASSWORD";
                ui.btn.style.opacity = "1";

                // 1. Update AI Strength Badge
                
               
const isWeak = data.strength === "WEAK";

ui.strengthText.innerText = data.strength; 

if (isWeak) {
    ui.badge.className = "strength-badge weak"; 
} else {
    ui.badge.className = "strength-badge strong"; 
}
                // 2. Render NLP Warnings
                ui.nlpDiv.innerHTML = ""; 
                if (data.warnings?.length) {
                    ui.nlpDiv.innerHTML = data.warnings
                        .map(w => `<p class="warning-item"><span class="icon">⚠</span> ${w}</p>`)
                        .join('');
                }

                // 3. Render Breach Data
                if (data.breach_count > 0) {
                    ui.breachText.innerHTML = `🚨 This password appears in <b style="color:#ff4444;">${data.breach_count.toLocaleString()}</b> real data breaches.`;
                    updateProgressBar("100%", "#ff4444");
                } else {
                    ui.breachText.innerHTML = `✅ Found in <b style="color:#00ff88;">0</b> breaches. Safe!`;
                    updateProgressBar("100%", "#00ff88");
                }

                // 4. Update Crack Time Display & Radial Dial
                if (data.crack_time) {
                    const details = document.querySelectorAll('.crack-time-details .value');
                    if(details.length >= 3) {
                        details[0].innerText = data.crack_time.cpu;
                        details[1].innerText = data.crack_time.gpu;
                        details[2].innerText = data.crack_time.cluster;
                    }
                    ui.crackDisplay.innerText = data.crack_time.gpu;
                    
                    // Animate the SVG circular progress dial
                    const score = data.crack_time.score; 
                    ui.dial.style.strokeDashoffset = 282 - (282 * score) / 100;
                    
if (isWeak) {
    ui.dial.style.stroke = "#ff4444"; // Red for weak
} else {
    ui.dial.style.stroke = "#00ff88"; // Green for strong
}
                }

                // 5. Render Password Suggestions with Copy functionality
                ui.genDiv.innerHTML = "";
                if (data.suggestions) {
                    data.suggestions.forEach(pass => {
                        const p = document.createElement('p');
                        p.className = "generated-item";
                        p.innerHTML = `${pass} <span class="copy-btn" style="cursor:pointer;">📋</span>`;
                        
                        // Handle Copy to Clipboard
                        p.querySelector('.copy-btn').addEventListener('click', function() {
                            navigator.clipboard.writeText(pass);
                            this.innerText = "✅"; 
                            setTimeout(() => this.innerText = "📋", 2000);
                        });
                        ui.genDiv.appendChild(p);
                    });
                }
            } catch (error) {
                console.error('Error:', error);
                ui.btn.innerText = "ERROR";
            }
        });
    }

    /**
     * Helper to update the linear progress bar (Breach Card)
     */
    function updateProgressBar(width, color) {
        ui.progressBar.style.width = width;
        ui.progressBar.style.background = color;
        if (width == "0%") {
            ui.progressBar.style.boxShadow = "none"; 
        } else {
            ui.progressBar.style.boxShadow = "0 0 10px " + color; 
        }
    }
});