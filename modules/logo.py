"""
modules/logo.py
"""

import base64
import os


def _load_logo_b64() -> tuple[str, str]:
    candidates = [
        "valuemomentum_logo.png",
        "valuemomentum_logo.jpg",
        "valuemomentum_logo.jpeg",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "valuemomentum_logo.png"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "valuemomentum_logo.jpg"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "valuemomentum_logo.jpeg"),
    ]
    for path in candidates:
        if os.path.exists(path):
            ext  = os.path.splitext(path)[1].lower()
            mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode(), mime
    return "", ""


LOGO_B64, LOGO_MIME = _load_logo_b64()


def logo_img_tag(height: int = 38) -> str:
    if not LOGO_B64:
        return ""
    return (
        f'<img src="data:{LOGO_MIME};base64,{LOGO_B64}" '
        f'style="height:{height}px;margin-right:14px;vertical-align:middle;'
        f'border-radius:4px;background:#1e1e2e;padding:3px 6px;" />'
    )
