let notificationUrls = {};

// --- 1. PASSWORD CHECKER ---
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === "CHECK_PWD") {
        fetch('http://127.0.0.1:5000/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ password: request.password })
        })
        .then(res => res.json())
        .then(data => {
            if (!data || data.status === "inactive" || !data.strength) return;

            let strengthStr = String(data.strength).toLowerCase();
            let isStrong = (strengthStr === "strong" || strengthStr === "safe");

            if (!isStrong) {
                let notifId = "pwd_" + Date.now();
                notificationUrls[notifId] = `http://127.0.0.1:5000/password-tool?val=${encodeURIComponent(request.password)}`;
                
                chrome.notifications.create(notifId, {
                    type: "basic",
                    iconUrl: "icon.png",
                    title: "⚠️ WEAK PASSWORD DETECTED",
                    message: `AI Analysis: ${data.strength}. Click to audit security.`,
                    priority: 2
                });
            }
        }).catch(err => console.log("Password API Error"));
    }
    return true; 
});

// --- 2. URL CHECKER (Safe + Phishing + Login Check) ---
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url && tab.url.startsWith('http')) {
        
        if (tab.url.includes("127.0.0.1:5000")) return;

        fetch('http://127.0.0.1:5000/api/analyze-url', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include', // Cookies bhejne ke liye zaroori hai
            body: JSON.stringify({ url: tab.url })
        })
        .then(res => {
            // LOGIN CHECK: Agar user login nahi hai, toh Flask 401 bhejega
            if (res.status === 401) {
                console.log("User not logged in. Ignoring URL scan.");
                throw new Error("Unauthorized");
            }
            return res.json();
        })
        .then(data => {
            let notifId = "url_" + Date.now();
            notificationUrls[notifId] = `http://127.0.0.1:5000/url_tool?val=${encodeURIComponent(tab.url)}`;

            // Check if URL is Phishing/Dangerous
            if (data.prediction.toLowerCase().includes("phishing") || data.risk_score > 40) {
                chrome.notifications.create(notifId, {
                    type: "basic",
                    iconUrl: "icon.png",
                    title: "🚨 SUSPICIOUS URL DETECTED",
                    message: `Status: ${data.prediction}. Risk Score: ${data.risk_score}. Click for report.`,
                    priority: 2
                });
            } 
            // Check if URL is Safe
            else {
                chrome.notifications.create(notifId, {
                    type: "basic",
                    iconUrl: "icon.png",
                    title: "✅ URL SECURED",
                    message: `Site: ${new URL(tab.url).hostname} is safe. AI Accuracy: 92%`,
                    priority: 1
                });
            }
        })
        .catch(err => {
            if (err.message !== "Unauthorized") {
                console.log("URL API Error: Server might be down.");
            }
        });
    }
});

// --- 3. COMMON CLICK LISTENER ---
chrome.notifications.onClicked.addListener((id) => {
    if (notificationUrls[id]) {
        chrome.tabs.create({ url: notificationUrls[id] });
        delete notificationUrls[id];
    }
});