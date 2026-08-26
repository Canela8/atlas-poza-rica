import re

with open('c:/Users/PC/Downloads/atlas-poza-rica-main/atlas-poza-rica-main/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove map.addLayer for specific layers
layers_to_remove = [
    'layer_Otro_6', 'layer_Intermitente_7', 'layer_Directa_8', 'layer_Daado_9', 
    'layer_Bueno_10', 'layer_Apagada_11', 'layer_RiesgoAlto', 'layer_RiesgoMedio', 'layer_RiesgoBajo'
]

for layer in layers_to_remove:
    # replace " map.addLayer(layer_Name);" with ""
    content = re.sub(r'\s*map\.addLayer\(' + layer + r'\);', '', content)

with open('c:/Users/PC/Downloads/atlas-poza-rica-main/atlas-poza-rica-main/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed map.addLayer for infrastructure layers.")
