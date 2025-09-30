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
import time
from langdetect import detect, LangDetectException
# Removed: from vc import main as VoiceAssistant (assuming it's not used elsewhere)

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class QueryRequest(BaseModel):
    message: str

class FarmData(BaseModel):
    name: str

class LivestockTransactionData(BaseModel):
    operation: Literal["buy", "sell"]
    animal_type: str
    quantity: int

class CollectData(BaseModel):
    animal_type: str
    quantity: int

class ManageYieldData(BaseModel):
    product_name: str
    quantity: int
    action: str

# --- Language Detection ---
def detect_language(text: str) -> str:
    """Detects the language of a given text."""
    try:
        return detect(text)
    except LangDetectException:
        return "en"

# --- LangChain Tools ---
@tool
def translate_to_english(text: str = Field(description="The text to translate into English.")) -> str:
    """Translates a given text from any language into English using Gemini."""
    llm_translator = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.0)
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a professional translator. Your sole purpose is to accurately translate text into English."),
            ("user", "Translate the following text to English, respond with ONLY the translated text: {text}")
        ]
    )
    chain = prompt_template | llm_translator
    translation = chain.invoke({"text": text})
    return translation.content

@tool
async def createfarm(name: str) -> str:
    """Creates a new farm with the given name for the user."""
    name_clean = (name or "").strip()
    if not name_clean:
        return "Please provide a non-empty farm name."
    resp = await create_farm(FarmData(name=name_clean))
    
    success_message = resp.get("message", f"Farm '{name_clean}' created successfully!")
    guidance_prompt = "To help you get started, would you like to see a profit analysis to decide which animals to invest in?"
    
    return f"{success_message}\n\n{guidance_prompt}"

@tool
async def show_profit_analysis() -> str:
    """Use this tool only when a user asks about profit, interest, or financial 
    analysis related to farm animals (goats, hens, quails). or Uses this Tool to provide a profit about an animal products like eggs or kids .
    Don't Use this tool to provide profit analysis on the company and other analysis
    Correct usage: Farm livestock profit analysis, ROI, or investment breakdown.
    """
    report = """
        Here is a complete lifetime profit analysis to help you decide on the best investment.

        ### Lifetime Profit Analysis (Per Animal)

        | Metric                     | Goat 🐐         | Normal Hen 🐔 | Quail 🐦      |
        | :------------------------- | :-------------- | :------------ | :------------ |
        | **Investment (Costs)** |                 |               |               |
        | Upfront Purchase Cost      | (₹ 4,000)       | (₹ 250)       | (₹ 40)        |
        | Total Lifetime Feed & Maint.| (₹ 10,000)      | (₹ 1,500)     | (₹ 500)       |
        | **Total Lifetime Investment**| **(₹ 14,000)** | **(₹ 1,750)** | **(₹ 540)** |
        |                            |                 |               |               |
        | **Returns (Revenue)** |                 |               |               |
        | **Product Price** | ₹4,000(kid goat)| ₹6(1 chicken egg) | ₹3 (1 quail egg) |
        | Lifetime Production        | 20–26 Kids      | ~ 1,050 Eggs  | ~ 550 Eggs    |
        | Lifetime Revenue (Products)| ₹92,000         | ₹6,300        | ₹1,650        |
        | Final Sale Price (Meat)    | ₹ 15,000        | ₹ 150         | ₹ 60          |
        | **Total Lifetime Revenue** | **~ ₹ 107,000** | **₹ 6,450** | **₹ 1,710** |
        |                            |                 |               |               |
        | **Financial Summary** |                 |               |               |
        | **Total Lifetime Profit** | **~ ₹ 93,000** | **₹ 4,700** | **₹ 1,170** |
        | **Annualized Profit** | **~ ₹ 9,300** | **~ ₹ 783** | **~ ₹ 585** |
        | **Return on Investment (ROI)**| **~ 664%** | **~ 269%** | **~ 217%** |

        ---
        ### Business Analysis

        * **Goats (High Return, Long-Term):** The most profitable long-term asset with an enormous **664% ROI**.
        * **Hens (Excellent All-Rounder):** Offer a fantastic balance with a very strong **269% ROI** and provide a much faster return than goats.
        * **Quails (Quick & Efficient):** The perfect entry-level investment with an excellent **217% ROI** over two years.
    """
    return report

@tool
async def manageLiveStock(operation: str, animal_type: str, quantity: int) -> str:
    """
    Use this tool to buy and sell livestock from the farm. 
    Always make an operation : buy or sell, 
    Livestock or animal_type includes chicken, quail, and goat, 
    No of animals : int
    **Always ask the user for confirmation before executing this tool.**
    """
    valid_animals = ["chicken", "quail", "goat"]
    op_clean = operation.lower()
    animal_clean = animal_type.lower()
    
    if op_clean not in ["buy", "sell"]:
        return f"Error: Invalid operation '{operation}'. Please use 'buy' or 'sell'."
    if animal_clean not in valid_animals:
        return f"Error: Unknown animal type '{animal_type}'. Valid animals are: {valid_animals}."
    
    data = LivestockTransactionData(operation=op_clean, animal_type=animal_clean, quantity=quantity)
    resp = await livestock_transaction(data)
    return resp.get("message")

