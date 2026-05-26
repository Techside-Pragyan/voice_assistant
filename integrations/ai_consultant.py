import openai
from config.settings import OPENAI_API_KEY, ASSISTANT_NAME
from utils.memory import memory

class AIConsultant:
    def __init__(self):
        self.client = None
        if OPENAI_API_KEY and "your_" not in OPENAI_API_KEY:
            self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        self.conversation_history = [
            {"role": "system", "content": f"You are AURA (Artificial User Responsive Agent), a high-tier AI assistant. You have full control over the user's desktop environment. You are proactive, brilliant, and extremely concise. Memory: {memory.get('user_name', 'User')} is your primary operator."}
        ]

    def ask_stream(self, question):
        """
        Ultra-fast streaming response. Yields sentences as they are generated.
        """
        # FREE FALLBACK AI if no OpenAI Key is present
        if not self.client:
            try:
                from ddgs import DDGS
                with DDGS() as ddgs:
                    # Fallback to web search summary since free chat API is deprecated
                    results = list(ddgs.text(question, max_results=1))
                    if results:
                        yield f"Here is what I found on the web: {results[0]['body']}"
                    else:
                        yield "I don't have an answer for that right now. Please add an OpenAI key for full conversational abilities."
            except ImportError:
                yield "DuckDuckGo search library is missing."
            except Exception as e:
                yield "I am operating without an AI brain. Please add your OpenAI key to the .env file."
            return
            
        try:
            self.conversation_history.append({"role": "user", "content": question})
            
            # Keep context very short for speed
            if len(self.conversation_history) > 5:
                self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-4:]

            response = self.client.chat.completions.create(
                model="gpt-4o-mini", # Faster and smarter than 3.5
                messages=self.conversation_history,
                max_tokens=200,
                stream=True # Enable streaming
            )
            
            full_answer = ""
            current_sentence = ""
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_answer += content
                    current_sentence += content
                    
                    if any(punct in content for punct in ['.', '!', '?', '\n', ',']):
                        if len(current_sentence.strip()) > 10 or '.' in content: 
                            yield current_sentence.strip()
                            current_sentence = ""

            if current_sentence.strip():
                yield current_sentence.strip()
                
            self.conversation_history.append({"role": "assistant", "content": full_answer})
        except Exception as e:
            yield f"I had a small glitch: {e}"

    def ask(self, question):
        # Compatibility wrapper
        return "".join(list(self.ask_stream(question)))

# Singleton instance
ai_consultant = AIConsultant()
