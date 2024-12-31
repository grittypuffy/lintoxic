import speech_recognition as sr
from transformers import MBartForConditionalGeneration, MBartTokenizer
from lingua import Language, LanguageDetectorBuilder

class AudioProcessor:
    _instance = None

    @staticmethod
    def get_instance(model_name: str):
        if AudioProcessor._instance is None:
            AudioProcessor._instance = AudioProcessor()
        return AudioProcessor._instance


    def __init__(self, model_name: str):
        if AudioProcessor._instance is not None:
            raise Exception("This is a singleton class, use the get_instance() method.")
        self.model = MBartForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = MBartTokenizer.from_pretrained(model_name)
        self.languages = [Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.SPANISH, Language.TAMIL]
        self.language_detector = LanguageDetectorBuilder.from_languages(*languages).build()
        

    @torch.no_grad()
    def predict_language(self, text: str) -> str:
        confidence_value = self.language_detector.compute_language_confidence_values(text)[0]
        if confidence_value is not None:
            return confidence_value.language
        for confidence in confidence_values:
            print(f"{confidence.language.name}: {confidence.value:.2f}")

    def speech_to_text(file):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audiofile) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_text = recognizer.record(source)
            try:
                transcription = recognizer.recognize_google(audio_text)
                return transcription 
            except:
                return "Error Occured"
