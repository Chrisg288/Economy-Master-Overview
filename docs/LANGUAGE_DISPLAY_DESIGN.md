# Language Display Design

The interface should eventually allow the user to select a display language independently of the vendor/source language.

Each normalized record supports:

```json
{
  "source_language": "English",
  "translations": {
    "en": {"item_name": "...", "description": "..."},
    "fr": {"item_name": "...", "description": "..."}
  }
}
```

Display order for a requested language:

1. Human-reviewed translation.
2. Trusted machine translation stored with provenance and date.
3. Source text with a visible fallback-language indicator.

Do not silently label untranslated source text as translated.
