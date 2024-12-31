import logging
from lintoxic.utils.toxicity import ToxicContentClassifier, TamilToxicContentClassifier

def check_toxicity(text: str):
    toxic_content_classifier = ToxicContentClassifier.get_instance()
    results = toxic_content_classifier.predict(text)
    if results:
        return (True, results)
    toxic_content_classifier = TamilToxicContentClassifier.get_instance()
    results = toxic_content_classifier.predict(text)
    if results:
        return (True, results)
    return (False, "The content is not toxic")