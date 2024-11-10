import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import base64
import os
from gtts import gTTS

# Carrega as variáveis de ambiente
load_dotenv()

# Imagem de exemplo em base64
def convert_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        return image_base64

# Instancia o cliente da OpenAI
def analize_image(image):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Descreva as cores da roupa da pessoa da imagem?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image}",
                        }
                    },
                ],
            }
        ],
    )
    return completion.choices[0].message.content

if __name__ == "__main__":

    st.title('Acessibilidade.AI')

    selectbox = st.tabs(
        ["Reconhecimento de cores", "Reconhecimento de objetos", "Leitura de documentos"]
    )

    # Funcionalidade - De identificar as cores da roupa
    with selectbox[0]:

        #Audio explicando para que serve essa função de identificar as cores
        audio_explain = gTTS(text="Olá, essa funcionalidade tem como objetivo identificar\
            as cores da roupa da sua roupa. Para isso, você deve fazer \
            o upload de uma imagem no formato jpeg ou tirar uma foto.", lang='pt', slow=False)
        
        arquivo_audio_explain = "explicacao_cores.mp3"
        audio_explain.save(arquivo_audio_explain)

        audio_file_explain = open(arquivo_audio_explain, "rb")
        audio_bytes_explain = audio_file_explain.read()
        st.audio(audio_bytes_explain, format="audio/mp3", autoplay=True)

        # Adicionar imagem
        image_temp = st.file_uploader("Escolha uma imagem png", type=["jpeg"]) or st.camera_input(label="Tire uma foto")

        if image_temp is not None:
            image_path = f"/tmp/{image_temp.name}"
            with open(image_path, "wb") as f:
                f.write(image_temp.getbuffer())

            image_base64 = convert_image_base64(image_path)
            return_analyze = analize_image(image_base64)

            st.markdown(return_analyze)

            # Converter o texto em áudio
            text_for_audio = return_analyze
            audio = gTTS(text=text_for_audio, lang='pt', slow=False)

            arquivo_audio = "descricao_roupa.mp3"
            audio.save(arquivo_audio)

            # Reproduzir o áudio no Streamlit
            audio_file = open(arquivo_audio, "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3", autoplay=True)

            # Remover arquivo de áudio
            os.remove(arquivo_audio)
            os.remove(arquivo_audio_explain)
            
            # Remove arquivo de imagem
            os.remove(image_path)  

    # Funcionalidade - reconhecimento de objetos
    with selectbox[1]:
        st.write('Em construção')

    # Funcionalidade - leitura de documentos
    with selectbox[2]:
        st.write('Em construção')
 
