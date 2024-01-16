
class FormNotFoundError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class QuestionNotFoundError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
