import json, os, re, sys, urllib.request
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT = os.environ.get("TELEGRAM_CHAT_ID", "8674492982")
RAW = "https://raw.githubusercontent.com/nanhdi79-del/anh-dang-bai/main/"

def api(method, data):
    req = urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/{method}",
        json.dumps(data).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

code = sys.argv[1]
pkg = json.load(open(f"goi/{code}.json", encoding="utf-8"))
fb = pkg.get("fb", {})
ten = re.sub(r"\s*\(.*?\)\s*$", "", pkg.get("ten", code))
text = (ten + "\n\n" + fb.get("text", ""))[:1020]
kb = {"inline_keyboard": [[
    {"text": "✅ Duyệt", "callback_data": f"duyet:{code}"},
    {"text": "✏️ Sửa", "callback_data": "sua"},
    {"text": "🗑 Huỷ", "callback_data": "huy"}],
    [{"text": "🧪 Thử (lưu nháp, không đăng)", "callback_data": f"thu:{code}"}]]}
if fb.get("video"):
    res = api("sendVideo", {"chat_id": CHAT, "video": RAW + fb["video"] if not fb["video"].startswith("http") else fb["video"],
                            "supports_streaming": True, "caption": text, "reply_markup": kb})
else:
    res = api("sendPhoto", {"chat_id": CHAT, "photo": RAW + fb["image"] if not fb["image"].startswith("http") else fb["image"],
                            "caption": text, "reply_markup": kb})
print(res.get("ok"), res.get("description", ""))
