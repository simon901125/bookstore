from __future__ import annotations

import json
import re
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import NamedTemporaryFile


ROOT = Path(__file__).resolve().parent
MEMBER_FILE = ROOT / "python" / "member.json"
ORDER_FILE = ROOT / "python" / "order.json"
BOOKS_FILE = ROOT / "python" / "books.json"
SAVING_BOOKS_FILE = ROOT / "python" / "member_savingbooks.json"


def load_books() -> list[dict]:
    if not BOOKS_FILE.exists():
        return []
    with BOOKS_FILE.open("r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except:
            return []


def save_books(books: list[dict]) -> None:
    BOOKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(
        "w", encoding="utf-8", dir=BOOKS_FILE.parent, delete=False, suffix=".tmp"
    ) as temp_file:
        json.dump(books, temp_file, ensure_ascii=False, indent=2)
        temp_file.write("\n")
        temp_path = Path(temp_file.name)
    temp_path.replace(BOOKS_FILE)

COMMON_EMAIL_DOMAINS = {
    "gmail.com",
    "yahoo.com",
    "yahoo.com.tw",
    "hotmail.com",
    "outlook.com",
    "icloud.com",
    "msn.com",
    "live.com",
    "protonmail.com",
    "mail.com",
    "pchome.com.tw",
    "seed.net.tw",
    "hinet.net",
}

TAIWAN_CITIES = {
    "\u53f0\u5317\u5e02",
    "\u65b0\u5317\u5e02",
    "\u6843\u5712\u5e02",
    "\u53f0\u4e2d\u5e02",
    "\u53f0\u5357\u5e02",
    "\u9ad8\u96c4\u5e02",
    "\u57fa\u9686\u5e02",
    "\u65b0\u7af9\u5e02",
    "\u5609\u7fa9\u5e02",
    "\u65b0\u7af9\u7e23",
    "\u82d7\u6817\u7e23",
    "\u5f70\u5316\u7e23",
    "\u5357\u6295\u7e23",
    "\u96f2\u6797\u7e23",
    "\u5609\u7fa9\u7e23",
    "\u5c4f\u6771\u7e23",
    "\u5b9c\u862d\u7e23",
    "\u82b1\u84ee\u7e23",
    "\u53f0\u6771\u7e23",
    "\u6f8e\u6e56\u7e23",
    "\u91d1\u9580\u7e23",
    "\u9023\u6c5f\u7e23",
}

REQUIRED_MEMBER_FIELDS = [
    "email",
    "password",
    "nickname",
    "gender",
    "birthday",
    "phone",
    "address",
    "securityQuestion",
    "securityAnswer",
]


def load_members() -> list[dict]:
    if not MEMBER_FILE.exists():
        return []

    with MEMBER_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data if isinstance(data, list) else []


def save_members(members: list[dict]) -> None:
    MEMBER_FILE.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=MEMBER_FILE.parent,
        delete=False,
        suffix=".tmp",
    ) as temp_file:
        json.dump(members, temp_file, ensure_ascii=False, indent=2)
        temp_file.write("\n")
        temp_path = Path(temp_file.name)

    temp_path.replace(MEMBER_FILE)


def load_orders() -> list[dict]:
    if not ORDER_FILE.exists():
        return []
    with ORDER_FILE.open("r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            return data if isinstance(data, list) else []
        except:
            return []


def save_orders(orders: list[dict]) -> None:
    ORDER_FILE.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=ORDER_FILE.parent,
        delete=False,
        suffix=".tmp",
    ) as temp_file:
        json.dump(orders, temp_file, ensure_ascii=False, indent=2)
        temp_file.write("\n")
        temp_path = Path(temp_file.name)
    temp_path.replace(ORDER_FILE)


def load_saving_books() -> list[dict]:
    if not SAVING_BOOKS_FILE.exists():
        return []

    with SAVING_BOOKS_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data if isinstance(data, list) else []


def save_saving_books(records: list[dict]) -> None:
    SAVING_BOOKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=SAVING_BOOKS_FILE.parent,
        delete=False,
        suffix=".tmp",
    ) as temp_file:
        json.dump(records, temp_file, ensure_ascii=False, indent=2)
        temp_file.write("\n")
        temp_path = Path(temp_file.name)

    temp_path.replace(SAVING_BOOKS_FILE)


