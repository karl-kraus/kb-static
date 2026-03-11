const ids = [...document.querySelectorAll('[data-chart-type="bar"]')].map(el => el.id);
const base_path = 'js/charts/data/'
const charts = {};

function renderChart(container, payload) {
    const chart = new Chart(container, {
        type: 'bar',
        data: {
            labels: payload.labels,
            datasets:[{
                label: 'Texte',
                data: payload.data,
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                zoom: {
                    pan: {
                        enabled: true,
                        mode: 'x'
                    },
                    zoom: {
                        wheel: {
                            enabled: true
                        },
                        pinch: {
                            enabled: true
                        },
                        mode: 'x'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    charts[container.id] = chart;
}

for (const resetButton of document.querySelectorAll('[data-chart-reset]')) {
    resetButton.addEventListener('click', () => {
        const chart = charts[resetButton.dataset.chartReset];

        if (chart) {
            chart.resetZoom();
        }
    });
}

for (const cur_id of ids) {
    const url = `${base_path}${cur_id}.json`
    
    fetch(url)
    .then((response) => {
        if (!response.ok) {
            throw new Error(`Failed to load ${url}: ${response.status} ${response.statusText}`);
        }
        return response.json();
    })
    .then((data) => {
        renderChart(document.getElementById(cur_id), data);
    })
    .catch((error) => {
        console.error(`Error while loading ${url} data:`, error);
    });
}