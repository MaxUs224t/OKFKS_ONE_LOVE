import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

from cipher.caesar import shift_text as caesar
from cipher.vigenere import transform_text as vigenere
from cipher.transposition import encrypt as trans_encrypt, decrypt as trans_decrypt
from utils.file_manager import read_text_file, write_text_file


# Тексты интерфейса для двух языков
TEXTS = {
    "ru": {
        "title": "Шифратор",
        "method": "Метод:", "key": "Ключ:",
        "input": "Исходный текст:", "result": "Результат:",
        "encrypt": "Зашифровать", "decrypt": "Расшифровать",
        "load": "Загрузить .txt", "copy": "Копировать",
        "save": "Сохранить .txt", "clear": "Очистить",
        "help_hint": "F1 — справка", "help": "Справка",
        "learning": "Обучение", "docs": "Документация", "about": "О программе",
        "example": "Например: ",
        "caesar": "Шифр Цезаря", "vigenere": "Шифр Виженера", "transposition": "Транспозиция",
        "caesar_key": "3", "vigenere_key": "СЕКРЕТ", "transposition_key": "4",
        "empty_text": "Введите текст для обработки.",
        "empty_key": "Укажите ключ.",
        "bad_caesar": "Ключ Цезаря должен быть целым числом.",
        "bad_vigenere": "Ключ Виженера должен содержать только буквы русского или английского алфавита.",
        "bad_transposition": "Ключ транспозиции должен быть положительным целым числом.",
        "file_error": "Не удалось прочитать файл. Поддерживается только UTF-8.",
        "save_error": "Не удалось сохранить файл.",
        "loaded": "Файл загружен.", "copied": "Результат скопирован.", "saved": "Файл сохранён.",
        "clear_q": "Очистить исходный текст и результат?",
        "exit_q": "Результат ещё не сохранён. Выйти?",
        "replace_q": "Заменить текущий текст содержимым файла?",
        "yes": "Да", "no": "Нет", "ok": "OK",
        "error": "Ошибка", "info": "Готово",
        "about_text": "Шифратор\nУчебное программное средство\n\nЯзык: Python\nGUI: Tkinter\nОС: Windows\n\nАвтор: Кощеев Максим Сергеевич\nГруппа: ИСП-324т\n\nВерсия: 1.0",
        "learning_text": (
            "Шифр Цезаря\n"
            "Каждая буква сдвигается по своему алфавиту на число позиций, указанное ключом.\n"
            "Пример: текст «ПРИВЕТ», ключ 3.\n\n"
            "Шифр Виженера\n"
            "Каждая буква получает сдвиг из буквенного ключа. Ключ повторяется по мере чтения текста.\n"
            "Пример: текст «ПРИВЕТ», ключ «СЕКРЕТ».\n\n"
            "Столбцовая транспозиция\n"
            "Символы записываются по строкам в таблицу, а затем читаются по столбцам.\n"
            "Ключ задаёт количество столбцов. Символы не заменяются, меняется только их порядок."
        ),
        "docs_text": (
            "Назначение\n"
            "Учебный шифратор предназначен для демонстрации трёх простых способов обработки текста.\n\n"
            "Работа с программой\n"
            "1. Выберите метод в выпадающем списке.\n"
            "2. Введите ключ по подсказке.\n"
            "3. Введите текст или загрузите UTF-8 TXT.\n"
            "4. Нажмите «Зашифровать» или «Расшифровать».\n"
            "5. Результат можно скопировать или сохранить в TXT.\n\n"
            "Поддерживаются русский и английский алфавиты. Цифры и знаки препинания сохраняются.\n"
            "Программа является учебной и не предназначена для реальной защиты конфиденциальных данных."
        ),
    },
    "en": {
        "title": "Cipher",
        "method": "Method:", "key": "Key:",
        "input": "Input text:", "result": "Result:",
        "encrypt": "Encrypt", "decrypt": "Decrypt",
        "load": "Load .txt", "copy": "Copy",
        "save": "Save .txt", "clear": "Clear",
        "help_hint": "F1 — help", "help": "Help",
        "learning": "Learning", "docs": "Documentation", "about": "About",
        "example": "Example: ",
        "caesar": "Caesar cipher", "vigenere": "Vigenere cipher", "transposition": "Transposition",
        "caesar_key": "3", "vigenere_key": "SECRET", "transposition_key": "4",
        "empty_text": "Enter text to process.",
        "empty_key": "Enter a key.",
        "bad_caesar": "The Caesar key must be an integer.",
        "bad_vigenere": "The Vigenere key must contain only Russian or English letters.",
        "bad_transposition": "The transposition key must be a positive integer.",
        "file_error": "The file could not be read. Only UTF-8 is supported.",
        "save_error": "The file could not be saved.",
        "loaded": "File loaded.", "copied": "Result copied.", "saved": "File saved.",
        "clear_q": "Clear input text and result?",
        "exit_q": "The result has not been saved. Exit?",
        "replace_q": "Replace current text with the file contents?",
        "yes": "Yes", "no": "No", "ok": "OK",
        "error": "Error", "info": "Done",
        "about_text": "Cipher\nEducational software\n\nLanguage: Python\nGUI: Tkinter\nOS: Windows\n\nAuthor: Koshcheev Maxim Sergeevich \nGroup: ISP-324t\n\nVersion: 1.0",
        "learning_text": (
            "Caesar cipher\n"
            "Each letter is shifted inside its alphabet by the number given as the key.\n"
            "Example: text «HELLO», key 3.\n\n"
            "Vigenere cipher\n"
            "Each letter receives a shift from the letter key. The key repeats as the text is read.\n"
            "Example: text «HELLO», key «SECRET».\n\n"
            "Columnar transposition\n"
            "Characters are written into a table by rows and then read by columns.\n"
            "The key sets the number of columns. Characters are not replaced, only reordered."
        ),
        "docs_text": (
            "Purpose\n"
            "The educational cipher demonstrates three simple ways to transform text.\n\n"
            "How to use\n"
            "1. Select a method.\n"
            "2. Enter the key shown in the hint.\n"
            "3. Enter text or load a UTF-8 TXT file.\n"
            "4. Click Encrypt or Decrypt.\n"
            "5. Copy or save the result as TXT.\n\n"
            "Russian and English alphabets are supported. Digits and punctuation are preserved.\n"
            "This program is educational and is not intended for real confidential data protection."
        ),
    },
}


