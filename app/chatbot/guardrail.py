"""Lightweight, rule-based guardrail for the kids' chatbot.

This is a fast pre-check before calling the LLM. It catches obvious off-topic,
personal-info, and unsafe requests in Indonesian. The system prompt provides the
primary topic lock; this guardrail adds a cheap safety net.
"""

from typing import Optional

# Obvious off-topic topics (Indonesian)
_OFF_TOPIC_KEYWORDS = [
    "main game",
    "bermain game",
    "game online",
    "free fire",
    "mobile legend",
    "tugas mtk",
    "tugas matematika",
    "pr matematika",
    "pr bing",
    "coding",
    "program",
    "python",
    "javascript",
    "cuaca hari ini",
    "jam berapa",
    "tanggal berapa",
    "berita terbaru",
]

# Requests that try to extract personal info from the child
_PERSONAL_INFO_KEYWORDS = [
    "alamat rumah",
    "nomor hp",
    "nomor telepon",
    "foto kamu",
    "foto aku",
    "nama lengkap",
    "siapa nama kamu",
    "berapa umur kamu",
    "kirim foto",
    "kirim gambar",
    "kirim lokasi",
    "lokasi kamu",
]

# Unsafe real-world meetup / contact requests
_UNSAFE_KEYWORDS = [
    "bertemu",
    "ketemuan",
    "ketemu",
    "jumpa",
    "main bareng",
    "jalan bareng",
]


def is_off_topic(user_input: str) -> bool:
    text = user_input.lower()
    return any(k in text for k in _OFF_TOPIC_KEYWORDS)


def requests_personal_info(user_input: str) -> bool:
    text = user_input.lower()
    return any(k in text for k in _PERSONAL_INFO_KEYWORDS)


def is_unsafe(user_input: str) -> bool:
    text = user_input.lower()
    return any(k in text for k in _UNSAFE_KEYWORDS)


def guardrail_check(user_input: str, module_name: str) -> Optional[str]:
    """Return a canned redirect if the input fails lightweight checks.

    Returns None if the input is allowed to pass to the LLM.
    """
    if requests_personal_info(user_input) or is_unsafe(user_input):
        return (
            "Aku tidak boleh meminta atau menerima informasi pribadi, "
            "dan aku tidak bisa membahas pertemuan dengan orang asing. "
            f"Yuk, kita fokus belajar tentang {module_name} saja."
        )
    if is_off_topic(user_input):
        return (
            f"Maaf, aku hanya bisa membahas {module_name}. "
            "Yuk, kita fokus belajar!"
        )
    return None
