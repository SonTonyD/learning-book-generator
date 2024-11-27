from llamaapi import LlamaAPI
import json
import extract_chapter as ec

# Replace 'Your_API_Token' with your actual API token
api_token = 'LA-6bd0b23628cf4afc8ca7096f73393c315fe0fe451b554273977c18f2ed67ceda'

llama = LlamaAPI(api_token)

from openai import OpenAI

def test(name) :
    client = OpenAI(
        # This is the default and can be omitted
        api_key=api_token,
        base_url="https://api.llama-api.com"
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Bonjour, je m'appelle " + name,
            }
        ],
        functions = None,
        model="llama3.1-70b",
        max_tokens=50,
        stream=True
    )

    result = "";

    for chunk in chat_completion:
        result += str(chunk.choices[0].delta.content)

    result = result[:-4]
    return result

def generate_outlines(sujet) :
    client = OpenAI(
        # This is the default and can be omitted
        api_key=api_token,
        base_url="https://api.llama-api.com"
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Donne moi un sommaire détaillé en français sur le sujet suivant : "+sujet+". Devant les grands titres de chapitres tu mettra des caractères suivant : '###' , et devant les petites parties tu mettras : '#'.",
            }
        ],
        functions = None,
        model="llama3.1-70b",
        max_tokens=800,
        stream=True
    )

    result = "";

    for chunk in chat_completion:
        result += str(chunk.choices[0].delta.content)

    result = result[:-4]


    print("#################################")
    print("############## SOMMAIRE GENERE ###################")
    print(result)
    print("#################################")
    print("#################################")


    return result

def generate_subsection_content(chapters):
    chapter_contents = []

    client = OpenAI(
        # This is the default and can be omitted
        api_key=api_token,
        base_url="https://api.llama-api.com"
    )

    for chapter in chapters:
        chapter_text = ""

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Dès que tu vois '###' il s'agit d'un titre de chapitre. Si tu vois '#' il s'agit d'une sous-partie. Maintenant, je veux que tu me rédiges chaque sous parties en dessous de son sous-titre respectif (#): "+chapter+". Tu prendras soin à garder mon format avec les # et les ###. Tu ne feras pas de bullet point. Rédiges un bon paragraphe uniquement en dessous de chaque sous partie #, N'écrit pas d'introduction au chapitre. Reviens bien à la ligne après chaque titre de sous partie. N'hésite pas à apporter des exemples de temps à autres.",
                }
            ],
            functions = None,
            model="llama3.1-70b",
            max_tokens=5000,
            stream=True
        )
        
        for chunk in chat_completion:
            chapter_text += str(chunk.choices[0].delta.content)

        chapter_text = chapter_text[:-4]
        chapter_contents.append(str(chapter_text) + str('\n'))

    for chapter_content in chapter_contents:
        print("############## CONTENU DE UN CHAPITRE ##################")
        print(chapter_content)
        print("########################################################")

    return chapter_contents



sujet = "Histoire de la Corée"

def generate_livre(sujet):
    outlines = generate_outlines(sujet)
    chapters = ec.extract_chapters(outlines)
    chapter_contents = generate_subsection_content(chapters)

    with open("output.txt", "w", encoding="utf-8") as file:
        file.write("Sujet: "+sujet+"\n")
        for content in chapter_contents:
            file.write(content+"\n")




