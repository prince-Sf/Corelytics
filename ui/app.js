// CONFIGURATION 

const API = "http://127.0.0.1:8000"

let state = {
    domain: null,
    recipient: null,
    category: null,
    scenario: null
}

let isLoading = false
let scenarioRequired = false

//  DOM ELEMENTS 

const domainBox = document.getElementById("domainOptions")
const recipientBox = document.getElementById("recipientOptions")
const categoryBox = document.getElementById("categoryOptions")
const scenarioBox = document.getElementById("scenarioOptions")

const intentPath = document.getElementById("intentPath")
const generateBtn = document.getElementById("generateBtn")
const copyBtn = document.getElementById("copyBtn")
const output = document.getElementById("emailOutput")

// Step indicators
const step1 = document.getElementById("step1")
const step2 = document.getElementById("step2")
const step3 = document.getElementById("step3")
const step4 = document.getElementById("step4")

const scenarioSection = document.getElementById("scenarioSection")

// LOGGING 

const logger = {
    log: (msg, data) => {
        console.log(`%c[INFO] ${msg}`, 'color: #22c55e; font-weight: bold;', data || "")
    },
    error: (msg, error) => {
        console.error(`%c[ERROR] ${msg}`, 'color: #ef4444; font-weight: bold;', error || "")
    },
    warn: (msg, data) => {
        console.warn(`%c[WARN] ${msg}`, 'color: #f59e0b; font-weight: bold;', data || "")
    }
}

// MOUSE GLOW 

document.addEventListener("mousemove", e => {
    document.body.style.setProperty("--x", e.clientX + "px")
    document.body.style.setProperty("--y", e.clientY + "px")
})

// NOTIFICATIONS 

function showError(message) {
    logger.error("Notification", message)
    const errorDiv = document.createElement("div")
    errorDiv.className = "error-notification"
    errorDiv.textContent = message
    document.body.appendChild(errorDiv)
    
    setTimeout(() => {
        errorDiv.classList.add("show")
    }, 100)
    
    setTimeout(() => {
        errorDiv.classList.remove("show")
        setTimeout(() => errorDiv.remove(), 300)
    }, 4000)
}

function showSuccess(message) {
    logger.log("Notification", message)
    const successDiv = document.createElement("div")
    successDiv.className = "success-notification"
    successDiv.textContent = message
    document.body.appendChild(successDiv)
    
    setTimeout(() => {
        successDiv.classList.add("show")
    }, 100)
    
    setTimeout(() => {
        successDiv.classList.remove("show")
        setTimeout(() => successDiv.remove(), 300)
    }, 3000)
}

// LOADING STATE 

function setLoading(loading) {
    isLoading = loading
    generateBtn.disabled = loading || !canGenerate()
    generateBtn.textContent = loading ? "⏳ Generating..." : "Generate Email"
}

function canGenerate() {
    // Can generate if domain, recipient, category are selected
    // Scenario is optional
    return state.domain && state.recipient && state.category
}

//  STEP INDICATORS 

function updateSteps() {
    step1.classList.toggle("active", state.domain !== null)
    step2.classList.toggle("active", state.recipient !== null)
    step3.classList.toggle("active", state.category !== null)
    step4.classList.toggle("active", state.scenario !== null)
}

//  DOMAIN 

