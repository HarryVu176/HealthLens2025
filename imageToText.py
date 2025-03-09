import PIL.Image
from PIL import ImageFile
from client import getFormatting, imagePrompt

class ImageToText:
    def __init__(self, format: str, context: str = None):
        self.format = getFormatting(format)
        if context:
            self.prompt = f"Please extract the text from this image into the following json format using this context {context}: {self.format}"
        else:
            self.prompt = f"Please extract the text from this image into the following json format: {self.format}"

    def process(self, image: ImageFile):
        # image = PIL.Image.open(imagePath)
        response = imagePrompt(self.prompt, image)
        return response

class ImageToFacts(ImageToText):
    def __init__(self):
        super(ImageToFacts, self).__init__('label')

class ImageToDoctorsNote(ImageToText):
    def __init__(self, prefferredLanguage):

        context = f"""
        Here are your instructions for processing a doctors note.
        1. Translate this document into {prefferredLanguage}
        2. If the document isn't translatable, just set all fields to null.
        3. Simplify the note into something even a 10 year old could understand.
        4. If no prescriptions are present, don't put any elements in the prescribed array.
        5. If prescriptions are present, add them to the array with the given template
        """
        super(ImageToDoctorsNote, self).__init__('doctornote', context)

if __name__ == "__main__":
    # imgToFacts = ImageToFacts()
    # text = imgToFacts.process('pills.jpg')
    image = PIL.Image.open('docNote2.jpg')
    imgToDoctorNote = ImageToDoctorsNote("english")
    text = imgToDoctorNote.process(image)
    print(text)