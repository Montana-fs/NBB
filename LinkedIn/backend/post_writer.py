import os
import anthropic
from backend.config import SYSTEM_PROMPT


def write_post(article, usp, language):
    api_key = os.getenv("ANTHROPIC_API_KEY")

    lang_label = {"da": "dansk", "en": "English", "de": "Deutsch", "sv": "svenska"}.get(language, language)
    usp_text = usp[language]

    if article.get("manual"):
        user_message = f"""Emne eller begivenhed: {article['title']}

Denne uges USP: {usp_text}
Skriv opslaget på: {lang_label}

Dette er et manuelt angivet emne — brug det som udgangspunkt for opslaget. Introducer emnet naturligt og sæt NBB i relation til det. Der er ingen ekstern nyhedskilde at linke til.

Skriv LinkedIn-opslaget nu."""
    else:
        user_message = f"""Aktuel nyhed:
Titel: {article['title']}
Kilde: {article['source']}
Resumé: {article['summary']}
Link: {article['url']}

Denne uges USP: {usp_text}
Skriv opslaget på: {lang_label}

Skriv LinkedIn-opslaget nu."""

    if not api_key:
        return _mock_post(article, usp_text, language)

    client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_message}],
    )

    return response.content[0].text


def _mock_post(article, usp_text, language):
    if language == "da":
        return f"""En ny rapport sætter fokus på det vi hos NBB arbejder med hver eneste dag: at gøre industriel emballage til en del af løsningen, ikke en del af problemet.

{article['title']}

Det bekræfter en stigende tendens i industrien — virksomheder efterspørger nu aktivt emballage der understøtter cirkulær økonomi. Hos NBB har vi allerede svaret klar.

{usp_text}

Bigbags er ikke bare opbevaring. Det er et valg om, hvilken type industri vi vil være en del af.

Er du nysgerrig på, hvad den rette bigbag-løsning kan gøre for din virksomhed? Skriv til os — vi rådgiver gerne.

#bigbags #cirkulærøkonomi #grønomstilling #bæredygtigindustri #NBB

[MOCK — ingen API-nøgle fundet]"""
    else:
        return f"""A new report highlights exactly what we at NBB work with every day: making industrial packaging part of the solution, not the problem.

{article['title']}

This confirms a growing trend — companies are now actively seeking packaging that supports the circular economy. At NBB, we already have the answer.

{usp_text}

Bigbags are not just storage. They are a choice about what kind of industry we want to be part of.

Curious about what the right bigbag solution can do for your business? Reach out — we are happy to advise.

#bigbags #circulareconomy #greentransition #sustainableindustry #NBB

[MOCK — no API key found]"""
