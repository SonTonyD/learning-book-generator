def extract_chapters(text: str):
    """
    Divise un texte en une liste de blocs de chapitres basés sur les titres commençant par '###'.
    
    :param text: Le texte d'entrée structuré en chapitres avec '###'.
    :return: Une liste où chaque élément est un bloc de chapitre.
    """
    # Diviser le texte en parties à chaque occurrence de '###' (en excluant la première occurrence vide)
    parts = text.split("###")[1:]
    
    # Ajouter le '###' au début de chaque partie pour conserver le format
    chapters = [f"###{part.strip()}" for part in parts]

    
    print("########## CHAPITREE GENERES ##############")
    # Affichage du résultat
    for i, chapter in enumerate(chapters):
        print(f"Chapitre {i}:\n{chapter}\n")

    print("########################")
    
    return chapters

# Example usage
text = """### Introduction

# Definition and scope of petrochemistry
# Importance of petrochemistry in modern society

### History of Petrochemistry

# Early developments in the field
# Key milestones and discoveries
# Impact of World War II on the development of petrochemistry

### Principles of Petrochemistry

# Chemical reactions and processes involved in petrochemistry
# Thermodynamics and kinetics of petrochemical reactions
# Role of catalysts and reaction conditions

### Petrochemical Processes

# Crude oil refining and processing
# Production of petrochemicals from crude oil
# Examples of petrochemicals produced through refining and processing

### Petrochemical Products

# Plastics and polymers
# Fuels and lubricants
# Chemicals and intermediates
# Other petrochemical products

### Environmental and Health Impacts of Petrochemistry

# Air and water pollution
# Soil contamination
# Health effects of exposure to petrochemicals
# Regulatory efforts to mitigate environmental and health impacts

### Future of Petrochemistry

# Trends and challenges in the industry
# Emerging technologies and innovations
# Sustainability and environmental considerations
# Outlook for the future of petrochemistry

### Conclusion

# Summary of key points
# Importance of petrochemistry in modern society
# Future directions and challenges for the industry(mon_ia_env)"""
