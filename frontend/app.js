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

        if (data.status === "error") {
            throw new Error(data.result.error || "Unknown error");
        }

        // 2. Extract Data
        const result = data.result.data; // The 'data' block from Orchestrator
        
        // 3. Render Narrative
        document.getElementById('narrativeText').innerText = result.narrative;
        
        // 4. Render Metadata
        document.getElementById('sourceTag').innerText = result.source;
        document.getElementById('trendTag').innerText = result.analysis.trend_direction.toUpperCase();

        // 5. Render Chart
        renderChart(result.analysis.chart_data);

        // Show Results
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('results').classList.remove('hidden');

    } catch (err) {
        document.getElementById('loading').classList.add('hidden');
        const errorDiv = document.getElementById('error');
        errorDiv.innerText = `Error: ${err.message}`;
        errorDiv.classList.remove('hidden');
    }
}

function renderChart(chartData) {
    const ctx = document.getElementById('dataChart').getContext('2d');
    
    // Destroy previous chart if exists
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
                borderColor: '#6366f1', // Force our theme color
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                tension: 0.3, // Smooth curves
                borderWidth: 2,
                pointRadius: 4
            }))
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false } // Hide legend for cleaner look
            },
            scales: {
                y: { grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
                x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
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