from LLM import LLM
from snownlp import SnowNLP

class NLPService(LLM):

    def __init__(self, sts_count, top, step ,need_group=True):
        super().__init__()
        self._sts_count = sts_count
        self._top = top
        self._step = step
        self._need_group = need_group

    @staticmethod
    def _GroupOverlappingSegments(segments: list):
        groups = []
        current_group = []
        segments.sort(key=lambda x: x[2][0])

        # 对每个线段进行遍历
        for segment in segments:
            if not current_group:
                current_group.append(segment)
            else:
                # 判断当前线段是否与当前分组中的线段重叠
                if segment[2][0] < current_group[-1][2][1]:
                    current_group.append(segment)
                else:
                    groups.append(current_group)
                    current_group = [segment]

        if current_group:
            groups.append(current_group)

        return groups

    @staticmethod
    def _Sentences(text: str):
        return SnowNLP(text).sentences

    @staticmethod
    def _MakeContext(sts) -> str:
        if len(sts) == 0:
            return None
        return "\n".join([str(x)+'. '+y[1] for x, y in enumerate(sts)])

    @staticmethod
    def _MakePrompt(context: str, question: str) -> str:
        prompt = context + "\n###\n请仅根据以上上下文推理以下问题的答案\n###\n" + question
        return prompt

    def ComputeCosineSimilarity(self, text1, text2):
        raise NotImplementedError("this method is not implemented")

    def Chat(self, messages):
        if len(messages) != 2:
            return messages
        text = messages[0]
        question = messages[1]
        sts = NLPService._Sentences(text)
        key_sts = []
        l = len(sts)
        for i in range(0, l, self._step):
            self.Progress(int(i/len(sts)*100))
            left = i
            right = i+self._sts_count+1 if i + \
                    self._sts_count+1 < len(sts) else len(sts)
            t = ' '.join(sts[left: right])
            rate = self.ComputeCosineSimilarity(t, question)
            self.Log(f"关联度：{rate}\n内容： {t}\n--------------------------------\n")
            if rate == 0:
                continue
            key_sts.append((rate, t, (left, right)))
        self.Progress(100)

        if self._need_group:
            key_sts = self._GroupOverlappingSegments(key_sts)
            key_sts = [sorted(x, key=lambda t: t[0], reverse=True)[0]
                       for x in key_sts]

        key_sts.sort(key=lambda x: x[0], reverse=True)
        if len(key_sts) > self._top:
            key_sts = key_sts[:self._top]
        context = NLPService._MakeContext(key_sts)
        if context is None:
            return None
        prompt = NLPService._MakePrompt(context, question)
        return [prompt]

    def Description(self):
        return "NLP"
