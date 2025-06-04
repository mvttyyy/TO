class ConsoleView:
    def show_media_page(self, books, page=0, page_size=10):
        total = len(books)
        total_pages = (total - 1) // page_size + 1
        start = page * page_size
        end = min(start + page_size, total)
        print(f"\n=== LISTA MEDIÓW (strona {page+1}/{total_pages}) ===")
        for idx, b in enumerate(books[start:end], start + 1):
            print(f"{idx}. {b.title} ({b.status})")
        print("[n]astępna, [p]oprzednia, [q] powrót do menu")

    def show_media_list(self, books):
        # jeśli chcemy bez paginacji
        print("\n=== LISTA MEDIÓW ===")
        for idx, b in enumerate(books, 1):
            print(f"{idx}. {b.title} ({b.status})")

    def prompt(self, msg):
        return input(msg)

    def prompt_index(self, msg, max_idx):
        while True:
            try:
                # use the existing prompt() to read input
                idx = int(self.prompt(msg))
                if 1 <= idx <= max_idx:
                    return idx - 1
            except ValueError:
                pass
            self.show_message(f"Podaj prawidłowy numer (1–{max_idx})")

    def show_message(self, msg):
        print(msg)