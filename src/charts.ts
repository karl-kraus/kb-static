import biblPerAuthors from './data/bibl-per-author.json' 
import biblPerPlaces from './data/bibl-per-place.json' 
import biblPerYears from './data/bibl-per-year.json' 
import biblPerOrgs from './data/bibl-per-org.json'
import Chart from 'chart.js/auto';

const container = document.getElementById("chartCanvas");

const data = {
    biblPerAuthors,
    biblPerPlaces,
    biblPerYears,
    biblPerOrgs
};

for (const [x, cur_data] of Object.entries(data)) {
    let canvas = document.createElement('canvas')
    canvas.id = x
    container.append(canvas)
    new Chart(
        canvas,
        {
            type: 'bar',
            data: {
                labels: cur_data.labels.map(String),
                datasets: [
                    {
                        label: 'Texts',
                        data: cur_data.data
                    }
                ]
            }
        }
    );
}


