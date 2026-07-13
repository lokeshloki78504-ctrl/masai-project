<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Product Card Generator</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="card-generator">
            <h2>AI Product Card Generator</h2>
            <p class="subtitle">Generate marketing copy for your product ideas</p>
            
            <input type="text" id="productInput" placeholder="AI Study Buddy...">
            <button id="generateBtn" onclick="generateProductCard()">GENERATE CARD</button>
            
            <div id="resultCard" class="result-card" style="display: none;">
                <div class="icon">🤖</div>
                <h3 id="resTitle">StudyGenius</h3>
                <p id="resTagline" class="tagline">"Study smart. Succeed brilliantly."</p>
                <p id="resDesc" class="description">Loading details...</p>
                
                <div class="btn-group">
                    <button class="btn-copy" onclick="copyText()">📋 Copy Content</button>
                    <button class="btn-reset" onclick="resetForm()">🔄 Generate Another</button>
                </div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>body {
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}
.container {
    width: 100%;
    max-width: 500px;
    padding: 20px;
}
.card-generator {
    background: white;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    text-align: center;
}
h2 { color: #333; margin-bottom: 5px; }
.subtitle { color: #666; font-size: 14px; margin-bottom: 25px; }
input {
    width: 90%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 16px;
    margin-bottom: 15px;
    outline: none;
}
button {
    width: 95%;
    padding: 12px;
    background: #4f46e5;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: 0.3s;
}
button:hover { background: #4338ca; }
.result-card {
    margin-top: 30px;
    padding: 20px;
    border: 1px solid #eee;
    border-radius: 12px;
    background: #fafafa;
    text-align: left;
}
.icon { font-size: 30px; text-align: center; margin-bottom: 10px; }
.result-card h3 { margin: 5px 0; color: #111; text-align: center; }
.tagline { font-style: italic; color: #4f46e5; font-weight: 500; text-align: center; margin-bottom: 15px; }
.description { color: #444; font-size: 14px; line-height: 1.6; }
.btn-group { display: flex; gap: 10px; margin-top: 15px; }
.btn-copy { background: #22c55e; }
.btn-copy:hover { background: #16a34a; }
.btn-reset { background: #3b82f6; }
.btn-reset:hover { background: #2563eb; }const GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"; // உங்கள் API Key-ஐ இங்கே போடுங்கள்

async function generateProductCard() {
    const inputVal = document.getElementById("productInput").value;
    const btn = document.getElementById("generateBtn");
    
    if (!inputVal) {
        alert("தயவுசெய்து ஒரு ஐடியாவை டைப் செய்யவும்!");
        return;
    }
    
    btn.innerText = "GENERATING...";
    btn.disabled = true;
    
    // AI-யிடம் இருந்து நமக்குத் தேவையான வடிவில் பதிலை கேட்கும் Prompt
    const promptText = `I am making a product named "${inputVal}". Generate an awesome marketing card for it. 
    Provide the response strictly in this format:
    Title: [Catchy Brand Name]
    Tagline: "[Short Catchy Tagline]"
    Description: [2-3 sentences of persuasive product description]`;

    try {
        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_API_KEY}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ contents: [{ parts: [{ text: promptText }] }] })
        });
        
        const data = await response.json();
        const aiResponse = data.candidates[0].content.parts[0].text;
        
        // பதிலைப் பிரித்து கார்டில் காட்டுதல்
        const titleMatch = aiResponse.match(/Title:\s*(.*)/);
        const taglineMatch = aiResponse.match(/Tagline:\s*(.*)/);
        const descMatch = aiResponse.match(/Description:\s*([\s\S]*)/);
        
        document.getElementById("resTitle").innerText = titleMatch ? titleMatch[1] : inputVal;
        document.getElementById("resTagline").innerText = taglineMatch ? taglineMatch[1] : "";
        document.getElementById("resDesc").innerText = descMatch ? descMatch[1] : aiResponse;
        
        document.getElementById("resultCard").style.display = "block";
    } catch (error) {
        alert("ஏதோ தவறு நடந்துவிட்டது! API Key சரியாக உள்ளதா என சரிபார்க்கவும்.");
        console.error(error);
    } finally {
        btn.innerText = "GENERATE CARD";
        btn.disabled = false;
    }
}

function copyText() {
    const text = document.getElementById("resDesc").innerText;
    navigator.clipboard.writeText(text);
    alert("விளக்கம் காப்பி செய்யப்பட்டது!");
}

function resetForm() {
    document.getElementById("productInput").value = "";
    document.getElementById("resultCard").style.display = "none";
}
