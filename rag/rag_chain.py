from .retriever import Retriever
from .llm import LLMService


class RAGChain:
    def __init__(self):
        self.retriever = Retriever()
        self.llm = LLMService()
        self.system_prompt = """
        CRITICAL: Give the SHORTEST possible answer.

            Rules:
            1. If asked "how many", give ONLY the number and unit
            2. If asked "what is the policy", state ONLY the main policy
            3. NEVER mention multiple sources or variations
            4. NEVER say "according to" or "as stated in"
            5. Pick the MOST RELEVANT single answer

            Examples:
            Q: "How many weeks of parental leave?"
            GOOD: "Up to 16 weeks."
            BAD: "16 weeks of parental leave are offered, as stated in Source 2. Some states offer different amounts..."

            Q: "What is the vacation policy?"
            GOOD: "Minimum two weeks (10 days) per year."
            BAD: "According to the policy manual, employees should take a minimum of two weeks..."

            BE EXTREMELY BRIEF.
        """

    def query(self, question, top_k=3, source_filter=None, stream=False):
        # retrieve relevant documents
        retrieved_docs = self.retriever.retrieve(
            query=question, top_k=top_k, source_filter=source_filter
        )

        # format retrieved docs into context
        context = self.retriever.format_context(retrieved_docs)

        # generate answer using llm
        if stream:
            return {
                "answer": self.llm.stream_generate(
                    prompt=question, context=context, system_prompt=self.system_prompt
                ),
                "sources": retrieved_docs,
            }
        else:
            answer = self.llm.generate(
                prompt=question, context=context, system_prompt=self.system_prompt
            )

            return {"answer": answer, "sources": retrieved_docs}
