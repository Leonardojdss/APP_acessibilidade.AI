import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import base64
import os
from gtts import gTTS
from streamlit_option_menu import option_menu

# Carrega as variáveis de ambiente
load_dotenv()

# Imagem de exemplo em base64
def convert_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        return image_base64

# Instancia o cliente da OpenAI
def analize_image(image, prompt):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{prompt}"},
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

    st.markdown("<h1 style='text-align: center;'>Acessibilidade.AI</h1>", unsafe_allow_html=True)

    menu = option_menu(None, 
        ["Deficiências visuais", "Deficiências de ouvir"], 
        icons=["eyeglasses", "ear"], 
        menu_icon="cast", 
        default_index=0, 
        orientation="horizontal") 

    if menu == "Deficiências visuais":

        selectbox = st.tabs(
            ["Reconhecimento de cores", "Reconhecimento de objetos", "Leitura de documentos"]
        )

        # Funcionalidade - De identificar as cores da roupa
        with selectbox[0] as tab:

            #Audio explicando para que serve essa função de identificar as cores
            audio_explain = gTTS(text="Olá, essa funcionalidade tem como objetivo identificar\
                as cores da roupa da sua roupa ou as cores do objeto que você queira. Para isso, você deve tirar uma foto. \
                ou enviar uma imagem no formato jpeg", lang='pt', slow=False)
            
            arquivo_audio_explain = "explicacao_cores.mp3"
            audio_explain.save(arquivo_audio_explain)

            audio_file_explain = open(arquivo_audio_explain, "rb")
            audio_bytes_explain = audio_file_explain.read()
            st.audio(audio_bytes_explain, format="audio/mp3", 
                     #autoplay=True
                     )

            os.remove(arquivo_audio_explain)

            # Adicionar imagem
            image_temp = st.file_uploader("Escolha uma imagem jpg", type=["jpeg","png"], key="file_uploader_objetos") or st.camera_input(label="Ou tire uma foto", key="camera_input_objetos")

            if image_temp is not None:
                image_path = f"/tmp/{image_temp.name}"
                with open(image_path, "wb") as f:
                    f.write(image_temp.getbuffer())

                prompt="Você é um copiloto para pessoas com deficiência visual, você deve ajudar as pessoas com essa deficiencia\
                    a identificar a roupa que ela esta usando ou as cores do objeto que ela esta mostrando para você, pode ser sua roupa\
                    ou qualquer objeto que ela queira identificar as cores, sempre responda como se estivessem conversando com ela, você esta\
                    uma roupa com a cor X,Y ou Z ou o objeto que você esta mostrando é da cor X,Y ou Z"

                image_base64 = convert_image_base64(image_path)
                return_analyze = analize_image(image_base64, prompt)

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
            
                # Remove arquivo de imagem
                os.remove(image_path)  

        # Funcionalidade - reconhecimento de objetos
        with selectbox[1] as tab:
            
            #Audio explicando para que serve essa função de identificar os objetos
            audio_explain = gTTS(text="Olá, essa funcionalidade tem como objetivo identificar\
                os objetos, então aponte a camera do celular para o objeto ou envie a foto deste objeto", lang='pt', slow=False)
            
            arquivo_audio_explain = "explicacao_objeto.mp3"
            audio_explain.save(arquivo_audio_explain)

            audio_file_explain = open(arquivo_audio_explain, "rb")
            audio_bytes_explain = audio_file_explain.read()
            st.audio(audio_bytes_explain, format="audio/mp3", 
                     #autoplay=True
                     )

            os.remove(arquivo_audio_explain)

            # Adicionar imagem
            image_temp = st.file_uploader("Escolha uma imagem jpg", type=["jpeg","png"], key="file_uploader_documentos") or st.camera_input(label="Ou tire uma foto", key="camera_input_documentos")

            if image_temp is not None:
                image_path = f"/tmp/{image_temp.name}"
                with open(image_path, "wb") as f:
                    f.write(image_temp.getbuffer())

                prompt="Você é um copiloto para pessoas com deficiência visual, você deve ajudar as pessoas com essa deficiencia\
                    a identificar a identificar o objeto que ela enviando na foto, sempre responda como se estivessem conversando com ela, você esta\
                    você esta vendo um objeto X ou Y ou Z e ele tem tais caracteristicas, seja objetivo na resposta"

                image_base64 = convert_image_base64(image_path)
                return_analyze = analize_image(image_base64, prompt)

                st.markdown(return_analyze)

                # Converter o texto em áudio
                text_for_audio = return_analyze
                audio = gTTS(text=text_for_audio, lang='pt', slow=False)

                arquivo_audio = "descricao_objeto.mp3"
                audio.save(arquivo_audio)

                # Reproduzir o áudio no Streamlit
                audio_file = open(arquivo_audio, "rb")
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3", autoplay=True)

                # Remover arquivo de áudio
                os.remove(arquivo_audio)
            
                # Remove arquivo de imagem
                os.remove(image_path)  

        # Funcionalidade - leitura de documentos
        with selectbox[2] as tab:

            #Audio explicando para que serve essa função de leitura de documentos
            audio_explain = gTTS(text="Olá, essa funcionalidade tem como objetivo realizar a leitura\
                dos seus documentos, então aponte a camera do celular para o documento e tire uma foto \
                ou envie a foto ou arquivo pdf do seu documento", 
                lang='pt', slow=False)
            
            arquivo_audio_explain = "explicacao_documento.mp3"
            audio_explain.save(arquivo_audio_explain)

            audio_file_explain = open(arquivo_audio_explain, "rb")
            audio_bytes_explain = audio_file_explain.read()
            st.audio(audio_bytes_explain, format="audio/mp3", 
                     #autoplay=True
                     )

            os.remove(arquivo_audio_explain)

            # Adicionar imagem
            image_temp = st.file_uploader("Escolha uma imagem jpg", type=["jpeg","png"]) or st.camera_input(label="Ou tire uma foto")

            if image_temp is not None:
                image_path = f"/tmp/{image_temp.name}"
                with open(image_path, "wb") as f:
                    f.write(image_temp.getbuffer())

                prompt="Você é um copiloto para pessoas com deficiência visual, você deve ajudar as pessoas com essa deficiência\
                    a ler o documento que ela está enviando na foto, sempre responda como se estivesse conversando com ela.\
                    Você está vendo um documento com o seguinte conteúdo: X, Y ou Z. Seja objetivo na resposta e leia\
                    tudo que estiver no documento."

                image_base64 = convert_image_base64(image_path)
                return_analyze = analize_image(image_base64, prompt)

                st.markdown(return_analyze)

                # Converter o texto em áudio
                text_for_audio = return_analyze
                audio = gTTS(text=text_for_audio, lang='pt', slow=False)

                arquivo_audio = "descricao_objeto.mp3"
                audio.save(arquivo_audio)

                # Reproduzir o áudio no Streamlit
                audio_file = open(arquivo_audio, "rb")
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3", autoplay=True)

                # Remover arquivo de áudio
                os.remove(arquivo_audio)
            
                # Remove arquivo de imagem
                os.remove(image_path)

    if menu == "Deficiências de ouvir":
        st.write('🚧 Em construção 🚧')
