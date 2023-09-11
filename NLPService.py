from Model import Model
import re

class NLPService(Model):

    def __init__(self, sts_count, top):
        super().__init__()
        self._sts_count = sts_count
        self._top = top


    @staticmethod
    def _Sentences(text: str):
        return re.split(r'[。 ]', text)

    @staticmethod
    def _MakeContext(sts) -> str:
        if len(sts) == 0:
            return None
        return "\n".join([x[1] for x in sts])

    @staticmethod
    def _MakePrompt(context: str, question: str) -> str:
        prompt = context + "\n###\n请根据以上上下文推理以下问题的答案\n###\n" + question
        return prompt

    def ComputeSimilarity(self, text1, text2):
        raise NotImplementedError("this method is not implemented")

    def Chat(self, messages):
        if len(messages) != 2:
            return messages
        text = messages[0]
        question = messages[1]
        sts = NLPService._Sentences(text)
        key_sts = []
        l = len(sts)
        for i in range(0, l, self._sts_count):
            self.Progress(int(i/len(sts)*100))
            left = i
            right = i+self._sts_count if i + \
                    self._sts_count < len(sts) else len(sts)
            t = '\n'.join(sts[left: right])
            rate = self.ComputeSimilarity(t, question)
            self.Log(f"关联度：{rate}\n内容： {t}\n--------------------------------\n")
            if rate == 0:
                continue
            key_sts.append((rate, t, (left, right)))
        self.Progress(100)


        key_sts.sort(key=lambda x: x[0], reverse=True)
        if len(key_sts) > self._top:
            key_sts = key_sts[:self._top]
        key_sts.sort(key=lambda x: x[2][0])
        context = NLPService._MakeContext(key_sts)
        if context is None:
            return None
        prompt = NLPService._MakePrompt(context, question)
        return [prompt]

    def Description(self):
        return "NLP"
