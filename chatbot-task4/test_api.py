import json
import urllib.request


def main() -> None:
    data = json.dumps({"message": "pricing"}).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:5000/api/chat",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        print(resp.status)
        print(resp.read().decode("utf-8"))


if __name__ == "__main__":
    main()

