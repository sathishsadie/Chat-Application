from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from collections import deque
from typing import Any, Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.pydantic_v1 import Field
from langdetect import detect, LangDetectException
import time
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ---------------- Initialize FastAPI App ----------------
app = FastAPI()
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Pydantic Models ----------------
class QueryRequest(BaseModel):
    message: str

class IngredientCheck(BaseModel):
    recipe: str

class BuyItem(BaseModel):
    item: str
    quantity: int

# ---------------- Kitchen Data ----------------
RECIPE_INGREDIENTS = {
    "curd rice": ["rice", "curd", "salt"],
    "lemon rice": ["rice", "lemon", "green chili", "salt", "oil"],
    "tomato rice": ["rice", "tomato", "onion", "spices", "salt", "oil"]
}

# Assume the kitchen already has some items
KITCHEN_STOCK = {
    "rice": True,
    "curd": True,
    "salt": True,
    "lemon": False,
    "green chili": False,
    "oil": True,
    "tomato": True,
    "onion": True,
    "spices": True
}

# ---------------- LangChain Tools ----------------
@tool
def check_ingredients(recipe: str = Field(description="Recipe name to check ingredients")) -> str:
    """Checks if ingredients for a recipe are available in the kitchen."""
    recipe_lower = recipe.lower()
    if recipe_lower not in RECIPE_INGREDIENTS:
        return f"Sorry, I only know how to cook Curd Rice, Lemon Rice, and Tomato Rice."

    required = RECIPE_INGREDIENTS[recipe_lower]
    missing = [item for item in required if not KITCHEN_STOCK.get(item, False)]

    if missing:
        return f"To cook {recipe.title()}, you are missing: {', '.join(missing)}. Please buy them from the store."
    else:
        return f"All ingredients are available ✅. You can cook {recipe.title()} now!"

@tool
async def buy_item(item: str, quantity: int) -> str:
    """Buys missing kitchen items and updates stock."""
    KITCHEN_STOCK[item] = True
    return f"Bought {quantity} {item}(s). Stock updated!"

# ---------------- Agent Configuration ----------------
BASE_SYSTEM_PROMPT = (
    "You are Kitchen AI — a helpful cooking assistant.\n"
    "1. You only know how to cook 3 recipes: Curd Rice, Lemon Rice, and Tomato Rice.\n"
    "2. To check ingredients, use the `check_ingredients` tool.\n"
    "3. If ingredients are missing, suggest buying them with the `buy_item` tool.\n"
    "4. Avoid making up other recipes or ingredients.\n"
)

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.0,api_key=GEMINI_API_KEY)

TOOLS = [check_ingredients, buy_item]
memory: deque = deque(maxlen=20)

def extract_response_text(resp: Any) -> str:
    if isinstance(resp, dict):
        return str(resp.get("output", resp))
    return str(resp)

# ---------------- FastAPI Endpoints ----------------
@app.post("/chat")
async def chat_with_bot(request: QueryRequest):
    st = time.time()
    input_message = request.message

    try:
        user_lang = detect(input_message)
    except LangDetectException:
        user_lang = "en"

    final_prompt_instruction = "\n\nRespond in English language."

    translated_query = input_message

    chat_history_list = list(memory)

    dynamic_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", BASE_SYSTEM_PROMPT + final_prompt_instruction),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    try:
        agent = create_tool_calling_agent(llm, TOOLS, dynamic_prompt)
        agent_executor = AgentExecutor(agent=agent, tools=TOOLS, verbose=True)
        result = await agent_executor.ainvoke({
            'input': input_message,
            'chat_history': chat_history_list
        })
    except Exception as e:
        return {"response": f"Sorry, an error was raised: {e}"}

    assistant_text = extract_response_text(result)
    memory.append(HumanMessage(content=input_message))
    memory.append(AIMessage(content=assistant_text))
    en = time.time()
    return {"response": assistant_text, "Total Time Taken": en-st}

@app.post("/buy")
async def buy(data: BuyItem):
    KITCHEN_STOCK[data.item] = True
    return {"message": f"Bought {data.quantity} {data.item}(s). Stock updated!"}
