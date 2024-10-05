# Mappa di domande con le parole chiave attese (Text-Plan) e la struttura della frase (Sentence-Plan)
questions_with_keywords = {
    "What is POS tagging?": {
        'keywords': ['technique', 'disambiguation', 'categories', 'words', 'assigning'],
        'sentence_plan': {
            'subject': 'POS tagging',
            'verb': 'is',
            'object': 'technique',
            'modifiers': ['used for disambiguation', 'assigning them to categories']  # Questo include frasi che contengono le keyword
}



    },
    "What is tokenization in NLP?": {
        'keywords': ['segmenting', 'text', 'words', 'sub-words', 'units'],
        'sentence_plan': {
            'subject': 'tokenization',
            'verb': 'segment',
            'object': 'words',
            'additional_info': ['in NLP']  # Aggiunto per contenere informazioni aggiuntive
        }
    },
    "What are named entity recognitions?": {
        'keywords': ['identify', 'entities', 'names', 'places', 'organizations'],
        'sentence_plan': {
            'subject': 'entity recognition',
            'verb': 'identify',
            'object': 'entities',
            'additional_info': []  # Aggiunto per contenere informazioni aggiuntive
        }
    }
}