async function loadDomains() {
    try {
        logger.log("Loading domains from API")
        const res = await fetch(`${API}/domains`)
        
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}: ${res.statusText}`)
        }
        
        const data = await res.json()
        
        if (!data.data || !Array.isArray(data.data)) {
            throw new Error("Invalid response format")
        }
        
        logger.log("Domains loaded", data.data)
        
        domainBox.innerHTML = ""
        
        data.data.forEach(d => {
            const b = createBubble(d, (evt) => {
                domainBox.querySelectorAll(".bubble").forEach(bubble => {
                    bubble.classList.remove("selected")
                })
                evt.target.classList.add("selected")
                
                state.domain = d
                state.recipient = null
                state.category = null
                state.scenario = null
                
                logger.log("Domain selected", d)
                updateIntent()
                updateSteps()
                
                loadRecipients()
            })
            domainBox.appendChild(b)
        })
    } catch (error) {
        logger.error("Error loading domains", error)
        showError("Failed to load domains: " + error.message)
    }
}

// RECIPIENT 

async function loadRecipients() {
    if (!state.domain) {
        logger.warn("loadRecipients called without domain selected")
        return
    }
    
    try {
        logger.log("Loading recipients", `domain: ${state.domain}`)
        const url = `${API}/recipients?domain=${encodeURIComponent(state.domain)}`
        const res = await fetch(url)
        
        if (!res.ok) {
            const errorData = await res.json()
            throw new Error(errorData.detail || `HTTP ${res.status}`)
        }
        
        const data = await res.json()
        
        if (!data.data || !Array.isArray(data.data)) {
            throw new Error("Invalid response format")
        }
        
        logger.log("Recipients loaded", data.data)
        
        recipientBox.innerHTML = ""
        document.getElementById("recipientSection").classList.add("active")
        
        data.data.forEach(r => {
            const b = createBubble(r, (evt) => {
                recipientBox.querySelectorAll(".bubble").forEach(bubble => {
                    bubble.classList.remove("selected")
                })
                evt.target.classList.add("selected")
                
                state.recipient = r
                state.category = null
                state.scenario = null
                
                logger.log("Recipient selected", r)
                updateIntent()
                updateSteps()
                
                loadCategories()
            })
            recipientBox.appendChild(b)
        })
    } catch (error) {
        logger.error("Error loading recipients", error)
        showError("Failed to load recipients: " + error.message)
    }
}

//  CATEGORY 

async function loadCategories() {
    if (!state.domain || !state.recipient) {
        logger.warn("loadCategories called without required fields")
        return
    }
    
    try {
        logger.log("Loading categories", `domain: ${state.domain}, recipient: ${state.recipient}`)
        const url = `${API}/categories?domain=${encodeURIComponent(state.domain)}&recipient=${encodeURIComponent(state.recipient)}`
        const res = await fetch(url)
        
        if (!res.ok) {
            const errorData = await res.json()
            throw new Error(errorData.detail || `HTTP ${res.status}`)
        }
        
        const data = await res.json()
        
        if (!data.data || !Array.isArray(data.data)) {
            throw new Error("Invalid response format")
        }
        
        logger.log("Categories loaded", data.data)
        
        categoryBox.innerHTML = ""
        document.getElementById("categorySection").classList.add("active")
        
        data.data.forEach(c => {
            const b = createBubble(c, (evt) => {
                categoryBox.querySelectorAll(".bubble").forEach(bubble => {
                    bubble.classList.remove("selected")
                })
                evt.target.classList.add("selected")
                
                state.category = c
                state.scenario = null
                
                logger.log("Category selected", c)
                updateIntent()
                updateSteps()
                
                loadScenarios()
            })
            categoryBox.appendChild(b)
        })
    } catch (error) {
        logger.error("Error loading categories", error)
        showError("Failed to load categories: " + error.message)
    }
}

// SCENARIO 

async function loadScenarios() {
    if (!state.domain || !state.recipient || !state.category) {
        logger.warn("loadScenarios called without required fields")
        return
    }
    
    try {
        logger.log("Loading scenarios", `domain: ${state.domain}, recipient: ${state.recipient}, category: ${state.category}`)
        const url = `${API}/scenarios?domain=${encodeURIComponent(state.domain)}&recipient=${encodeURIComponent(state.recipient)}&category=${encodeURIComponent(state.category)}`
        const res = await fetch(url)
        
        if (!res.ok) {
            const errorData = await res.json()
            throw new Error(errorData.detail || `HTTP ${res.status}`)
        }
        
        const data = await res.json()
        
        if (!data.data || !Array.isArray(data.data)) {
            throw new Error("Invalid response format")
        }
        
        logger.log("Scenarios loaded", data.data)
        logger.log("Has scenarios?", data.hasScenarios)
        
        scenarioBox.innerHTML = ""
        
        if (data.hasScenarios && data.data.length > 0) {
            scenarioRequired = true
            scenarioSection.classList.add("active")
            
            data.data.forEach(s => {
                const b = createBubble(s, (evt) => {
                    scenarioBox.querySelectorAll(".bubble").forEach(bubble => {
                        bubble.classList.remove("selected")
                    })
                    evt.target.classList.add("selected")
                    
                    state.scenario = s
                    
                    logger.log("Scenario selected", s)
                    updateIntent()
                    updateSteps()
                    
                    generateBtn.disabled = false
                })
                scenarioBox.appendChild(b)
            })
        } else {
            scenarioRequired = false
            scenarioSection.classList.remove("active")
            state.scenario = null
            
            logger.log("⚠ No scenarios available - using category as scenario")
            showSuccess("✓ No sub-scenarios needed - ready to generate!")
            
            generateBtn.disabled = false
            updateSteps()
        }
        
        updateIntent()
    } catch (error) {
        logger.error("Error loading scenarios", error)
        showError("Failed to load scenarios: " + error.message)
    }
}

// GENERATE 

generateBtn.addEventListener("click", async () => {
    if (!state.domain || !state.recipient || !state.category) {
        showError("Please select domain, recipient, and category before generating")
        return
    }
    
    setLoading(true)
    
    try {
        logger.log("Generating email with state", state)
        
        const res = await fetch(`${API}/generate`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                domain: state.domain,
                recipient: state.recipient,
                category: state.category,
                scenario: state.scenario || null
            })
        })
        
        if (!res.ok) {
            const errorData = await res.json()
            throw new Error(errorData.detail || `HTTP Error: ${res.status}`)
        }
        
        const data = await res.json()
        
        if (!data.email) {
            throw new Error("No email content received")
        }
        
        output.value = data.email
        logger.log("Email generated successfully")
        logger.log("Metadata", data.metadata)
        showSuccess("✓ Email generated successfully!")
        
    } catch (error) {
        logger.error("Error generating email", error)
        showError("Failed to generate email: " + error.message)
        output.value = ""
    } finally {
        setLoading(false)
    }
})

// COPY TO CLIPBOARD 

copyBtn.addEventListener("click", async () => {
    if (!output.value) {
        showError("No email to copy")
        return
    }
    
    try {
        await navigator.clipboard.writeText(output.value)
        logger.log("Email copied to clipboard")
        showSuccess("✓ Email copied to clipboard!")
        
        const originalText = copyBtn.textContent
        copyBtn.textContent = "✓ Copied!"
        setTimeout(() => {
            copyBtn.textContent = originalText
        }, 2000)
    } catch (error) {
        logger.error("Error copying to clipboard", error)
        showError("Failed to copy: " + error.message)
    }
})

// UI UTILITIES 

function createBubble(text, clickHandler) {
    const b = document.createElement("div")
    b.className = "bubble"
    b.textContent = text
    b.addEventListener("click", clickHandler)
    return b
}

function updateIntent() {
    const parts = [
        state.domain,
        state.recipient,
        state.category,
        state.scenario
    ].filter(Boolean)
    
    intentPath.textContent = parts.length > 0 ? parts.join(" → ") : "None selected"
}

// INITIALIZATION 

window.addEventListener("load", () => {
    logger.log("🚀 Corelytics App Initialized")
    logger.log("📡 API URL", API)
    loadDomains()
})

window.addEventListener("beforeunload", () => {
    logger.log("👋 Page unloading")
})