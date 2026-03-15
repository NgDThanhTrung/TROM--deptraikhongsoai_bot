import os
import asyncio
import logging
import random
import re
from fastapi import FastAPI
from telethon import TelegramClient, events
from telethon.sessions import StringSession

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STR = os.environ.get("SESSION_STR", "")

spam_control = {"is_running": False, "stop_flag": False}
client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

@client.on(events.NewMessage(chats='deptraikhongsoai_bot'))
async def auto_revenge_handler(event):
    global spam_control
    message_text = event.raw_text
    
    if "BỊ MÓC TÚI!" in message_text and "đã trộm" in message_text:
        match = re.search(r'@(\w+)\s+đã trộm', message_text)
        if match:
            thief_username = f"@{match.group(1)}"
            logger.warning(f"REVENGE MODE: {thief_username}")
            
            spam_control["stop_flag"] = True
            await asyncio.sleep(2) 
            
            asyncio.create_task(run_sequence_spam("deptraikhongsoai_bot", thief_username, 100, mode="trom"))

async def run_sequence_spam(target: str, identifier: str, max_messages: int, mode: str):
    global spam_control
    
    if spam_control["is_running"] and not spam_control["stop_flag"]:
        return

    spam_control["is_running"] = True
    spam_control["stop_flag"] = False
    
    try:
        if not client.is_connected():
            await client.connect()
            
        for i in range(max_messages):
            if spam_control["stop_flag"]:
                break
            
            if mode == "trom":
                await client.send_message(target, f"/trom {identifier}")
                await asyncio.sleep(1.5)
                await client.send_message(target, "/mua mientu")
            elif mode == "tx":
                await client.send_message(target, f"/tx t {identifier}")
                await asyncio.sleep(1.5)
                await client.send_message(target, "/mua buatx")
            
            if i < max_messages - 1:
                await asyncio.sleep(random.uniform(5.0, 7.5))
                
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        spam_control["is_running"] = False
        spam_control["stop_flag"] = False

@app.get("/health")
async def health():
    return {"status": "alive", "busy": spam_control["is_running"]}

@app.get("/stop")
async def stop():
    spam_control["stop_flag"] = True
    return {"status": "stopped"}

@app.get("/trom-{user_id}/{count}")
async def trom_trigger(user_id: str, count: int):
    if spam_control["is_running"]:
        return {"error": "busy"}
    asyncio.create_task(run_sequence_spam("deptraikhongsoai_bot", user_id, count, mode="trom"))
    return {"status": "started", "mode": "trom"}

@app.get("/tx-t-{amount}/{count}")
async def tx_trigger(amount: str, count: int):
    if spam_control["is_running"]:
        return {"error": "busy"}
    asyncio.create_task(run_sequence_spam("deptraikhongsoai_bot", amount, count, mode="tx"))
    return {"status": "started", "mode": "tx"}

@app.on_event("startup")
async def startup():
    if API_ID and API_HASH and SESSION_STR:
        await client.connect()
