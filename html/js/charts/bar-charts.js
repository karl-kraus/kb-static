const ids = [...document.querySelectorAll('[data-chart-type="bar"]')].map(el => el.id);
const base_path = 'js/charts/data/'

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