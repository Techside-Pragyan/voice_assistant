import openai
from config.settings import OPENAI_API_KEY, ASSISTANT_NAME
from utils.memory import memory

class AIConsultant:
    def __init__(self):
        self.client = None
        if OPENAI_API_KEY:
            self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        self.conversation_history = [
            {"role": "system", "content": f"You are AURA, a fast AI assistant. Be concise. User: {memory.get('user_name', 'User')}."}
        ]

    def ask(self, question):
        if not OPENAI_API_KEY or "your_" in OPENAI_API_KEY:
            return "AI brain disconnected. Check .env."
            
        try:
            self.conversation_history.append({"role": "user", "content": question})
            
            # Keep only the last 4 messages for ultra-fast context processing
            if len(self.conversation_history) > 5:
                self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-4:]

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                max_tokens=150
            )
            
            answer = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": answer})
            return answer
        except Exception as e:
            return f"I had a small glitch in my brain: {e}"

# Singleton instance
ai_consultant = AIConsultant()
