"""
Fun Chat Agent - Greeter with Tavily Search Integration
Designed for easy deployment as a chat popup in other projects
"""
from openai import AsyncOpenAI
import asyncio
import os
import json
from dotenv import load_dotenv
from tavily import TavilyClient

# Load API keys
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

api_key = os.getenv('OPENAI_API_KEY')
tavily_key = os.getenv('TAVILY_API_KEY')

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env")
if not tavily_key:
    raise ValueError("TAVILY_API_KEY not found in .env")

client = AsyncOpenAI(api_key=api_key)
tavily = TavilyClient(api_key=tavily_key)

class FunChatAgent:
    """Stateless greeter agent for deployment"""
    
    def __init__(self):
        self.conversation_history = []
        self.system_message = """You are a friendly, warm, and enthusiastic greeter bot. 
Your personality:
- Always greet users warmly and make them feel welcome
- Be conversational and engaging. 
- Be kids friendly and positive.
- Use 'google_search' to find relevant, interesting information when needed
- Keep responses concise, fun, and helpful
- Use emojis occasionally to add personality
- Help with questions, recommendations, and general chat
Stay positive and make the interaction enjoyable!"""

    async def perform_search(self, query):
        """Search for information using Tavily"""
        try:
            search_result = tavily.search(query=query, max_results=3)
            return json.dumps(search_result)
        except Exception as e:
            return json.dumps({"error": str(e)})

    async def chat(self, user_message):
        """
        Process user message and return agent response
        Returns: (response_text, used_search)
        """
        import datetime
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        dynamic_system_message = self.system_message + f"\n[System Info: The current date today is {current_date}]"

        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Call AI with search tool capability
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": dynamic_system_message}] + self.conversation_history,
            tools=[{
                "type": "function",
                "function": {
                    "name": "google_search",
                    "description": "Search for information on the web",
                    "parameters": {
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"]
                    }
                }
            }]
        )

        response_message = response.choices[0].message
        used_search = False

        # Handle tool calls
        if response_message.tool_calls:
            # Add assistant's tool call to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response_message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {"name": tc.function.name, "arguments": tc.function.arguments}
                    } for tc in response_message.tool_calls
                ]
            })
            
            for tool_call in response_message.tool_calls:
                query = json.loads(tool_call.function.arguments).get("query")
                search_result = await self.perform_search(query)
                
                # Add search result to history
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": search_result
                })
                used_search = True

            # Get final answer from AI
            final_res = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": dynamic_system_message}] + self.conversation_history
            )
            agent_text = final_res.choices[0].message.content
        else:
            agent_text = response_message.content

        # Add final response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": agent_text
        })

        return agent_text, used_search

    def reset_conversation(self):
        """Clear conversation history for new session"""
        self.conversation_history = []

    def get_history(self):
        """Get current conversation history"""
        return self.conversation_history

    def get_context_summary(self):
        """Get a summary of the conversation context"""
        if not self.conversation_history:
            return "No conversation yet"
        return f"{len(self.conversation_history)} messages in current session"


# For standalone CLI usage
async def main():
    """Interactive CLI mode"""
    agent = FunChatAgent()
    
    print("=" * 60)
    print("🤖 Welcome to Fun Chat Agent 🤖 ")
    print("=" * 60)
    print("Chat with me about anything! Type 'exit' to quit.\n")
    
    try:
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() == 'exit':
                print("\n👋 Thanks for chatting! Goodbye!")
                break
            
            print("Agent: Thinking...", end="\r")
            response, used_tool = await agent.chat(user_input)
            
            if used_tool:
                print(f"Agent: {response} (🔍 searched)\n")
            else:
                print(f"Agent: {response}\n")
            
    except KeyboardInterrupt:
        print("\n\n👋 Conversation ended. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())