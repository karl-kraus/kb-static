fetch('js/charts/data/bibl-per-author.json')
    .then((response) => {
        if (!response.ok) {
            throw new Error(`Failed to load 'js/charts/data/bibl-per-author.json': ${response.status} ${response.statusText}`);
        }
        return response.json();
    })
    .then((data) => {
        renderChart(document.getElementById('bibl-by-author'), data);
    })
    .catch((error) => {
        console.error('Error while loading bibliography by author data:', error);
    });
