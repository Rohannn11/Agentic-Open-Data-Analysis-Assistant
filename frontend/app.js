const API_URL = "http://127.0.0.1:8000/api/v1/query";
let chartInstance = null;

async function submitQuery() {
    const query = document.getElementById('queryInput').value;
    if (!query) return;

    // Reset UI
    document.getElementById('results').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
    document.getElementById('loading').classList.remove('hidden');
    
    // Interactive Loading Text
    const statusText = document.getElementById('status-text');
    statusText.innerText = "Planner Agent: Analyzing Request...";

    try {
        // 1. Send Request
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: query })
        });

        const data = await response.json();

        // Handle potential backend errors explicitly
        if (data.status === "error" || (data.result && data.result.type === "error")) {
            throw new Error(data.result.message || "Unknown error occurred in the backend.");
        }

        // 2. Extract Data
        const result = data.result.data; // The 'data' block from Orchestrator
        const analysis = result.analysis; // Shortcut for easy access

        // 3. Render Key Metrics (The new Analytics Grid)
        // We handle missing data gracefully with "N/A"
        document.getElementById('valAvg').innerText = analysis.average ?? "N/A";
        document.getElementById('valGrowth').innerText = (analysis.growth_rate ?? 0) + "%";
        document.getElementById('valMin').innerText = analysis.min_value ?? "N/A";
        document.getElementById('valMax').innerText = analysis.max_value ?? "N/A";

        // 4. Render Source Citation Badge
        // Combines the API Source (e.g. WORLDBANK) with the Dataset Label for professional context
        const datasetLabel = analysis.chart_data && analysis.chart_data.datasets.length > 0 
                             ? analysis.chart_data.datasets[0].label 
                             : "Unknown Data";
        document.getElementById('sourceBadge').innerText = `${result.source} [${datasetLabel}]`;

        // 5. Render Narrative (Parsed with Marked.js for formatting)
        document.getElementById('narrativeText').innerHTML = marked.parse(result.narrative);

        // 6. Render Chart
        renderChart(analysis.chart_data);

        // Show Results
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('results').classList.remove('hidden');

    } catch (err) {
        document.getElementById('loading').classList.add('hidden');
        const errorDiv = document.getElementById('error');
        errorDiv.innerText = `Error: ${err.message}`;
        errorDiv.classList.remove('hidden');
        console.error("Full Error:", err);
    }
}

function renderChart(chartData) {
    const ctx = document.getElementById('dataChart').getContext('2d');
    
    // Destroy previous chart if exists to prevent "glitching" overlays
    if (chartInstance) {
        chartInstance.destroy();
    }

    if (!chartData) return;

    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: chartData.datasets.map(ds => ({
                ...ds,
                borderColor: '#6366f1', // Force our Indigo theme color
                backgroundColor: 'rgba(99, 102, 241, 0.1)', // Light indigo fill
                tension: 0.3, // Smooth curves (Bezier)
                borderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // Allows chart to fill the container height
            plugins: {
                legend: { display: false }, // Clean look, label is in the header
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

// Allow "Enter" key to submit
document.getElementById("queryInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        submitQuery();
    }
});