import pandas as pd

# Lees het quant.sf bestand
input_file = "../../voorbeeld_data/quant.sf"
df = pd.read_csv(input_file, sep="\t")

# Selecteer interessante kolummen
selected_columns = ["Name", "TPM"]
df_selected = df[selected_columns]

# Opslaan als JSON
json_output_file = "../../voorbeeld_data/quant.json"
df_selected.to_json(json_output_file, orient="records", indent=4)

print(f'Output geschreven naar: {json_output_file}')

"""
Dit is iets snels wat ik in elkaar heb gegooid om de voorbeeld data te veranderen van bestandstype.
Wellicht kan het later in het project worden gebruikt!
"""