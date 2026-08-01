import tkinter as tk

from .. import theme as th
from .. import icons
from .. import fx
from .. import services
from ..widgets import (AuroraCanvas, RoundedButton, StatCard, TextField,
                       ScrollArea, EntryCard, EmptyState)
from .base import Screen
from .login import LoginScreen
from .modals import AddEntryModal, ConfirmModal


class DashboardScreen(Screen):
    def _build(self):
        self.entries = services.decrypt_entries(services.load_vault(), self.app.key)
        self._build_hero()
        self._build_content()
        self._rebuild_list()

    # ---------------------------------------------------------------- hero
    def _build_hero(self):
        self.hero = AuroraCanvas(self.frame, bg=th.BG)
        self.hero.config(height=178)
        self.hero.pack(side="top", fill="x")

        brand_icon = tk.Canvas(self.hero, width=44, height=44, bg=th.BG,
                               highlightthickness=0, bd=0)
        brand_icon.place(x=28, y=18)
        fx.round_rect(brand_icon, 2, 2, 42, 42, 20,
                      fill=th.lerp_color(th.ACCENT, th.BG, 0.55), outline="")
        icons.draw("lock", brand_icon, 22, 22, 17, th.TEXT)
        tk.Label(self.hero, text="RunesCrypt", bg=th.BG, fg=th.TEXT,
                 font=th.F(18, "bold")).place(x=78, y=20)
        tk.Label(self.hero, text="Protected vault • AES-256",
                 bg=th.BG, fg=th.MUTED, font=th.F(10)).place(x=78, y=46)

        name = (self.app.login or "there").strip()
        tk.Label(self.hero, text=f"Hi, {name}", bg=th.BG, fg=th.TEXT,
                 font=th.F(24, "bold")).place(x=28, y=86)
        tk.Label(self.hero, text="Welcome back to your encrypted vault",
                 bg=th.BG, fg=th.MUTED, font=th.F(12)).place(x=28, y=122)

        self.avatar = tk.Canvas(self.hero, width=40, height=40, bg=th.BG,
                                highlightthickness=0, bd=0)
        self.avatar.place(x=0, y=18)
        self._draw_avatar()

        self.btn_logout = RoundedButton(self.hero, "Log out", self._logout,
                                        variant="secondary", height=40, icon="logout",
                                        bg=th.BG, width=118, font_size=13)
        self.btn_logout.place(x=0, y=18)
        self.hero.bind("<Configure>", self._layout_hero)

    def _draw_avatar(self):
        self.avatar.delete("all")
        icons.avatar(self.avatar, 20, 20, 17, self.app.login or "?",
                     th.avatar_color(self.app.login), "#ffffff", th.F(15, "bold"))

    def _layout_hero(self, e=None):
        w = self.hero.winfo_width()
        if w <= 1:
            return
        self.btn_logout.place_configure(x=w - 24, y=18, anchor="ne")
        self.avatar.place_configure(x=w - 158, y=18)

    # -------------------------------------------------------------- content
    def _build_content(self):
        self.content = tk.Frame(self.frame, bg=th.BG)
        self.content.pack(fill="both", expand=True, padx=28, pady=(20, 10))

        self.stats = tk.Frame(self.content, bg=th.BG)
        self.stats.pack(fill="x", pady=(2, 8))
        self.stat_total = StatCard(self.stats, "key", "0", "Total passwords",
                                   th.ACCENT, bg=th.BG)
        self.stat_platforms = StatCard(self.stats, "shield", "0", "Platforms",
                                       th.TEAL, bg=th.BG)
        self.stat_crypto = StatCard(self.stats, "lock", "AES-256", "Encryption",
                                    th.WARNING, bg=th.BG)
        for s in (self.stat_total, self.stat_platforms, self.stat_crypto):
            s.pack(side="left", fill="x", expand=True, padx=5)

        self.action_row = tk.Frame(self.content, bg=th.BG)
        self.action_row.pack(fill="x", pady=(10, 12))
        tk.Label(self.action_row, text="Stored credentials", bg=th.BG, fg=th.TEXT,
                 font=th.F(14, "bold")).pack(side="left")
        self.search = TextField(self.action_row, placeholder="Search your passwords…",
                                bg=th.BG, on_change=lambda e: self._on_search())
        self.search.pack(side="left", fill="x", expand=True, padx=(12, 12))
        self.btn_add = RoundedButton(self.action_row, "Add password", self._add,
                                     variant="primary", height=52, icon="plus", bg=th.BG, width=170)
        self.btn_add.pack(side="right")

        self.list_holder = tk.Frame(self.content, bg=th.BG)
        self.list_holder.pack(fill="both", expand=True)

        self._update_stats()

    def _update_stats(self):
        self.stat_total.set_value(len(self.entries))
        self.stat_platforms.set_value(len({e["platform name"].lower() for e in self.entries}))
        self.stat_crypto.set_value("AES-256")

    def _query(self):
        try:
            return self.search.value.strip().lower()
        except tk.TclError:
            return ""

    def _on_search(self):
        self._rebuild_list()

    def _rebuild_list(self):
        for child in self.list_holder.winfo_children():
            child.destroy()
        self.scroll = None

        if not self.entries:
            EmptyState(self.list_holder, icon="key", title="Your vault is empty",
                       subtitle="Add your first password to get started",
                       action_text="Add your first password", on_action=self._add,
                       bg=th.BG).pack(fill="both", expand=True)
            return

        q = self._query()
        shown = [(idx, e) for idx, e in enumerate(self.entries)
                 if not q or q in (e["platform name"].lower() or e["email or user name"].lower())]

        self.scroll = ScrollArea(self.list_holder, bg=th.BG)
        self.scroll.pack(fill="both", expand=True)

        if not shown:
            EmptyState(self.scroll.inner, icon="search", title="No matches",
                       subtitle=f"No entry matches \u201c{self.search.value.strip()}\u201d",
                       bg=th.BG).pack(fill="both", expand=True, pady=30)
            return

        for n, (idx, e) in enumerate(shown):
            if n % 2 == 0:
                row = tk.Frame(self.scroll.inner, bg=th.BG)
                row.pack(fill="x")
            card = EntryCard(
                row,
                platform=e["platform name"],
                email=e["email or user name"],
                password=e["password"],
                index=idx,
                color=th.avatar_color(e["platform name"]),
                on_copy_email=self._copy_email,
                on_copy_password=self._copy_password,
                on_edit=self._edit,
                on_delete=self._delete,
                scrollarea=self.scroll,
                bg=th.BG,
            )
            card.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        self.scroll.scroll_top()

    # ------------------------------------------------------------- actions
    def _add(self):
        AddEntryModal(self.app, key=self.app.key, on_saved=self.reload)

    def _edit(self, card):
        AddEntryModal(self.app, key=self.app.key, index=card.index,
                      platform=card.platform, email=card.email, password=card.password,
                      on_saved=self.reload)

    def _delete(self, card):
        def confirm():
            services.delete_entry(card.index)
            self.reload()
            self.app.toast("Password deleted", "info")

        ConfirmModal(self.app, title="Delete this password?",
                     message=f"\u201c{card.platform}\u201d will be permanently removed from your vault.",
                     confirm_text="Delete", on_confirm=confirm)

    def _copy_email(self, card):
        self.app.copy(card.email, "Email copied")

    def _copy_password(self, card):
        self.app.copy(card.password, "Password copied")

    def reload(self):
        self.entries = services.decrypt_entries(services.load_vault(), self.app.key)
        self._update_stats()
        self._rebuild_list()

    def _logout(self):
        self.app.key = None
        self.app.login = None
        self.app.transition(LoginScreen)
