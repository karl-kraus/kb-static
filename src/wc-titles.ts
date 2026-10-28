import Chart from 'chart.js/auto';
import { WordCloudController, WordElement } from 'chartjs-chart-wordcloud';
import words from './data/wc-title.json';

type WordEntry = { key: string; value: number };
type DataSource = 'full_titles' | 'titles';

Chart.register(WordCloudController, WordElement);

const container = document.getElementById('visContainer');
if (!container) throw new Error('visContainer element not found');

container.style.height = '80vh';
container.style.minHeight = '600px';
container.style.position = 'relative';

const sourceControls = document.createElement('fieldset');
sourceControls.className = 'mb-3';
const legend = document.createElement('legend');
legend.className = 'fs-5';
legend.textContent = 'Datenquelle';
sourceControls.append(legend);

const dataSources: Array<{ value: DataSource; label: string }> = [
    { value: 'full_titles', label: 'Vollständige Titel' },
    { value: 'titles', label: 'Titel' },
];
const sourceInputs: HTMLInputElement[] = [];
dataSources.forEach(({ value, label }, index) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'form-check form-check-inline';
    const input = document.createElement('input');
    input.className = 'form-check-input';
    input.type = 'radio';
    input.name = 'wc-data-source';
    input.id = `wc-${value}`;
    input.value = value;
    input.checked = index === 0;
    const inputLabel = document.createElement('label');
    inputLabel.className = 'form-check-label';
    inputLabel.htmlFor = input.id;
    inputLabel.textContent = label;
    wrapper.append(input, inputLabel);
    sourceControls.append(wrapper);
    sourceInputs.push(input);
});
container.before(sourceControls);

const minSize = 12;
const maxSize = 80;

let chart: Chart<'wordCloud'> | undefined;

function renderWordCloud(source: DataSource): void {
    const entries = words[source] as WordEntry[];
    const maxValue = Math.max(...entries.map((word) => word.value));
    chart?.destroy();
    container.replaceChildren();

    const canvas = document.createElement('canvas');
    canvas.id = 'wcTitles';
    container.append(canvas);

    chart = new Chart(canvas, {
        type: 'wordCloud',
        data: {
            labels: entries.map((word) => word.key),
            datasets: [
                {
                    label: 'Häufigkeit',
                    data: entries.map((word) => minSize + (word.value / maxValue) * (maxSize - minSize)),
                },
            ],
        },
        options: {
            onClick: (event, elements, chart) => {
            if (!elements.length) return;

            const index = elements[0].index;
            const word = chart.data.labels[index];

            window.location.href = `search.html?kb-static[query]=${encodeURIComponent(word)}`;
        },
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
}

sourceInputs.forEach((control) => {
    control.addEventListener('change', () => {
        if (control.checked) renderWordCloud(control.value as DataSource);
    });
});

renderWordCloud('full_titles');
