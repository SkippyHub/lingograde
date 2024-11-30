# lingograde
lingo grade, grades your speech, identifies issues, and enhances language skills to become a native speaker.

#features
#recording
- record from microphone
- record from file
- record from youtube

##grading skills 
grades in a star graph, provide a prompt to read and analyze your speech.
it will grade your speech and provide a star graph with the grade.
a gauge on the certification level you are at.

###speech
- pronunciation 
how well you pronounce the words
- fluency
how well you speak fluent, your melody is 
- Coherence
how well you speak coherent, your ideas are clear. 
- grammar
how well you speak grammatically correct.
- vocabulary 
how diverse your vocabulary is.

###certification
- CEFR scale grade.
a scale grade of your english level. according to the CEFR scale. 
A1, A2, B1, B2, C1, C2
- IELTS scale grade.
a scale grade of your english level. according to the IELTS scale. from 1 to 9.


##goals MVP challenge
### MVP 1
- record from microphone
- grading skills
- star graph

### MVP 2
- certification

##stack
- python
- docker
- streamlit
- gemma  

##packages
- whisper (audio to text)
- gemma 2 (text to text)
- langchain (chaining models)
- dotenv (env variables)
- ffmpeg (audio processing)
- numpy (audio processing)
- pandas (audio processing)


##Additional Packages
- librosa (advanced audio analysis)
- pyDictionary (vocabulary enhancement)
- spaCy (NLP processing)
- pytest (testing framework)


## Development

1. Clone and install dependencies:

```bash
git clone https://github.com/skippyhub/lingograde.git
cd lingograde
pip install -r requirements.txt
```

2. Run locally:

```bash
streamlit run app/main.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines.

## Deployment

Run with Docker:
```bash
docker build -t lingograde .
docker run -p 8501:8501 lingograde
```



