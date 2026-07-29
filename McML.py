#Diese Klasse stellt eine einfache Markov-Verkettung da, gewissermaßen den "Urgroßvater" moderner KI
from pypdf import PdfReader
import random
import re #Regular Expression

#Basisklasse für unser Sprachmodell:
class LanguageModel:

    def __init__(self):
        self.text = ""
        #Modell zum Speichern von Wortbeziehungen:
        self.model = {}

    def load_text(self):
        raise NotImplementedError

    def train(self):
        #Erzeugt ein Markov-Modell, das sich für jedes Wort merkt, welche Wörter danach kommen
        if not self.text:
            raise ValueError("Kein Text geladen")
        text = self.text.lower() #optional, da eine Markov-Verkettung Case Sensitive ist
        #Satzzeichen entfernen, da diese sonst als Teil des Wortes gesehen werden. Dafür nutzen wir einen Regex:
        text = re.sub(r"[^\w\s]", "", text)
        words = text.split()  # Wandelt den Text in eine Liste aus Wörtern um
         if len(words) < 2:
             raise ValueError("Text enthält nicht genug Wörter zum Trainieren")
        #Wortbeziehungen erzeugen:
        for i in range(len(words) - 1):
            current_word = words[i]
            next_word = words[i+1]
            if current_word not in self.model:
                self.model[current_word] = []
            self.model[current_word].append(next_word)
            #[ameise][hat][ist][ist][schläft]

    def generate(self, start_word = None, length=50):
        if not self.model:
            raise ValueError("Modell wurde noch nicht trainiert.")
        if start_word == "":
            start_word = random.choice(list(self.model.keys()))
        current_word = start_word.lower()
        result= [current_word]
        for _ in range(length):
            if current_word not in self.model:
                print("Das angegebene Wort konnte nicht gefunden werden. Modell unzureichend trainiert.")
                break
            next_word = random.choice(self.model[current_word])
            result.append(next_word)
            current_word = next_word
        return " ".join(result)

class PDFLanguageModel(LanguageModel):

    def __init__(self, pdf_path):
        super().__init__()
        self.pdf_path = pdf_path

    def load_text(self):
        reader = PdfReader(self.pdf_path)
        pages_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)
        self.text = "\n".join(pages_text)


def main():
    model = PDFLanguageModel("KI-Baum.pdf")
    #PDF laden:
    model.load_text()
    #Modell trainieren:
    model.train()
    print("Hier ist unser generierter Text:")
    text = model.generate(
        #Man könnte hier ein Wort vorgeben. Gibt man keines vor, wird zufällig eines ausgewählt.
        start_word=""
    )
    print(text)

main()
