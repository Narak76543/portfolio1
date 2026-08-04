import json
import urllib.request

API_BASE = "http://localhost:8000/api/v1"

def main():
    # 1. Login with JSON payload
    data = json.dumps({"email": "admin@saratnarak.com", "password": "Admin123456!"}).encode('utf-8')
    req = urllib.request.Request(
        f"{API_BASE}/auth/login",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read().decode())
            token = body["access_token"]
            print("1. Admin login success! Token obtained.")
    except Exception as e:
        print("Login failed:", e)
        return

    # 2. Test fetching project by UUID ID
    proj_id = "c99f93e2-e98e-4dfb-b21d-7c4d17f74f28"
    req_proj = urllib.request.Request(f"{API_BASE}/projects/{proj_id}", headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req_proj) as resp:
            proj = json.loads(resp.read().decode())
            print(f"2. GET /projects/{proj_id} success! Title: '{proj['title']}', display_order={proj['display_order']}, featured={proj['featured']}")
    except Exception as e:
        print("GET project by ID failed:", e)

    # 3. Test listing projects
    req_list = urllib.request.Request(f"{API_BASE}/projects")
    with urllib.request.urlopen(req_list) as resp:
        projects = json.loads(resp.read().decode())
        print(f"3. GET /projects success! Returned {len(projects)} projects:")
        for p in projects:
            print(f"   - [Order {p['display_order']}] '{p['title']}' (slug: {p['slug']}, featured={p['featured']}, cover={p['cover_image_url']})")

if __name__ == "__main__":
    main()
