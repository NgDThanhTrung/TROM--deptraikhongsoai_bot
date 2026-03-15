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
    if "BỊ MÓC TÚI!" in event.raw_text and "đã trộm" in event.raw_text:
        match = re.search(r'@(\w+)\s+đã trộm', event.raw_text)
        if match:
            thief = f"@{match.group(1)}"
            logger.warning(f"REVENGE START: {thief}")
            
            spam_control["stop_flag"] = True
            await asyncio.sleep(3) # Tăng thời gian đợi dừng hẳn
            
            asyncio.create_task(run_task("deptraikhongsoai_bot", thief, 100, "trom"))

async def run_task(target, data, count, mode):
    global spam_control
    if spam_control["is_running"] and not spam_control["stop_flag"]:
        return

    spam_control["is_running"], spam_control["stop_flag"] = True, False
    
    try:
        if not client.is_connected(): await client.connect()
        for i in range(count):
            if spam_control["stop_flag"]: break
            
            if mode == "trom":
                await client.send_message(target, f"/trom {data}")
                await asyncio.sleep(2.5) # Tăng từ 1.5s lên 2.5s để tránh bot quét 2 tin nhắn gần nhau
                await client.send_message(target, "/mua mientu")
            elif mode == "tx":
                await client.send_message(target, f"/tx t {data}")
                await asyncio.sleep(2.5) # Tăng từ 1.5s lên 2.5s
                await client.send_message(target, "/mua buatx")
            else:
                await client.send_message(target, data)
            
            # Nghỉ ngẫu nhiên từ 6.5s đến 9.5s (An toàn hơn mức 5s tối thiểu)
            if i < count - 1:
                await asyncio.sleep(random.uniform(6.5, 9.5))
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
    return {"status": "stopping"}

@app.get("/trom-{user_id}/{count}")
async def trom_api(user_id: str, count: int):
    if spam_control["is_running"]: return {"status": "busy"}
    asyncio.create_task(run_task("deptraikhongsoai_bot", user_id, count, "trom"))
    return {"status": "started"}

@app.get("/tx-t-{amount}/{count}")
async def tx_api(amount: str, count: int):
    if spam_control["is_running"]: return {"status": "busy"}
    asyncio.create_task(run_task("deptraikhongsoai_bot", amount, count, "tx"))
    return {"status": "started"}

@app.get("/{bot}/{cmd}/{count}")
async def any_api(bot: str, cmd: str, count: int):
    if spam_control["is_running"]: return {"status": "busy"}
    full_cmd = f"/{cmd.replace('-', ' ')}"
    asyncio.create_task(run_task(bot, full_cmd, count, "any"))
    return {"status": "started"}

@app.on_event("startup")
async def startup():
    if API_ID and API_HASH and SESSION_STR: await client.connect()
