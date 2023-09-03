from Document import Document
from NLPService import NLPService
from LLM import LLM

class ApprehendIrisService:

    @staticmethod
    def _MakeContext( sts) -> str:
        if len(sts) == 0:
            return None
        return "\n".join([str(x)+'. '+y[1] for x,y in enumerate(sts)])

    @staticmethod
    def _MakePrompt( context:str, question:str) -> str:
        prompt = context + "\n###\n请仅根据以上上下文推理以下问题的答案\n###" + question
        return prompt

    @staticmethod
    def Ask( llm: LLM, sts:list, question: str) -> str:
        context = ApprehendIrisService._MakeContext(sts)
        if context is None:
            return "从文中没找到这个问题的答案"
        prompt = ApprehendIrisService._MakePrompt(context, question)
        return llm.Request(prompt)

