import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict


@dataclass(frozen=True)
class ChatbotModule:
    """Static knowledge for one learning topic.

    No database is needed: the FAQ and system prompt are bundled as files.
    """

    slug: str
    name: str
    faqs: list[dict]
    system_prompt_template: str

    @property
    def faq_text(self) -> str:
        """FAQ formatted for injection into the system prompt."""
        return "\n\n".join(
            f"{i}. Q: {item['q']}\n   A: {item['a']}"
            for i, item in enumerate(self.faqs, start=1)
        )

    @property
    def system_prompt(self) -> str:
        return self.system_prompt_template.format(faq_text=self.faq_text)

    @property
    def faq_intro(self) -> str:
        """Friendly first message shown in the FAQ popup/chat intro."""
        lines = [
            f"Halo! Aku SiBot, teman belajarmu untuk topik {self.name}.",
            "",
            "Berikut FAQ yang sering ditanyakan:",
        ]
        for i, item in enumerate(self.faqs, start=1):
            lines.append(f"{i}. {item['q']}")
        lines.append("")
        lines.append(
            f"Kalau ada yang mau ditanyakan, langsung tanya ya! "
            f"Aku akan membahas seputar {self.name} saja."
        )
        return "\n".join(lines)


def _load_module(slug: str, name: str) -> ChatbotModule:
    base_dir = Path(__file__).parent
    faq_path = base_dir / "faqs" / f"{slug}.json"
    prompt_path = base_dir / "prompts" / f"{slug}.txt"

    with open(faq_path, encoding="utf-8") as f:
        faqs = json.load(f)

    with open(prompt_path, encoding="utf-8") as f:
        template = f.read()

    return ChatbotModule(slug=slug, name=name, faqs=faqs, system_prompt_template=template)


MODULES: Dict[str, ChatbotModule] = {
    "data_online": _load_module("data_online", "Lindungi Data di Internet"),
    "financial": _load_module("financial", "Keamanan Finansial"),
    "personal_safety": _load_module("personal_safety", "Keselamatan Personal"),
}


def get_module(slug: str) -> ChatbotModule:
    if slug not in MODULES:
        raise ValueError(
            f"Unknown module slug: {slug}. Available: {list(MODULES.keys())}"
        )
    return MODULES[slug]