def validate_member(member: dict, existing_members: list[dict]) -> str | None:
    if not isinstance(member, dict):
        return "\u6703\u54e1\u8cc7\u6599\u683c\u5f0f\u4e0d\u6b63\u78ba\u3002"

    missing_fields = [field for field in REQUIRED_MEMBER_FIELDS if not member.get(field)]
    if missing_fields:
        return "\u8acb\u5b8c\u6574\u586b\u5beb\u6240\u6709\u5fc5\u586b\u6b04\u4f4d\u3002"

    email = str(member["email"]).strip().lower()
    match = re.fullmatch(r"[a-z0-9._%+-]+@([a-z0-9.-]+\.[a-z]{2,})", email)
    if not match or match.group(1) not in COMMON_EMAIL_DOMAINS:
        return "\u96fb\u5b50\u90f5\u4ef6\u683c\u5f0f\u6216\u7db2\u57df\u4e0d\u7b26\u5408\u8a3b\u518a\u898f\u5247\u3002"

    if any(str(item.get("email", "")).lower() == email for item in existing_members):
        return "\u6b64\u96fb\u5b50\u90f5\u4ef6\u5df2\u7d93\u8a3b\u518a\u904e\u3002"

    phone = str(member["phone"]).strip()
    if any(str(item.get("phone", "")).strip() == phone for item in existing_members):
        return "此電話號碼已被其他帳號使用。"

    password = str(member["password"])
    if (
        not re.fullmatch(r"[A-Za-z0-9]{1,20}", password)
        or not re.search(r"[A-Z]", password)
        or not re.search(r"[a-z]", password)
        or not re.search(r"\d", password)
    ):
        return "\u5bc6\u78bc\u9700\u5305\u542b\u5927\u5c0f\u5beb\u82f1\u6587\u5b57\u6bcd\u8207\u6578\u5b57\uff0c\u6700\u591a 20 \u4f4d\uff0c\u4e14\u4e0d\u53ef\u4f7f\u7528\u7b26\u865f\u3002"

    if len(str(member["nickname"])) > 20:
        return "\u66b1\u7a31\u4e0d\u53ef\u8d85\u904e 20 \u5b57\u3002"

    if not re.fullmatch(r"09\d{8}", str(member["phone"])):
        return "\u806f\u7d61\u96fb\u8a71\u9700\u70ba 09 \u958b\u982d\u7684 10 \u78bc\u624b\u6a5f\u865f\u78bc\u3002"

    address = str(member["address"])
    has_city = any(city in address for city in TAIWAN_CITIES)
    has_district = re.search(r"[^\s]+(\u5340|\u9109|\u93ae|\u5e02)", address)
    has_street = re.search(r"(\u8def|\u8857|\u5927\u9053|\u5df7|\u5f04)", address)
    has_number = re.search(r"\d+\u865f", address)
    if not (has_city and has_district and has_street and has_number):
        return "\u914d\u9001\u5730\u5740\u9700\u70ba\u5b8c\u6574\u7684\u53f0\u7063\u5730\u5740\u3002"

    member["email"] = email
    return None


class BookstoreRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.end_headers()

    def do_GET(self) -> None:
        if self.path.startswith("/api/orders"):
            self.handle_get_orders()
            return
        super().do_GET()

    def do_POST(self) -> None:
        if self.path == "/api/register":
            self.handle_register()
            return

        if self.path == "/api/update-member":
            self.handle_update_member()
            return

        if self.path == "/api/orders":
            self.handle_create_order()
            return

        if self.path == "/api/update-order-status":
            self.handle_update_order_status()
            return

        if self.path == "/api/saving-books":
            self.handle_saving_books()
            return

        self.send_error(HTTPStatus.NOT_FOUND)

    def do_DELETE(self) -> None:
        if self.path == "/api/saving-books":
            self.handle_remove_saving_book()
            return

        self.send_error(HTTPStatus.NOT_FOUND)

    def read_json_payload(self) -> dict:
        content_length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(content_length).decode("utf-8")
        return json.loads(payload)

    def handle_register(self) -> None:
        try:
            member = self.read_json_payload()
            members = load_members()
            validation_error = validate_member(member, members)
            if validation_error:
                self.send_json({"ok": False, "message": validation_error}, HTTPStatus.BAD_REQUEST)
                return

            members.append({field: member[field] for field in REQUIRED_MEMBER_FIELDS})
            save_members(members)
            self.send_json(
                {
                    "ok": True,
                    "member": {
                        "email": member["email"],
                        "nickname": member["nickname"],
                    },
                },
                HTTPStatus.CREATED,
            )
        except json.JSONDecodeError:
            self.send_json(
                {"ok": False, "message": "\u9001\u51fa\u7684\u8cc7\u6599\u4e0d\u662f\u6709\u6548 JSON\u3002"},
                HTTPStatus.BAD_REQUEST,
            )
        except Exception as error:
            self.send_json(
                {"ok": False, "message": f"\u5beb\u5165\u6703\u54e1\u8cc7\u6599\u5931\u6557\uff1a{error}"},
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    def handle_update_member(self) -> None:
        try:
            update_data = self.read_json_payload()
            email = str(update_data.get("email", "")).strip().lower()
            if not email:
                self.send_json({"ok": False, "message": "缺少會員 Email。"}, HTTPStatus.BAD_REQUEST)
                return

            members = load_members()
            member_index = next((i for i, m in enumerate(members) if str(m.get("email", "")).lower() == email), -1)
            
            if member_index == -1:
                self.send_json({"ok": False, "message": "找不到該會員。"}, HTTPStatus.NOT_FOUND)
                return

            member = members[member_index]
            
            # Check phone uniqueness if phone is being updated
            if "phone" in update_data:
                new_phone = str(update_data["phone"]).strip()
                if any(str(m.get("phone", "")).strip() == new_phone and str(m.get("email", "")).lower() != email for m in members):
                    self.send_json({"ok": False, "message": "此電話號碼已被其他會員使用。"}, HTTPStatus.CONFLICT)
                    return

            updatable_fields = ["password", "nickname", "gender", "birthday", "phone", "address", "securityQuestion", "securityAnswer"]
            for field in updatable_fields:
                if field in update_data:
                    member[field] = update_data[field]

            save_members(members)
            self.send_json({"ok": True, "message": "會員資料已更新。"})
            
        except Exception as error:
            self.send_json({"ok": False, "message": f"更新失敗：{error}"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    def handle_create_order(self) -> None:
        try:
            order_data = self.read_json_payload()
            email = str(order_data.get("email", "")).strip().lower()
            if not email:
                self.send_json({"ok": False, "message": "缺少會員 Email。"}, HTTPStatus.BAD_REQUEST)
                return

            items = order_data.get("items", [])
            books = load_books()
            
            # --- 庫存檢查與扣除 ---
            for item in items:
                book = next((b for b in books if str(b.get("isbn")) == str(item.get("isbn"))), None)
                if not book:
                    self.send_json({"ok": False, "message": f"書籍 {item.get('title')} 不存在。"}, HTTPStatus.BAD_REQUEST)
                    return
                if book.get("stock", 0) < item.get("quantity", 0):
                    self.send_json({"ok": False, "message": f"書籍 {item.get('title')} 庫存不足。"}, HTTPStatus.BAD_REQUEST)
                    return
                book["stock"] -= item.get("quantity", 0)
            # --------------------

            orders = load_orders()
            import random
            import datetime
            order_id = f"ARC-{datetime.datetime.now().strftime('%y%m%d')}{random.randint(100, 999)}"
            
            new_order = {
                "orderId": order_id,
                "email": email,
                "createdAt": datetime.datetime.now().isoformat(),
                "items": items,
                "totalAmount": order_data.get("totalAmount", 0),
                "status": "pending_payment",
                "recipient": order_data.get("recipient", ""),
                "phone": order_data.get("phone", ""),
                "shippingAddress": order_data.get("address", "")
            }
            
            orders.append(new_order)
            save_orders(orders)
            save_books(books) # 儲存更新後的庫存
            self.send_json({"ok": True, "orderId": order_id})
        except Exception as error:
            self.send_json({"ok": False, "message": f"建立訂單失敗：{error}"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    def handle_update_order_status(self) -> None:
        try:
            data = self.read_json_payload()
            order_id = data.get("orderId")
            new_status = data.get("status")
            
            if not order_id or not new_status:
                self.send_json({"ok": False, "message": "缺少訂單編號或狀態。"}, HTTPStatus.BAD_REQUEST)
                return

            orders = load_orders()
            order = next((o for o in orders if o.get("orderId") == order_id), None)
            
            if not order:
                self.send_json({"ok": False, "message": "找不到該訂單。"}, HTTPStatus.NOT_FOUND)
                return

            # --- 庫存釋放 (若取消訂單) ---
            if new_status == "cancelled" and order.get("status") != "cancelled":
                books = load_books()
                for item in order.get("items", []):
                    book = next((b for b in books if str(b.get("isbn")) == str(item.get("isbn"))), None)
                    if book:
                        book["stock"] = book.get("stock", 0) + item.get("quantity", 0)
                save_books(books)
            # --------------------------

            order["status"] = new_status
            save_orders(orders)
            self.send_json({"ok": True})
        except Exception as error:
            self.send_json({"ok": False, "message": f"更新狀態失敗：{error}"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    def handle_get_orders(self) -> None:
        from urllib.parse import urlparse, parse_qs
        parsed_url = urlparse(self.path)
        params = parse_qs(parsed_url.query)
        email = params.get("email", [""])[0].strip().lower()

        if not email:
            self.send_json({"ok": False, "message": "缺少 Email 參數。"}, HTTPStatus.BAD_REQUEST)
            return

        orders = load_orders()
        user_orders = [o for o in orders if str(o.get("email", "")).lower() == email]
        # Sort by date descending
        user_orders.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
        
        self.send_json({"ok": True, "orders": user_orders})

    def handle_saving_books(self) -> None:
        try:
            data = self.read_json_payload()
            email = str(data.get("email", "")).strip().lower()
            isbn = str(data.get("isbn", "")).strip()
            if not email or not isbn:
                self.send_json({"ok": False, "message": "\u7f3a\u5c11\u6703\u54e1 email \u6216 ISBN\u3002"}, HTTPStatus.BAD_REQUEST)
                return

            members = load_members()
            if not any(str(member.get("email", "")).lower() == email for member in members):
                self.send_json({"ok": False, "message": "\u8acb\u5148\u767b\u5165\u6703\u54e1\u3002"}, HTTPStatus.UNAUTHORIZED)
                return

            records = load_saving_books()
            record = next((item for item in records if str(item.get("email", "")).lower() == email), None)
            if not record:
                record = {"email": email, "isbns": []}
                records.append(record)

            isbns = record.setdefault("isbns", [])
            if isbn not in isbns:
                isbns.append(isbn)
                save_saving_books(records)

            self.send_json({"ok": True, "email": email, "isbns": isbns}, HTTPStatus.CREATED)
        except json.JSONDecodeError:
            self.send_json(
                {"ok": False, "message": "\u9001\u51fa\u7684\u8cc7\u6599\u4e0d\u662f\u6709\u6548 JSON\u3002"},
                HTTPStatus.BAD_REQUEST,
            )
        except Exception as error:
            self.send_json(
                {"ok": False, "message": f"\u5beb\u5165\u6536\u85cf\u66f8\u5931\u6557\uff1a{error}"},
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    def handle_remove_saving_book(self) -> None:
        try:
            data = self.read_json_payload()
            email = str(data.get("email", "")).strip().lower()
            isbn = str(data.get("isbn", "")).strip()
            if not email or not isbn:
                self.send_json({"ok": False, "message": "\u7f3a\u5c11\u6703\u54e1 email \u6216 ISBN\u3002"}, HTTPStatus.BAD_REQUEST)
                return

            records = load_saving_books()
            record = next((item for item in records if str(item.get("email", "")).lower() == email), None)
            if not record:
                self.send_json({"ok": True, "email": email, "isbns": []})
                return

            isbns = [item for item in record.get("isbns", []) if item != isbn]
            record["isbns"] = isbns
            save_saving_books(records)
            self.send_json({"ok": True, "email": email, "isbns": isbns})
        except json.JSONDecodeError:
            self.send_json(
                {"ok": False, "message": "\u9001\u51fa\u7684\u8cc7\u6599\u4e0d\u662f\u6709\u6548 JSON\u3002"},
                HTTPStatus.BAD_REQUEST,
            )
        except Exception as error:
            self.send_json(
                {"ok": False, "message": f"\u79fb\u9664\u6536\u85cf\u66f8\u5931\u6557\uff1a{error}"},
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    def send_json(self, data: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    port = 8000
    server = ThreadingHTTPServer(("localhost", port), BookstoreRequestHandler)
    print(f"Bookstore server running at http://localhost:{port}/")
    server.serve_forever()


if __name__ == "__main__":
    main()
