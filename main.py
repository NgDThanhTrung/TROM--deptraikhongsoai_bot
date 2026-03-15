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
            logger.warning(f"DETECTED THEFT! Thief: {thief_username}. Starting revenge...")
            
            spam_control["stop_flag"] = True
            await asyncio.sleep(1)
            
            asyncio.create_task(run_sequence_spam("deptraikhongsoai_bot", thief_username, 100))

async def run_universal_spam(target: str, base_cmd: str, max_messages: int):
    global spam_control
    if spam_control["is_running"]: return
    spam_control["is_running"], spam_control["stop_flag"] = True, False
    try:
        if not client.is_connected(): await client.connect()
        for i in range(max_messages):
            if spam_control["stop_flag"]: break
            msg_content = f"{base_cmd} #{i + 1}"
            await client.send_message(target, msg_content)
            logger.info(f"Sent to {target}: {msg_content}")
            if i < max_messages - 1:
                await asyncio.sleep(random.uniform(1.5, 3.5))
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        spam_control["is_running"] = False

async def run_sequence_spam(target: str, user_id: str, max_messages: int):
    global spam_control
    spam_control["is_running"], spam_control["stop_flag"] = True, False
    try:
        if not client.is_connected(): await client.connect()
        for i in range(max_messages):
            if spam_control["stop_flag"] and i > 0: break
            
            await client.send_message(target, f"/trom {user_id}")
            await asyncio.sleep(1.5)
            await client.send_message(target, "/mua mientu")
            
            if i < max_messages - 1:
                await asyncio.sleep(random.uniform(5.0, 7.5))
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        spam_control["is_running"] = False

async def run_tx_sequence(target: str, amount: str, max_messages: int):
    global spam_control
    if spam_control["is_running"]: return
    spam_control["is_running"], spam_control["stop_flag"] = True, False
    try:
        if not client.is_connected(): await client.connect()
        for i in range(max_messages):
            if spam_control["stop_flag"]: break
            await client.send_message(target, f"/tx t {amount}")
            await asyncio.sleep(1.5)
            await client.send_message(target, "/mua buatx")
            if i < max_messages - 1:
                await asyncio.sleep(random.uniform(5.0, 7.5))
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        spam_control["is_running"] = False

@app.get("/health")
async def health():
    return {"status": "alive"}

@app.get("/stop")
async def stop():
    spam_control["stop_flag"] = True
    return {"status": "stopped"}

@app.get("/trom-{user_id}/{count}")
async def trom_trigger(user_id: str, count: int):
    target_bot = "deptraikhongsoai_bot"
    asyncio.create_task(run_sequence_spam(target_bot, user_id, count))
    return {"status": "started", "mode": "trom_sequence", "victim": user_id}

@app.get("/tx-t-{amount}/{count}")
async def tx_trigger(amount: str, count: int):
    target_bot = "deptraikhongsoai_bot"
    asyncio.create_task(run_tx_sequence(target_bot, amount, count))
    return {"status": "started", "mode": "tx_sequence", "amount": amount}

@app.get("/{bot_username}/{command}/{count}")
async def dynamic_trigger(bot_username: str, command: str, count: int):
    full_cmd = f"/{command.replace('-', ' ')}"
    asyncio.create_task(run_universal_spam(bot_username, full_cmd, count))
    return {"target": bot_username, "cmd": full_cmd, "count": count}

@app.on_event("startup")
async def startup():
    if API_ID and API_HASH and SESSION_STR:
        await client.connect()
