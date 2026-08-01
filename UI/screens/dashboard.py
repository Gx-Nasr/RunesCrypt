from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from .. import theme as th
from ..widgets import (AvatarWidget, Button, EmptyState, EntryCard, Field,
                       ScrollArea, StatCard)
from .base import Screen
from .auth import Brand


class HeroBar(QWidget):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedHeight(148)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 18, 0, 0)
        lay.setSpacing(0)

        row = QHBoxLayout()
        row.setSpacing(12)
        brand = Brand(self, 40)
        row.addWidget(brand)
        name_lbl = QLabel("RunesCrypt", self)
        name_lbl.setFont(th.font(17, "heavy"))
        name_lbl.setStyleSheet(f"""
                    color: {th.TEXT.name()};
                    background-color: transparent;
                """)
        row.addWidget(name_lbl)
        row.addStretch(1)

        self.btn_logout = Button(self, "Log out", self._logout, variant="secondary",
                                 height=40, radius=12, icon="logout", font_size=13,
                                 bg=th.BG)
        self.btn_logout.setFixedWidth(128)
        row.addWidget(self.btn_logout)
        lay.addLayout(row)

        lay.addStretch(1)

        who = (self.app.login or "there").strip()
        greet = QLabel(f"Hi, {who}", self)
        greet.setFont(th.font(26, "heavy"))
        greet.setStyleSheet(f"""
                    color: {th.TEXT.name()};
                    background-color: transparent;
                """)
        lay.addWidget(greet)
        sub = QLabel("Welcome back to your encrypted vault", self)
        sub.setFont(th.font(12))
        sub.setStyleSheet(f"""
                    color: {th.TEXT.name()};
                    background-color: transparent;
                """)
        lay.addWidget(sub)
        lay.addSpacing(14)

    def _logout(self):
        self.app.key = None
        self.app.login = None
        from .login import LoginScreen
        self.app.transition(LoginScreen)


class DashboardScreen(Screen):
    def build(self):
        self.entries = self.app.services.decrypt_entries(
            self.app.services.load_vault(), self.app.key)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 0, 28, 18)
        lay.setSpacing(0)

        self.hero = HeroBar(self, self.app)
        lay.addWidget(self.hero)

        self.content = QVBoxLayout()
        self.content.setSpacing(0)

        stats = QHBoxLayout()
        stats.setSpacing(12)
        self.stat_total = StatCard(self, "key", "0", "Total passwords", th.ACCENT)
        self.stat_platforms = StatCard(self, "shield", "0", "Platforms", th.TEAL)
        self.stat_crypto = StatCard(self, "lock", "AES-256", "Encryption", th.WARNING)
        for s in (self.stat_total, self.stat_platforms, self.stat_crypto):
            stats.addWidget(s, 1)
        self.content.addLayout(stats)
        self.content.addSpacing(16)

        action = QHBoxLayout()
        action.setSpacing(12)
        self.search = Field(self, "", placeholder="Search your passwords\u2026",
                            on_change=lambda t: self._rebuild_list())
        action.addWidget(self.search, 1)
        self.btn_add = Button(self, "Add password", self._add, variant="primary",
                              height=54, radius=14, icon="plus", font_size=14)
        self.btn_add.setFixedWidth(180)
        action.addWidget(self.btn_add)
        self.content.addLayout(action)
        self.content.addSpacing(6)

        self.content.addWidget(self._scroll_holder(), 1)

        lay.addLayout(self.content, 1)
        self._update_stats()
        self._rebuild_list()

    def _scroll_holder(self):
        self.scroll_area = ScrollArea(self)
        return self.scroll_area

    def _update_stats(self):
        self.stat_total.set_value(len(self.entries))
        self.stat_platforms.set_value(len({e["platform name"].lower() for e in self.entries}))

    def _query(self):
        try:
            return self.search.value.strip().lower()
        except Exception:
            return ""

    def _rebuild_list(self):
        self.scroll_area.clear()
        if not self.entries:
            es = EmptyState(self.scroll_area, icon="key", title="Your vault is empty",
                            subtitle="Add your first password to get started",
                            action_text="Add your first password", on_action=self._add)
            self.scroll_area.vbox.addWidget(es, 1)
            return

        q = self._query()
        shown = [(i, e) for i, e in enumerate(self.entries)
                 if not q or q in (e["platform name"].lower() or e["email or user name"].lower())]

        if not shown:
            es = EmptyState(self.scroll_area, icon="search", title="No matches",
                            subtitle=f"No entry matches \u201c{self.search.value.strip()}\u201d")
            self.scroll_area.vbox.addWidget(es, 1)
            return

        for i in range(0, len(shown), 2):
            row = QWidget()
            row.setAttribute(Qt.WA_TranslucentBackground)
            hl = QHBoxLayout(row)
            hl.setContentsMargins(0, 0, 0, 0)
            hl.setSpacing(12)
            for idx, e in shown[i:i + 2]:
                card = EntryCard(
                    row, platform=e["platform name"], email=e["email or user name"],
                    password=e["password"], index=idx,
                    color=th.avatar_color(e["platform name"]),
                    on_copy_email=self._copy_email, on_copy_password=self._copy_password,
                    on_edit=self._edit, on_delete=self._delete)
                hl.addWidget(card, 1)
            hl.addStretch(0)
            self.scroll_area.vbox.addWidget(row)

    # ------------------------------------------------------------- actions
    def _add(self):
        from .modals import AddEntryModal
        AddEntryModal(self.app, key=self.app.key, on_saved=self.reload)

    def _edit(self, card):
        from .modals import AddEntryModal
        AddEntryModal(self.app, key=self.app.key, index=card.index,
                      platform=card.platform, email=card.email, password=card.password,
                      on_saved=self.reload)

    def _delete(self, card):
        def confirm():
            self.app.services.delete_entry(card.index)
            self.reload()
            self.app.toast("Password deleted", "info")

        from .modals import ConfirmModal
        ConfirmModal(self.app, title="Delete this password?",
                     message=f"\u201c{card.platform}\u201d will be permanently removed from your vault.",
                     confirm_text="Delete", on_confirm=confirm)

    def _copy_email(self, card):
        self.app.copy(card.email, "Email copied")

    def _copy_password(self, card):
        self.app.copy(card.password, "Password copied")

    def reload(self):
        self.entries = self.app.services.decrypt_entries(
            self.app.services.load_vault(), self.app.key)
        self._update_stats()
        self._rebuild_list()
