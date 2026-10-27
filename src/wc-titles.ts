import Chart from 'chart.js/auto';
import { WordCloudController, WordElement } from 'chartjs-chart-wordcloud';
import words from './data/wc-titles.json';

type WordEntry = { key: string; value: number };

Chart.register(WordCloudController, WordElement);

const container = document.getElementById('visContainer');
if (!container) throw new Error('visContainer element not found');

container.style.height = '80vh';
container.style.minHeight = '600px';
container.style.position = 'relative';

const entries = words as WordEntry[];
const maxValue = Math.max(...entries.map((w) => w.value));
const minSize = 12;
const maxSize = 80;

const canvas = document.createElement('canvas');
canvas.id = 'wcTitles';
container.append(canvas);

new Chart(canvas, {
    type: 'wordCloud',
    data: {
        labels: entries.map((w) => w.key),
        datasets: [
            {
                label: 'Häufigkeit',
                // scale counts to font sizes in px
                data: entries.map((w) => minSize + (w.value / maxValue) * (maxSize - minSize)),
            },
        ],
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: true },
            tooltip: {
                callbacks: {
                    label: (ctx) => `${ctx.label}: ${entries[ctx.dataIndex].value}`,
                },
            },
        },
    },
});
