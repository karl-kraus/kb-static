import data from '../html/js/charts/data/bibl-per-author.json'
import Chart from 'chart.js/auto';

const canvas = document.getElementById('bibl-per-author');
if (!(canvas instanceof HTMLCanvasElement)) {
    throw new Error('Canvas element #bibl-per-author not found');
}


new Chart(
    canvas,
    {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Acquisitions by year',
                    data: data.data
                }
            ]
        }
    }
);

