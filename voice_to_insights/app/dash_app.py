import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import base64
import tempfile
import asyncio
from threading import Thread
from pyngrok import ngrok

from app.services.transcription import get_transcription
from app.services.insights import analyze_text
from app.services.sentiment import sentiment_analysis

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    html.H1("Voice-to-Insights Processing System", className="text-center my-4", style={"fontSize": "50px"}),

    dbc.Row([
        dbc.Col([
            dcc.Upload(
                id='upload-audio',
                children=html.Div(['Drag and Drop or ', html.A('Select Audio File')]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center'
                },
                multiple=False
            ),
            dbc.Button("Process Audio", id="process-btn", color="primary", n_clicks=0)
        ], width=6)
    ], justify="center"),

    dbc.Row([
        dbc.Col([
            html.H4("Transcript"),
            dbc.Card(dbc.CardBody(id="transcript-output"))
        ], width=6),

        dbc.Col([
            html.H4("Summary"),
            dbc.Card(dbc.CardBody(id="summary-output")),
            html.H4("Entities"),
            dbc.Card(dbc.CardBody(id="entities-output")),
            html.H4("Actions"),
            dbc.Card(dbc.CardBody(id="actions-output")),
            html.H4("Sentiment"),
            dbc.Card(dbc.CardBody(id="sentiment-output")),
        ], width=6)
    ])
], fluid=True)

@app.callback(
    Output("transcript-output", "children"),
    Output("summary-output", "children"),
    Output("entities-output", "children"),
    Output("actions-output", "children"),
    Output("sentiment-output", "children"),
    Input("process-btn", "n_clicks"),
    State("upload-audio", "contents")
)
def process_audio(n_clicks, audio_contents):
    if n_clicks == 0 or not audio_contents:
        return "", "", "", "", ""

    header, encoded = audio_contents.split(",", 1)
    audio_bytes = base64.b64decode(encoded)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp.write(audio_bytes)
    tmp.close()

    transcript = get_transcription(tmp.name)
    insights = asyncio.run(analyze_text(transcript))
    sentiment = sentiment_analysis(transcript)

    return (
        transcript,
        insights["summary"],
        ", ".join(insights["entities"]),
        "\n".join(insights["actions"]),
        sentiment
    )

def run_dash():
    public_url = ngrok.connect(8050)
    print("Public URL:", public_url)
    app.run(port=8050)

Thread(target=run_dash).start()