# Entry с подсказкой внутри поля
class PlaceholderEntry(ttk.Entry):
    def __init__(self, master, placeholder="", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self._showing = False

        self.bind("<FocusIn>", self._focus_in)
        self.bind("<FocusOut>", self._focus_out)

        self.show_placeholder()

    def show_placeholder(self):
        if not self.get():
            self.insert(0, self.placeholder)
            self.configure(foreground="#777777")
            self._showing = True

    def _focus_in(self, _event=None):
        if self._showing:
            self.delete(0, tk.END)
            self.configure(foreground="")
            self._showing = False

    def _focus_out(self, _event=None):
        if not self.get():
            self.show_placeholder()

    def real_value(self):
        # Не возвращаем сам placeholder как ключ
        return "" if self._showing else self.get().strip()

    def set_placeholder(self, value):
        self.placeholder = value

        if self._showing:
            self.delete(0, tk.END)
            self.insert(0, value)


# Окно справки
class HelpWindow(tk.Toplevel):
    def __init__(self, master, lang_getter):
        super().__init__(master)

        self.master_window = master
        self.lang_getter = lang_getter

        self.title(TEXTS[lang_getter()]["help"])
        self.geometry("760x520")
        self.minsize(600, 420)
        self.protocol("WM_DELETE_WINDOW", self.close)

        # Вкладки справки
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=12)

        self.learning_frame = ttk.Frame(self.notebook, padding=12)
        self.docs_frame = ttk.Frame(self.notebook, padding=12)
        self.about_frame = ttk.Frame(self.notebook, padding=12)

        self.notebook.add(self.learning_frame, text="")
        self.notebook.add(self.docs_frame, text="")
        self.notebook.add(self.about_frame, text="")

        self.learning_label = tk.Text(
            self.learning_frame,
            wrap="word",
            relief="flat",
            font=("Segoe UI", 11)
        )
        self.learning_label.pack(fill="both", expand=True)

        self.docs_label = tk.Text(
            self.docs_frame,
            wrap="word",
            relief="flat",
            font=("Segoe UI", 11)
        )
        self.docs_label.pack(fill="both", expand=True)

        self.about_label = tk.Label(
            self.about_frame,
            justify="left",
            anchor="nw",
            font=("Segoe UI", 11)
        )
        self.about_label.pack(fill="both", expand=True)

        self.update_texts()

        # Окно поверх основного
        self.transient(master)
        self.grab_set()

    def update_texts(self):
        t = TEXTS[self.lang_getter()]

        self.title(t["help"])
        self.notebook.tab(0, text=t["learning"])
        self.notebook.tab(1, text=t["docs"])
        self.notebook.tab(2, text=t["about"])

        # Text временно разблокируем для обновления
        for widget, key in (
            (self.learning_label, "learning_text"),
            (self.docs_label, "docs_text")
        ):
            widget.configure(state="normal")
            widget.delete("1.0", tk.END)
            widget.insert("1.0", t[key])
            widget.configure(state="disabled")

        self.about_label.configure(text=t["about_text"])

    def close(self):
        self.master_window.help_window = None
        self.destroy()