ANIMAL_CATALOG = {
    "chicken": {"yields": "egg", "is_offspring": False},
    "quail": {"yields": "egg", "is_offspring": False},
    "goat": {"yields": "kid", "is_offspring": True},
}

@tool
async def collect_yield(animal_type: str, quantity: int) -> str:
    """
    Step 1: Checks a specific number of animals for any yield (eggs or offspring).
    The AI must ask the user what to do next.
    """
    animal_clean = animal_type.lower()
    if animal_clean not in ANIMAL_CATALOG:
        return f"Error: Unknown animal type '{animal_type}'."
    
    data = CollectData(animal_type=animal_clean, quantity=quantity)
    resp = await collect(data)
    return resp.get("message")

@tool
async def manage_yield(product_name: str, quantity: int, action: str) -> str:
    """
    Step 2: Manages the yield that was just collected after the user has decided what to do.
    Valid actions for offspring (kids): 'raise', 'sell'.
    Valid actions for products (eggs): 'keep', 'sell'.
    """
    product_clean = product_name.lower()
    action_clean = action.lower()
    
    is_offspring = any(d.get("yields") == product_clean and d.get("is_offspring") for d in ANIMAL_CATALOG.values())
    valid_actions = ["raise", "sell"] if is_offspring else ["keep", "sell"]
        
    if action_clean not in valid_actions:
        return f"Error: Invalid action '{action}' for {product_name}. Valid actions are: {valid_actions}."
        
    data = ManageYieldData(product_name=product_clean, quantity=quantity, action=action_clean)
    resp = await manage(data)
    return resp.get("message")

# --- Agent Configuration ---
BASE_SYSTEM_PROMPT = (
    "You are Topia Farm AI — a helpful assistant with the following core functions\n"
    "1. To buy or sell livestock, use the `manageLiveStock` tool. Always ask for confirmation first.\n"
    "2. To handle farm products like eggs or newborns like kids, use a two-step process:\n"
    "   - First, call `collect_yield` to check for products.\n"
    "   - Second, after the user responds, call `manage_yield` to either keep, sell, or raise the products.\n"
    "3. If the user asks for business advice about animals or buying animals in the farm or profit analysis on animals, use the `show_profit_analysis` tool.\n"
    "4. If the user wants to create a farm, use the `createfarm` tool.\n"
    "Avoid inventing facts. If uncertain, say you don't know. & user asks about yourself respond in a correct way instead of from context ."
)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.0)

TOOLS = [
    createfarm, 
    translate_to_english, 
    show_profit_analysis, 
    manageLiveStock, 
    collect_yield, 
    manage_yield
]
memory: deque = deque(maxlen=20)

def extract_response_text(resp: Any) -> str:
    """Extract agent response text safely."""
    if isinstance(resp, dict):
        return str(resp.get("output", resp))
    return str(resp)

# --- FastAPI Endpoints ---
@app.post("/chat")
async def chat_with_bot(request: QueryRequest):
    st = time.time()
    input_message = request.message
    
    try:
        user_lang = detect(input_message)
    except LangDetectException:
        user_lang = "en"
    
    final_prompt_instruction = "\n\nRespond in English language."
    
    # Translation logic is kept as it is independent of the vector store
    translated_query = input_message
    if user_lang != 'en':
        try:
            translated_query = translate_to_english(input_message)
        except Exception as e:
            print(f"Translation failed: {e}")

    print(f"Original: '{input_message}', Language: {user_lang}, Translated for agent: '{translated_query}'")
    
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
    print(f"\n\nTotal Time : {en-st}\n\n")
    return {"response": assistant_text, "Total Time Taken": en-st}

@app.post("/createfarm")
async def create_farm(data: FarmData):
    print(f"Received request to create farm: {data.name}")
    return {"message": f"Farm '{data.name}' created successfully!"}

@app.post("/livestock_transaction")
async def livestock_transaction(data: LivestockTransactionData):
    """Endpoint to handle buying and selling livestock."""
    print(f"Received request to {data.operation} {data.quantity} {data.animal_type}(s)")
    action_past_tense = "purchased" if data.operation == "buy" else "sold"
    return {"message": f"{data.quantity} {data.animal_type}(s) have been {action_past_tense} successfully."}

@app.post("/collect")
async def collect(data: CollectData):
    """Endpoint for Step 1: collecting yield."""
    print(f"Received request to collect yield from {data.quantity} {data.animal_type}(s)")
    product_name = ANIMAL_CATALOG[data.animal_type]["yields"]
    yield_quantity = data.quantity  # Assuming 1 yield per animal
    return {"message": f"Success! Found {yield_quantity} {product_name}(s) from {data.quantity} {data.animal_type}(s)."}

@app.post("/manage_yield")
async def manage(data: ManageYieldData):
    """Endpoint for Step 2: managing the collected yield."""
    print(f"Received request to {data.action} {data.quantity} {data.product_name}(s)")
    return {"message": f"Action complete: {data.quantity} {data.product_name}(s) have been successfully {data.action}ed."}