const API_URL = "http://127.0.0.1:8000/api/v1/query";

// Global Chart Instances (to destroy them before re-rendering)
let lineChartInstance = null;
let barChartInstance = null;

async function submitQuery() {
    const query = document.getElementById('queryInput').value;
    if (!query) return;

    // --- 1. UI RESET ---
    document.getElementById('results').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
    document.getElementById('loading').classList.remove('hidden');
    
    // Interactive Loading Text
    const statusText = document.getElementById('status-text');
    statusText.innerText = "Planner Agent: Dispatching Analysis Tasks...";

    try {
        // --- 2. SEND REQUEST ---
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: query })
        });

        const data = await response.json();

        // Handle explicit backend errors
        if (data.status === "error" || (data.result && data.result.type === "error")) {
            throw new Error(data.result.message || "Unknown error from backend.");
        }

        // --- 3. EXTRACT DATA ---
        // Structure: response -> result -> data -> analysis
        const result = data.result.data; 
        const analysis = result.analysis; 

        // --- 4. RENDER METRICS (The Analytics Grid) ---
        // A. Average
        document.getElementById('valAvg').innerText = analysis.average ?? "N/A";
        
        // B. Net Change (The Fix: No hardcoded %, adds '+' for positive)
        let growthVal = analysis.growth_rate ?? 0;
        let growthSign = growthVal > 0 ? "+" : ""; 
        document.getElementById('valGrowth').innerText = `${growthSign}${growthVal}`;
        
        // C. Min/Max
        document.getElementById('valMin').innerText = analysis.min_value ?? "N/A";
        document.getElementById('valMax').innerText = analysis.max_value ?? "N/A";

        // --- 5. RENDER CITATION BADGE ---
        const datasetLabel = analysis.chart_data && analysis.chart_data.datasets.length > 0 
                             ? analysis.chart_data.datasets[0].label 
                             : "Data";
        document.getElementById('sourceBadge').innerText = `${result.source} [${datasetLabel}]`;

        // --- 6. RENDER NARRATIVE ---
        // Uses Marked.js to turn Markdown (##, **) into HTML
        document.getElementById('narrativeText').innerHTML = marked.parse(result.narrative);

        // --- 7. RENDER DUAL CHARTS ---
        renderLineChart(analysis.chart_data);
        renderBarChart(analysis.summary_chart_data);

        // --- 8. REVEAL UI ---
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('results').classList.remove('hidden');

    } catch (err) {
        document.getElementById('loading').classList.add('hidden');
        const errorDiv = document.getElementById('error');
        errorDiv.innerText = `System Error: ${err.message}`;
        errorDiv.classList.remove('hidden');
        console.error("Full Error:", err);
    }
}

// --- CHART 1: TREND LINE ---
function renderLineChart(chartData) {
    const ctx = document.getElementById('lineChart').getContext('2d');
    
    if (lineChartInstance) lineChartInstance.destroy();
    if (!chartData) return;

    lineChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: chartData.datasets.map(ds => ({
                ...ds,
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                tension: 0.3, // Smooth curves
                borderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                // THE FIX: Show Legend so user knows what lines represent
                legend: { 
                    display: true, 
                    position: 'top',
                    labels: { color: '#94a3b8', font: { size: 11 } }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: '#1e293b',
                    titleColor: '#e2e8f0',
                    bodyColor: '#e2e8f0',
                    borderColor: '#334155',
                    borderWidth: 1
                }
            },
            scales: {
                y: { 
                    grid: { color: '#334155' }, 
                    ticks: { color: '#94a3b8' },
                    beginAtZero: false
                },
                x: { 
                    grid: { display: false }, 
                    ticks: { color: '#94a3b8' } 
                }
            }
        }
    });
}

// --- CHART 2: COMPARISON BAR (NEW) ---
function renderBarChart(chartData) {
    // If no summary data exists, just return (prevents crash on single-point data)
    if (!chartData) return;
    
    const ctx = document.getElementById('barChart').getContext('2d');
    if (barChartInstance) barChartInstance.destroy();

    // Custom colors for bars
    const barColors = ["#6366f1", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"];

    barChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartData.labels, // Country Names
            datasets: [{
                label: 'Period Average',
                data: chartData.datasets[0].data,
                backgroundColor: barColors,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }, // Bars are labeled on X-axis
                tooltip: {
                    backgroundColor: '#1e293b',
                    titleColor: '#e2e8f0',
                    bodyColor: '#e2e8f0'
                }
            },
            scales: {
                y: { 
                    grid: { color: '#334155' }, 
                    ticks: { color: '#94a3b8' },
                    beginAtZero: true 
                },
                x: { 
                    grid: { display: false }, 
                    ticks: { color: '#94a3b8', font: { size: 10 } } 
                }
            }
        }
    });
}

// Allow "Enter" key to submit
document.getElementById("queryInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        submitQuery();
    }
});