# Главное окно программы
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.lang = "ru"
        self.help_window = None
        self.current_file = None

        self.title(TEXTS[self.lang]["title"])

        # Иконка лежит рядом с main.py
        try:
            self.iconbitmap(
                str(Path(__file__).resolve().parent.parent / "shifrator.ico")
            )
        except tk.TclError:
            pass

        self.geometry("900x650")
        self.minsize(760, 560)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind_all("<F1>", self.open_help)

        self._make_widgets()
        self.update_language()

    def _make_widgets(self):
        # Основной контейнер
        root = ttk.Frame(self, padding=16)
        root.pack(fill="both", expand=True)
        root.columnconfigure(0, weight=1)

        # Заголовок и выбор языка
        top = ttk.Frame(root)
        top.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        top.columnconfigure(0, weight=1)

        self.title_label = ttk.Label(top, font=("Segoe UI", 18, "bold"))
        self.title_label.grid(row=0, column=0, sticky="w")

        self.lang_combo = ttk.Combobox(
            top,
            values=["Русский", "English"],
            state="readonly",
            width=12
        )
        self.lang_combo.grid(row=0, column=1, sticky="e")
        self.lang_combo.bind("<<ComboboxSelected>>", self.change_language)

        # Выбор метода
        self.method_label = ttk.Label(root)
        self.method_label.grid(row=1, column=0, sticky="w")

        self.method_combo = ttk.Combobox(
            root,
            state="readonly",
            width=35
        )
        self.method_combo.grid(row=2, column=0, sticky="ew", pady=(2, 8))
        self.method_combo.bind("<<ComboboxSelected>>", self.change_method)

        # Ключ
        self.key_label = ttk.Label(root)
        self.key_label.grid(row=3, column=0, sticky="w")

        self.key_entry = PlaceholderEntry(root, width=35)
        self.key_entry.grid(row=4, column=0, sticky="ew", pady=(2, 8))

        # Заголовок исходного текста + загрузка файла
        input_head = ttk.Frame(root)
        input_head.grid(row=5, column=0, sticky="ew")
        input_head.columnconfigure(0, weight=1)

        self.input_label = ttk.Label(input_head)
        self.input_label.grid(row=0, column=0, sticky="w")

        self.load_button = ttk.Button(input_head, command=self.load_file)
        self.load_button.grid(row=0, column=1, sticky="e")

        # Поле исходного текста
        input_frame = ttk.Frame(root)
        input_frame.grid(row=6, column=0, sticky="nsew", pady=(2, 8))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)

        self.input_text = tk.Text(
            input_frame,
            wrap="word",
            undo=True,
            font=("Segoe UI", 10)
        )
        self.input_text.grid(row=0, column=0, sticky="nsew")

        self.input_scroll = ttk.Scrollbar(
            input_frame,
            orient="vertical",
            command=self.input_text.yview
        )
        self.input_scroll.grid(row=0, column=1, sticky="ns")
        self.input_text.configure(yscrollcommand=self.input_scroll.set)

        # Кнопки обработки
        actions = ttk.Frame(root)
        actions.grid(row=7, column=0, sticky="ew", pady=(0, 8))

        self.encrypt_button = ttk.Button(
            actions,
            command=lambda: self.process(False)
        )
        self.encrypt_button.pack(side="left", padx=(0, 8))

        self.decrypt_button = ttk.Button(
            actions,
            command=lambda: self.process(True)
        )
        self.decrypt_button.pack(side="left")

        # Заголовок результата
        result_head = ttk.Frame(root)
        result_head.grid(row=8, column=0, sticky="ew")

        self.result_label = ttk.Label(result_head)
        self.result_label.pack(side="left")

        # Поле результата
        result_frame = ttk.Frame(root)
        result_frame.grid(row=9, column=0, sticky="nsew", pady=(2, 8))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

        self.result_text = tk.Text(
            result_frame,
            wrap="word",
            undo=True,
            font=("Segoe UI", 10)
        )
        self.result_text.grid(row=0, column=0, sticky="nsew")

        self.result_scroll = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=self.result_text.yview
        )
        self.result_scroll.grid(row=0, column=1, sticky="ns")
        self.result_text.configure(yscrollcommand=self.result_scroll.set)

        # Нижние кнопки
        bottom = ttk.Frame(root)
        bottom.grid(row=10, column=0, sticky="ew")

        self.copy_button = ttk.Button(
            bottom,
            command=self.copy_result
        )
        self.copy_button.pack(side="left", padx=(0, 8))

        self.save_button = ttk.Button(
            bottom,
            command=self.save_result
        )
        self.save_button.pack(side="left", padx=(0, 8))

        self.clear_button = ttk.Button(
            bottom,
            command=self.clear_all
        )
        self.clear_button.pack(side="left")

        self.help_hint = ttk.Label(bottom)
        self.help_hint.pack(side="right")

        # Растягиваем большие поля при изменении размера окна
        root.rowconfigure(6, weight=1)
        root.rowconfigure(9, weight=1)

        self.status = ttk.Label(root, anchor="w")
        self.status.grid(row=11, column=0, sticky="ew", pady=(6, 0))

    def t(self, key):
        # Короткий доступ к текущему языку
        return TEXTS[self.lang][key]

    def update_language(self):
        self.title(self.t("title"))
        self.title_label.configure(text=self.t("title"))
        self.method_label.configure(text=self.t("method"))
        self.key_label.configure(text=self.t("key"))
        self.input_label.configure(text=self.t("input"))
        self.result_label.configure(text=self.t("result"))

        self.encrypt_button.configure(text=self.t("encrypt"))
        self.decrypt_button.configure(text=self.t("decrypt"))
        self.load_button.configure(text=self.t("load"))
        self.copy_button.configure(text=self.t("copy"))
        self.save_button.configure(text=self.t("save"))
        self.clear_button.configure(text=self.t("clear"))
        self.help_hint.configure(text=self.t("help_hint"))

        self.lang_combo.set(
            "Русский" if self.lang == "ru" else "English"
        )

        methods = [
            self.t("caesar"),
            self.t("vigenere"),
            self.t("transposition")
        ]

        current = self.method_combo.current()
        self.method_combo.configure(values=methods)

        # Сохраняем выбранный метод после смены языка
        self.method_combo.current(0 if current < 0 else current)

        self.update_key_placeholder()

        if self.help_window and self.help_window.winfo_exists():
            self.help_window.update_texts()

    def change_language(self, _event=None):
        self.lang = "en" if self.lang_combo.get() == "English" else "ru"
        self.update_language()

    def change_method(self, _event=None):
        self.update_key_placeholder()

    def update_key_placeholder(self):
        index = self.method_combo.current()

        key = [
            self.t("caesar_key"),
            self.t("vigenere_key"),
            self.t("transposition_key")
        ][max(index, 0)]

        self.key_entry.set_placeholder(self.t("example") + key)

    def _get_key(self):
        value = self.key_entry.real_value()

        if not value:
            raise ValueError(self.t("empty_key"))

        index = self.method_combo.current()

        # Цезарь: ключ должен быть числом
        if index == 0:
            try:
                return int(value)
            except ValueError:
                raise ValueError(self.t("bad_caesar"))

        # Виженер: только буквы
        if index == 1:
            from cipher.caesar import RUSSIAN, ENGLISH

            if not all(
                ch.upper() in RUSSIAN or ch.upper() in ENGLISH
                for ch in value
            ):
                raise ValueError(self.t("bad_vigenere"))

            return value

        # Транспозиция: положительное число
        try:
            number = int(value)
        except ValueError:
            raise ValueError(self.t("bad_transposition"))

        if number <= 0:
            raise ValueError(self.t("bad_transposition"))

        return number

    def process(self, decrypt):
        text = self.input_text.get("1.0", "end-1c")

        if not text:
            messagebox.showerror(
                self.t("error"),
                self.t("empty_text"),
                parent=self
            )
            return

        try:
            key = self._get_key()
            index = self.method_combo.current()

            # Вызываем нужный алгоритм
            if index == 0:
                result = caesar(text, key, decrypt)
            elif index == 1:
                result = vigenere(text, key, decrypt)
            else:
                result = (
                    trans_decrypt(text, key)
                    if decrypt
                    else trans_encrypt(text, key)
                )

            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", result)

            self.last_operation = "decrypt" if decrypt else "encrypt"
            self.status.configure(text="")

        except ValueError as exc:
            messagebox.showerror(
                self.t("error"),
                str(exc),
                parent=self
            )

    def load_file(self):
        path = filedialog.askopenfilename(
            parent=self,
            title=self.t("load"),
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ],
        )

        if not path:
            return

        current = self.input_text.get("1.0", "end-1c")

        # Не затираем введённый текст случайно
        if current:
            if not messagebox.askyesno(
                self.t("info"),
                self.t("replace_q"),
                parent=self
            ):
                return

        try:
            text = read_text_file(path)
        except (UnicodeDecodeError, OSError):
            messagebox.showerror(
                self.t("error"),
                self.t("file_error"),
                parent=self
            )
            return

        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", text)

        self.current_file = Path(path)
        self.status.configure(text=self.t("loaded"))

    def copy_result(self):
        result = self.result_text.get("1.0", "end-1c")

        if not result:
            return

        self.clipboard_clear()
        self.clipboard_append(result)
        self.update()

        self.status.configure(text=self.t("copied"))

    def save_result(self):
        result = self.result_text.get("1.0", "end-1c")

        if not result:
            return

        # Предлагаем имя на основе исходного файла
        if self.current_file:
            stem = self.current_file.stem
            suffix = (
                "_decrypted"
                if self._looks_decrypted()
                else "_encrypted"
            )
            initial = f"{stem}{suffix}.txt"
        else:
            initial = (
                "decrypted.txt"
                if self._looks_decrypted()
                else "encrypted.txt"
            )

        path = filedialog.asksaveasfilename(
            parent=self,
            title=self.t("save"),
            defaultextension=".txt",
            initialfile=initial,
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ],
        )

        if not path:
            return

        try:
            write_text_file(path, result)
        except OSError:
            messagebox.showerror(
                self.t("error"),
                self.t("save_error"),
                parent=self
            )
            return

        self.status.configure(text=self.t("saved"))

    def _looks_decrypted(self):
        # Если операция ещё не выполнялась, считаем результат шифрованным
        return getattr(self, "last_operation", "encrypt") == "decrypt"

    def clear_all(self):
        if (
            not self.input_text.get("1.0", "end-1c")
            and not self.result_text.get("1.0", "end-1c")
        ):
            return

        if not messagebox.askyesno(
            self.t("info"),
            self.t("clear_q"),
            parent=self
        ):
            return

        self.input_text.delete("1.0", tk.END)
        self.result_text.delete("1.0", tk.END)

        self.current_file = None
        self.status.configure(text="")

    def open_help(self, _event=None):
        # Если справка уже открыта, просто показываем её
        if self.help_window and self.help_window.winfo_exists():
            self.help_window.lift()
            self.help_window.focus_force()
            return "break"

        self.help_window = HelpWindow(
            self,
            lambda: self.lang
        )

        return "break"

    def on_close(self):
        has_result = bool(
            self.result_text.get("1.0", "end-1c")
        )

        if has_result:
            if not messagebox.askyesno(
                self.t("info"),
                self.t("exit_q"),
                parent=self
            ):
                return

        self.destroy()


# Точка запуска GUI
def run():
    app = MainWindow()
    app.mainloop()