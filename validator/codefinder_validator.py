import re
import os

class SyntaxValidator:
    def __init__(self, regex_file="data/regex.txt"):
        self.regex_data = {}

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(base_dir, regex_file)

        self._load_data()

    def _load_data(self):
        current_language = None

        if not os.path.exists(self.file_path):
            return

        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                if line.startswith("[") and line.endswith("]"):
                    current_language = line[1:-1].upper()
                    self.regex_data.setdefault(current_language, [])
                    continue

                if line == "===END===":
                    current_language = None
                    continue

                if current_language:
                    pattern = line.split("#", 1)[0].strip()
                    if pattern:
                        self.regex_data[current_language].append(pattern)

    def validate(self, text: str, options=None):
        if not text or not isinstance(text, str):
            return {"passed": True, "message": "Invalid input"}

        options = [opt.upper() for opt in (options or [])]

        if not options or "ALL" in options:
            languages_to_check = self.regex_data.keys()
        else:
            languages_to_check = [
                lang for lang in options if lang in self.regex_data
            ]

        for lang in languages_to_check:
            for pattern in self.regex_data.get(lang, []):
                if not pattern or pattern.isspace():
                    continue

                regex = re.compile(pattern, re.MULTILINE)

                if regex.search(text):
                    return {
                        "passed": False,
                        "message": "Syntax pattern detected",
                        "details": {
                            "language": lang,
                            "pattern": pattern
                        }
                    }

        return {
            "passed": True,
            "message": "No syntax pattern detected"
        }

