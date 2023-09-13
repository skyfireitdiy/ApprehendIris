from Model import Model
from snownlp import SnowNLP
import re

class AnswerDistribution:
    Central = 0
    Balanced = 1
    Dispersed = 2


class NLPService(Model):

    def __init__(self, max_sentence = 80, sentence_len=50):
        super().__init__()
        self._max_sentence = max_sentence
        self._sentence_len = sentence_len
        self.answer_distribution = AnswerDistribution.Central

    def SetAnswerDistribution(self, d):
        self.answer_distribution = d

    def _Sentences(self, text: str):
        data = re.split(r'[。\n]', text)
        data = [d for d in data if not re.match(r'^\s$', d)]
        ret = []
        for d in data:
            if len(d) > self._sentence_len:
                ret.extend(SnowNLP(d).sentences)
            else:
                ret.append(d)
        return ret



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
        sts = self._Sentences(text)
        key_sts = []
        l = len(sts)

        if self.answer_distribution == AnswerDistribution.Central:
            sts_count = 40
        elif self.answer_distribution == AnswerDistribution.Balanced:
            sts_count = 20
        else:
            sts_count = 10

        top = self._max_sentence // sts_count
        
        step = sts_count//2
        if step == 0:
            step = 1
        for i in range(0, l, step):
            self.Progress(int(i/len(sts)*100))
            left = i
            right = i+sts_count if i + \
                    sts_count < len(sts) else len(sts)
            t = '\n'.join(sts[left: right])
            rate = self.ComputeSimilarity(t, question)
            self.Log(f"关联度：{rate}\n内容： {t}\n--------------------------------\n")
            if rate == 0:
                continue
            key_sts.append((rate, t, (left, right)))
        self.Progress(100)


        key_sts.sort(key=lambda x: x[0], reverse=True)
        if len(key_sts) > top:
            key_sts = key_sts[:top]
        key_sts.sort(key=lambda x: x[2][0])
        context = NLPService._MakeContext(key_sts)
        if context is None:
            return None
        prompt = NLPService._MakePrompt(context, question)
        return [prompt]

    def Description(self):
        return "NLP"
