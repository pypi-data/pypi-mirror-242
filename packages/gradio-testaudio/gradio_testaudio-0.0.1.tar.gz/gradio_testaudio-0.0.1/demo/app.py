
import gradio as gr
from gradio_testaudio import TestAudio


example = TestAudio().example_inputs()

demo = gr.Interface(
    lambda x:x,
    TestAudio(),  # interactive version of your component
    TestAudio(),  # static version of your component
    # examples=[[example]],  # uncomment this line to view the "example version" of your component
)


demo.launch()
