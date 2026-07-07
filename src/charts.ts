import biblPerAuthors from './data/bibl-per-author.json'
import authorsPerDecade from './data/authors-decade.json'
import biblPerPlaces from './data/bibl-per-place.json'
import biblPerYears from './data/bibl-per-year.json'
import biblPerOrgs from './data/bibl-per-org.json'
import Chart from 'chart.js/auto';
import zoomPlugin from 'chartjs-plugin-zoom';

type SimpleChartPayload = {
    labels: Array<string | number>;
    data: number[];
};

type AuthorsPerDecadeSeries = {
    label: string;
    data: number[];
};

type AuthorsPerDecadePayload = {
    labels: number[];
    data: AuthorsPerDecadeSeries[];
};

type ChartPayload = SimpleChartPayload | AuthorsPerDecadePayload;

Chart.register(zoomPlugin);
const container = document.getElementById("chartCanvas");
if (!container) throw new Error("chartCanvas element not found");
const data: Record<string, ChartPayload> = {
    biblPerAuthors,
    biblPerPlaces,
    biblPerYears,
    biblPerOrgs,
    authorsPerDecade,
};
const titles: Record<string, string> = {
    biblPerAuthors: "Anzahl der Texte pro Autor",
    biblPerPlaces: "Anzahl der Texte pro Ort",
    biblPerYears: "Anzahl der Texte pro Jahr",
    biblPerOrgs: "Anzahl der Texte pro Verlag",
    authorsPerDecade: "Produktivste Forschende pro Jahrzehnt (Anzahl Publikationen pro Dekade)"
};
const h2_classes = ["text-center", "pt-2"]
const button_classes = ["btn", "btn-outline-primary", "d-block", "mx-auto", "mb-3"]
for (const [x, cur_data] of Object.entries(data)) {
    let canvas = document.createElement('canvas')
    canvas.id = x
    let heading = document.createElement('h2')
    heading.textContent = titles[x]
    heading.classList.add(...h2_classes)
    let button = document.createElement('button')
    button.textContent = "Zoom zurücksetzen"
    button.id = `${x}-resetButton`
    button.classList.add(...button_classes)
    container.append(heading)
    container.append(button)
    container.append(canvas)
    const datasets = x === 'authorsPerDecade'
        ? (cur_data as AuthorsPerDecadePayload).data.map((series) => ({
            label: series.label,
            data: series.data,
        }))
        : [
            {
                label: 'Texte',
                data: (cur_data as SimpleChartPayload).data,
            },
        ]
    let cur_chart = new Chart(
        canvas,
        {
            type: 'bar',
            data: {
                labels: cur_data.labels.map(String),
                datasets
            },
            options: {
                plugins: {
                    zoom: {
                        zoom: {
                            wheel: {
                                enabled: true,
                            },
                            pinch: {
                                enabled: true
                            },
                            mode: 'x',
                        }
                    }
                }
            }
        }
    );
    button.addEventListener('click', () => {
        if (cur_chart) {
            cur_chart.resetZoom();
        }
    });
}


