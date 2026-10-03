"""User-curated contact book (Chunk A — Contacts Core).

A dedicated, fully user-managed address book, separate from the auto-extracted
"People around you" list (the soft-disabled Curator's ``data/workspace/people/``).
Each contact is one ``<slug>.md`` file (YAML frontmatter + Markdown README) under
``user_data_dir()/data/contacts/``.

Public surface (Contract 1, consumed by Chunk B — do not change signatures):

- :class:`chappie.contacts.store.Contact`
- :class:`chappie.contacts.store.ContactStore`
- the ``relationship`` enum source of truth in :mod:`chappie.contacts.schema`
"""
from __future__ import annotations

from .schema import RELATIONSHIPS, Relationship
from .store import Contact, ContactStore

__all__ = ["Contact", "ContactStore", "RELATIONSHIPS", "Relationship"]
