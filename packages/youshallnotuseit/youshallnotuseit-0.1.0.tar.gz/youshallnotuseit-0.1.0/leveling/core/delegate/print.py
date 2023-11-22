from ...lang import lang
from ..overrider import writeBI


class AnswerChecker:
    __printer = print
    __expected: str

    def __init__(self, answer):
        self.__expected = answer

    @property
    def expected(self):
        return self.__expected

    def print(self, *args, sep=' ', end='\n', file=None, flush=False):
        ans = sep.join(map(str, args)) + end
        if ans.strip() == self.__expected.strip():
            self.__printer(lang["answer.fit"])
            self.__printer(ans, file=file, flush=flush)
        else:
            self.__printer(lang["answer.unfit"])
            self.__printer(lang["answer.expected"], self.expected)
            self.__printer(lang["answer.actual"], ans)

    @staticmethod
    def override(answer: str):
        ac = AnswerChecker(answer)
        writeBI('print', ac)
