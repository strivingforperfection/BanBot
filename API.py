#author: striving
#don't steal my code without giving me credits
import os 
import json
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()

ban_file = "bans.json"
api_key = ""
#same as what it would be in "BanBot.py"

class ban_entry(BaseModel):
    robloxid: str
    moderatordiscordid: str
    reason: str = ""


def load_bans():
    #create a bans.json file
    if not os.path.exists(ban_file):
        with open(ban_file, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}
    
    try:
        with open(ban_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_bans(bans):
    with open(ban_file, "w", encoding="utf-8") as f:
        json.dump(bans, f, indent=2)


def check_key(x_api_key):
    if api_key and x_api_key != api_key:
        raise HTTPException(status_code=401, detail="bad key")


@app.post("/ban")
async def ban(entry: ban_entry, x_api_key: str = Header(None)):
    check_key(x_api_key)
    bans = load_bans()
    bans[entry.robloxid] = {
        "moderator": entry.moderatordiscordid,
        "reason": entry.reason
    }
    save_bans(bans)
    return {"status": "ok", "robloxid": entry.robloxid}


@app.post("/unban")
async def unban(entry: ban_entry, x_api_key: str = Header(None)):
    check_key(x_api_key)
    bans = load_bans()
    if entry.robloxid in bans:
        del bans[entry.robloxid]
        save_bans(bans)
        return {"status": "ok", "robloxid": entry.robloxid}
    return {"status": "not_found", "robloxid": entry.robloxid}


@app.get("/is_banned/{roblox_id}")
async def is_banned(roblox_id: str):
    bans = load_bans()
    if roblox_id in bans:
        return {"banned": True, "entry": bans[roblox_id]}
    return {"banned": False}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
