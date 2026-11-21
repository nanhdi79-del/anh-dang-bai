"""Nhan nut bam tu Telegram (duyet/sua/huy) va dua bai vao Buffer."""
import json, os, re, sys, urllib.request, urllib.error

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
BUFFER = os.environ.get("BUFFER_API_KEY", "")
RAW = "https://raw.githubusercontent.com/nanhdi79-del/anh-dang-bai/main/"
SERVICES = ("facebook", "youtube", "tiktok")


def tg(method, data=None):
    req = urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/{method}",
                                 json.dumps(data or {}).encode(), {"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"ok": False, "description": e.read().decode()[:300]}


def say(chat, text):
    tg("sendMessage", {"chat_id": chat, "text": text[:4000]})


def gql(query, variables=None):
    req = urllib.request.Request("https://api.buffer.com", json.dumps({"query": query, "variables": variables or {}}).encode(),
                                 {"Content-Type": "application/json", "Authorization": f"Bearer {BUFFER}"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"errors": [{"message": f"HTTP {e.code}: {e.read().decode()[:300]}"}]}


def url(p):
    return p if p.startswith("http") else RAW + p


def channels():
    r = gql("query { account { organizations { id name } } }")
    orgs = (((r.get("data") or {}).get("account") or {}).get("organizations")) or []
    if not orgs:
        raise RuntimeError("Khong lay duoc organization Buffer: " + json.dumps(r.get("errors") or r)[:300])
    out = []
    for o in orgs:
        r = gql("query($i: ChannelsInput!){ channels(input:$i){ id name displayName service isDisconnected } }",
                {"i": {"organizationId": o["id"]}})
        out += (r.get("data") or {}).get("channels") or []
    return [c for c in out if not c.get("isDisconnected")]


CREATE = """mutation($i: CreatePostInput!){ createPost(input:$i){
  ... on PostActionSuccess { post { id dueAt } }
  ... on MutationError { message } } }"""


def post(ch, text, assets, meta=None, draft=False):
    inp = {"channelId": ch["id"], "text": text, "schedulingType": "automatic", "mode": "addToQueue", "assets": assets}
    if meta:
        inp["metadata"] = meta
    if draft:
        inp["saveToDraft"] = True
    r = gql(CREATE, {"i": inp})
    if r.get("errors"):
        return False, r["errors"][0]["message"]
    d = (r.get("data") or {}).get("createPost") or {}
    if d.get("post"):
        return True, d["post"].get("dueAt") or "da vao hang doi"
    return False, d.get("message", "loi khong ro")


def publish_video(code, chat, draft=False):
    pkg = json.load(open(f"goi/{code}.json", encoding="utf-8"))
    chs = [c for c in channels() if c["service"] in SERVICES]
    if not chs:
        say(chat, "Buffer chua co kenh Facebook, YouTube, TikTok nao dang ket noi.")
        return
    lines = []
    for c in chs:
        s = c["service"]
        if s == "facebook":
            blk, meta = pkg.get("fb", {}), {"facebook": {"type": "reel"}}
        elif s == "youtube":
            blk = pkg.get("yt", {})
            meta = {"youtube": {"title": blk.get("title", "")[:100], "categoryId": "22"}}
        else:
            blk, meta = pkg.get("tt", {}), None
        if not blk.get("video"):
            lines.append(f"- {s}: goi khong co video"); continue
        ok, info = post(c, blk.get("text", ""), [{"video": {"url": url(blk["video"])}}], meta, draft)
        lines.append(f"- {c.get('displayName') or c['name']} ({s}): {'OK, ' if ok else 'LOI: '}{info}")
    say(chat, ("THU (chi luu nhap trong Buffer, CHUA dang):\n" if draft else "Ket qua dua vao Buffer:\n") + "\n".join(lines))


def publish_image(code, chat):
    pkg = json.load(open(f"goi/{code}.json", encoding="utf-8"))
    fb = pkg.get("fb", {})
    chs = [c for c in channels() if c["service"] == "facebook"]
    if not chs:
        say(chat, "Buffer chua co kenh Facebook nao dang ket noi."); return
    lines = []
    for c in chs:
        ok, info = post(c, fb.get("text", ""), [{"image": {"url": url(fb["image"])}}], {"facebook": {"type": "post"}})
        lines.append(f"- {c.get('displayName') or c['name']}: {'OK, ' if ok else 'LOI: '}{info}")
    say(chat, "Ket qua dua vao Buffer:\n" + "\n".join(lines))


def main():
    info = tg("getWebhookInfo")
    if (info.get("result") or {}).get("url"):
        tg("deleteWebhook", {"drop_pending_updates": False})
    res = tg("getUpdates", {"timeout": 0, "allowed_updates": ["callback_query"]})
    ups = res.get("result") or []
    print("updates:", len(ups), res.get("description", ""))
    for u in ups:
        cq = u.get("callback_query")
        if not cq:
            continue
        data, chat = cq.get("data", ""), cq["message"]["chat"]["id"]
        msg_id = cq["message"]["message_id"]
        tg("answerCallbackQuery", {"callback_query_id": cq["id"]})
        if not data.startswith("thu:"):
            tg("editMessageReplyMarkup", {"chat_id": chat, "message_id": msg_id, "reply_markup": {"inline_keyboard": []}})
        try:
            if data.startswith("duyet:"):
                if not BUFFER:
                    say(chat, "Chua co BUFFER_API_KEY trong kho."); continue
                say(chat, "Da duyet. Dang dua vao Buffer...")
                publish_video(data.split(":", 1)[1], chat)
            elif data.startswith("thu:"):
                if not BUFFER:
                    say(chat, "Chua co BUFFER_API_KEY trong kho."); continue
                say(chat, "Dang thu: luu nhap vao Buffer, khong dang that...")
                publish_video(data.split(":", 1)[1], chat, draft=True)
            elif data.startswith("dimg:"):
                if not BUFFER:
                    say(chat, "Chua co BUFFER_API_KEY trong kho."); continue
                say(chat, "Da duyet. Dang dua vao Buffer...")
                publish_image(data.split(":", 1)[1], chat)
            elif data == "huy":
                say(chat, "Da huy, khong dang bai nay.")
            elif data == "sua":
                say(chat, "Anh nhan cho Claude cho can sua trong cuoc tro chuyen chinh, em se sua va gui lai ban moi.")
        except Exception as e:  # bao loi len Telegram
            say(chat, f"Loi khi xu ly: {e}")
    if ups:
        tg("getUpdates", {"offset": ups[-1]["update_id"] + 1, "timeout": 0})


main()
