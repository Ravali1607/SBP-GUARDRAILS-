import re

class valid_Url:
    def __init__(self, sentence):
        self.sentence = sentence
        self.isValid()

    def isValid(self):
        regex = ("((http|https)://)(www.)?" + "[a-zA-Z0-9@:%._\\+~#?&//=]" + "{2,256}\\.[a-z]" + "{2,6}\\b([-a-zA-Z0-9@:%" + "._\\+~#?&//=]*)")

        if (self.sentence == None):
            return False

        if(re.search(regex, self.sentence)):
            print("Yes, the given URL is valid.")
        else:
            print("No, the given URL is not valid.")


url = input("Enter URL:")
valid_Url(url)

