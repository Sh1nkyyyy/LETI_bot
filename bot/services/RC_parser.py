import aiohttp
import asyncio
import json
from datetime import datetime, timezone, timedelta

from config_data.config import config

url_endpoint = "/api/v1/groups.history"
url_domain = "https://student-chat.moevm.pro"

url = url_domain + url_endpoint

headers = {
    "accept": "application/json",
    "X-User-Id": config.rc_user_id,
    "X-Auth-Token": config.rc_auth_token.get_secret_value(),
}


async def fetch_messages():
    async with aiohttp.client.ClientSession() as session:
        
        rooms = config.rc_rooms
        
        new_msgs = {}
        
        for room_name, room_id in rooms.items():
            query_params = {
                "roomId": room_id,
                "oldest": ((datetime.now(timezone.utc)) - timedelta(hours=1)).replace(
                    minute=0, second=0, microsecond=0
                    ).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            }
            
            msgs = await check_room(session, query_params)
            
            if msgs:
                new_msgs[room_name] = msgs
                
        return new_msgs
        
        
async def check_room(session: aiohttp.client.ClientSession, query_params):
    async with session.get(url=url, headers=headers, params=query_params) as resp:
        if resp.status == 200:
            
            print(f"Ответ получен. Статус {resp.status}")
            
            resp_json = await resp.json(encoding="utf-8")
            
            if resp_json["messages"]:
                messages = resp_json["messages"]
            
                cleaned_messages = []
                
                for message in messages:
                    if message.get("tmid"):
                        continue
                    
                    user_info = message.get("u", {})
                    
                    clean_msg = {
                        "text": message.get("msg", "").strip(),
                        "date": message.get("ts"),
                        "author": user_info.get("name")
                    }
                    
                    cleaned_messages.append(clean_msg)
                    
                return cleaned_messages
                
                
                
                

if __name__ == "__main__":
   asyncio.run(fetch_messages())
    


