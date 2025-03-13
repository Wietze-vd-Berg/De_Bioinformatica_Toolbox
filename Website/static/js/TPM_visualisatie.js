"Snel in elkaar geflantse code, wellicht kan dit later in het project ook worden gebruikt!"
    "Bron: https://www.createwithdata.com/visualising-data-with-js-getting-started/"

document.addEventListener("DOMContentLoaded", function() { //javascript functie :O
    fetch("../Website/voorbeeld_data/quant.json")
        .then(response => response.json())
        .then(data => {
            console.log("Data geladen:", data); // Debug: controleer of de JSON correct wordt geladen

            // Sorteer op TPM en neem de top 10
            let top10 = data.sort((a, b) => b.TPM - a.TPM).slice(0, 10);

            let labels = top10.map(d => d.Name);
            let values = top10.map(d => d.TPM);

            let ctx = document.getElementById('voorbeeld_chart')?.getContext('2d');

            if (!ctx) { //Als voorbeeld_chart niet kan worden gevonden
                console.error("FOUT: Canvas-element 'voorbeeld_chart' niet gevonden!");
                return;
            }

            new Chart(ctx, { // Maakt de chart
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Voorbeeld: TPM Expressie',
                        data: values,
                        backgroundColor: 'rgba(255, 185, 170, 0.8)',
                        borderColor: 'rgba(250, 128, 114, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }).catch(error => console.error("Fout bij verwerken JSON:", error));
});