# -*- coding: utf-8 -*-
"""Copy of stable-diffusion-with-chatgpt-noteook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fY9ktufiur_iK-7cRmoVCfdEA2HhrvOgj
# Installation
"""

# !pip install -q gradio
# !pip install -q pyChatGPT
# !pip install -q git+https://github.com/openai/whisper.git
# !pip install -q --upgrade git+https://github.com/huggingface/diffusers.git transformers accelerate scipy
# !pip install openai

"""# Imports"""

import whisper
import gradio as gr 
import time
import warnings
import torch
from pyChatGPT import ChatGPT
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler

"""# Defining Variables"""

warnings.filterwarnings("ignore")

import openai
openai.api_key=""

model = whisper.load_model("base")

model.device

"""# Transcribe Function"""

def transcribe(audio):

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)

    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    prompt = result.text

    print(prompt)

    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=(prompt),
    temperature=0,
    max_tokens=2000,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=1
    )

    out_result=response["choices"][0]["text"]

    # out_image = pipe(out_result, height=768, width=768).images[0]

    return [prompt, out_result]

"""# Gradio Interface"""

output_1 = gr.Textbox(label="Speech to Text")
output_2 = gr.Textbox(label="ChatGPT Output")
# output_3 = gr.Image(label="Diffusion Output")

gr.Interface(
    title = 'OpenAI Whisper and ChatGPT ASR Gradio Web UI', 
    fn=transcribe, 
    inputs=[
        gr.inputs.Audio(source="microphone", type="filepath")
    ],

    outputs=[
        output_1,  output_2
    ],
    live=True).launch(share=True)

