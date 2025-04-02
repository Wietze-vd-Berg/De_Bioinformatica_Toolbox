import matplotlib
matplotlib.use('Agg') # Voorkomt crashes met threads en plots

import matplotlib.pyplot as plt
import numpy as np
import io
import base64

def generate_bar_chart(data_fastq1):
    """
    Genereert een staafgrafiek met TPM-expressie van de top 10 genen.

    :param data_fastq1: Lijst met expressiewaarden van FASTQ 1
    :param data_fastq2: Lijst met expressiewaarden van FASTQ 2
    :return: Base64-encoded afbeelding
    """
    top10 = sorted(data_fastq1, key=lambda x: x['TPM'], reverse=True)[:10]
    labels = [d['Name'] for d in top10]
    values_fastq1 = [d['TPM'] for d in top10]

    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.35
    x = np.arange(len(labels))

    ax.bar(x - bar_width/2, values_fastq1, bar_width, label='FASTQ 1', color='salmon')

    ax.set_xlabel('Genen')
    ax.set_ylabel('TPM Expressie')
    ax.set_title('TPM Expressie Vergelijking (Top 10)')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend()

    # Voeg een ondertitel toe met uitleg
    plt.figtext(0.5, -0.1, "TPM-expressie van de top 10 genen op basis van RNA-sequentieanalyse.",
                wrap=True, horizontalalignment='center', fontsize=10)

    img_io = io.BytesIO()
    plt.savefig(img_io, format='png', bbox_inches='tight')
    plt.close()
    img_io.seek(0)
    bar_chart_data = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return bar_chart_data