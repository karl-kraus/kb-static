import data from '../html/js/charts/data/bibl-per-author.json'
import Chart from 'chart.js/auto';

const canvas = document.getElementById('biblPerAuthors');
if (!(canvas instanceof HTMLCanvasElement)) {
    throw new Error('Canvas element #biblPerAuthors not found');
}


new Chart(
    canvas,
    {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Texts',
                    data: data.data
                }
            ]
        }
    }
);

