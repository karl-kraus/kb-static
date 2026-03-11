const ctx = document.getElementById('bibl-by-year');

const dataUrl = 'js/charts/data/bibl-per-year.json'

function renderChart(container, payload) {
    new Chart(container, {
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
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

fetch(dataUrl)
    .then((response) => {
        if (!response.ok) {
            throw new Error(`Failed to load ${dataUrl}: ${response.status} ${response.statusText}`);
        }
        return response.json();
    })
    .then((data) => {
        console.log('Loaded bibliography by year data:', data);
        renderChart(ctx, data);
    })
    .catch((error) => {
        console.error('Error while loading bibliography by year data:', error);
    });
