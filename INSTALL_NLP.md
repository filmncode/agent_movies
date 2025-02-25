# Installing Natural Language Processing Components

This guide will help you set up the Natural Language Processing (NLP) components for the Movie Score application.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation Steps

1. **Install the required packages**

   First, install all the required packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

2. **Install spaCy language model**

   After installing the base packages, you need to download the spaCy language model:

   ```bash
   python -m spacy download en_core_web_sm
   ```

   This will download the small English language model. If you want better accuracy, you can install the medium or large models instead:

   ```bash
   # For medium model (better accuracy, larger size)
   python -m spacy download en_core_web_md

   # For large model (best accuracy, largest size)
   python -m spacy download en_core_web_lg
   ```

3. **Configure the NLP service**

   If you want to use a different language model than the default small one, you'll need to update the `nlp_service.py` file:

   ```python
   # Change this line in src/services/nlp_service.py
   self.nlp = spacy.load('en_core_web_sm')
   
   # To use the medium model instead:
   self.nlp = spacy.load('en_core_web_md')
   
   # Or to use the large model:
   self.nlp = spacy.load('en_core_web_lg')
   ```

## Testing the NLP Component

To test if the NLP component is working correctly, you can run the following command:

```bash
python -c "from src.services.nlp_service import NLPService; nlp = NLPService(); print(nlp.process_message('Tell me about Inception'))"
```

You should see output similar to:

```
('get_info', 'inception')
```

This indicates that the NLP service correctly identified the intent as 'get_info' and extracted 'inception' as the movie title.

## Troubleshooting

If you encounter any issues:

1. **ImportError: No module named 'spacy'**
   
   Make sure you've installed all requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. **OSError: [E050] Can't find model 'en_core_web_sm'**
   
   You need to download the language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **Memory issues with large models**
   
   If you're experiencing memory issues with the medium or large models, switch to the small model:
   ```python
   self.nlp = spacy.load('en_core_web_sm')
   ```

4. **Slow processing times**
   
   The larger models (medium and large) will be slower but more accurate. If speed is a concern, use the small model.

## Customizing the NLP Component

You can customize the NLP component by:

1. **Adding new intent patterns**
   
   Edit the `intent_patterns` dictionary in `nlp_service.py` to add new patterns for existing intents or create new intents.

2. **Improving entity extraction**
   
   Modify the `_extract_potential_movie_title` method to improve how movie titles are extracted.

3. **Enhancing sentiment analysis**
   
   Update the `extract_sentiment` method with more sophisticated sentiment analysis techniques. 