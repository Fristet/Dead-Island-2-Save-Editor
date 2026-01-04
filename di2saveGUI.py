import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import os
import threading
import re
import csv
import json
import xml.etree.ElementTree as ET
import sys

def get_base_path():
    """실행 환경(PyInstaller exe 또는 .py 스크립트)에 따른 기본 경로 반환"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

class DI2SaveEditorGUI:
    def __init__(self, root):
        self.root = root
        
        self.base_path = get_base_path()
        self.exe_path = tk.StringVar()
        self.save_path = tk.StringVar()
        self.no_version_safety = tk.BooleanVar(value=True)
        self.lang_var = tk.StringVar(value="en")
        
        self.config_file = os.path.join(self.base_path, "config.json")
        self.lang_file = os.path.join(self.base_path, "lang.xml")
        
        self.ITEMS_DB = {}
        self.UPGRADES_LIST = []
        self.CATEGORIES_MAP = {}
        self.INTERNAL_TO_UI_MAP = {} 
        self.weapon_list_map = {} 
        self.current_weapon_upgrades = [] 
        self.current_weapon_id = None
        self.data_dir = None
        self.lang_db = {}

        self.root.geometry("1200x850")
        
        # --- [폰트 및 스타일 설정] ---
        # 윈도우 가독성을 위해 'Malgun Gothic' 적용
        self.default_font = ("Malgun Gothic", 9)
        self.bold_font = ("Malgun Gothic", 9, "bold")
        self.header_font = ("Malgun Gothic", 14, "bold")
        self.title_font = ("Malgun Gothic", 20, "bold")
        self.log_font = ("Malgun Gothic", 9) 

        style = ttk.Style()
        style.theme_use('clam')
        
        # 공통 스타일
        style.configure(".", font=self.default_font) # 전체 기본 폰트
        style.configure("TFrame", background="#f5f5f5")
        style.configure("Sidebar.TFrame", background="#2b2b2b")
        
        # 헤더 라벨
        style.configure("Header.TLabel", font=self.header_font, background="#f5f5f5", foreground="#333333")
        
        # 일반 라벨
        style.configure("TLabel", background="#f5f5f5", font=self.default_font)
        
        # 라벨 프레임
        style.configure("TLabelframe", background="#f5f5f5")
        style.configure("TLabelframe.Label", font=self.bold_font, background="#f5f5f5", foreground="#555555")
        
        # 트리뷰 (리스트)
        style.configure("Treeview", font=self.default_font, rowheight=25)
        style.configure("Treeview.Heading", font=self.bold_font)
        
        # 버튼
        style.configure("TButton", font=self.default_font)

        self.load_localization()
        self.update_title()
        self.create_layout()
        self.init_settings()

    def load_localization(self):
        self.lang_db = {'kr': {}, 'en': {}}
        if os.path.exists(self.lang_file):
            try:
                tree = ET.parse(self.lang_file)
                root_node = tree.getroot()
                for lang_node in root_node.findall('language'):
                    code = lang_node.get('code')
                    texts = {}
                    for text_node in lang_node.findall('text'):
                        texts[text_node.get('key')] = text_node.text
                    self.lang_db[code] = texts
            except Exception as e:
                print(f"Language Load Error: {e}")

    def T(self, key):
        lang = self.lang_var.get()
        if lang in self.lang_db and key in self.lang_db[lang]:
            return str(self.lang_db[lang][key]).replace("\\n", "\n")
        if 'en' in self.lang_db and key in self.lang_db['en']:
             return str(self.lang_db['en'][key]).replace("\\n", "\n")
        return key 

    def update_title(self):
        self.root.title(self.T('title'))

    def update_ui_text(self):
        self.update_title()
        self.lbl_exe.config(text=self.T('exe_path'))
        self.lbl_save.config(text=self.T('save_path'))
        self.btn_find_exe.config(text=self.T('btn_browse'))
        self.btn_find_save.config(text=self.T('btn_browse'))
        self.chk_safe.config(text=self.T('chk_safety'))
        self.lbl_lang.config(text=self.T('lbl_lang'))
        self.log_frame.config(text=" " + self.T('log_title') + " ")

        menus = [('menu_quick', 0), ('menu_inv', 1), ('menu_upgrade', 2)]
        for key, idx in menus:
            if idx < len(self.menu_buttons):
                self.menu_buttons[idx].config(text=self.T(key))

        if hasattr(self, 'current_page_idx'):
            if self.current_page_idx == 0: self.show_quick_page()
            elif self.current_page_idx == 1: self.show_inventory_page()
            elif self.current_page_idx == 2: self.show_upgrade_page()

    def on_lang_change(self, event=None):
        self.save_settings()
        self.update_ui_text()

    def create_layout(self):
        top_frame = tk.Frame(self.root, bg="#dddddd", height=60)
        top_frame.pack(fill="x", side="top")
        top_inner = tk.Frame(top_frame, bg="#dddddd")
        top_inner.pack(fill="x", padx=10, pady=10)

        # 상단 설정 영역
        self.lbl_exe = tk.Label(top_inner, text=self.T("exe_path"), bg="#dddddd", font=self.default_font)
        self.lbl_exe.pack(side="left")
        ttk.Entry(top_inner, textvariable=self.exe_path, width=35).pack(side="left", padx=5)
        self.btn_find_exe = tk.Button(top_inner, text=self.T("btn_browse"), command=self.browse_exe, font=self.default_font)
        self.btn_find_exe.pack(side="left")

        self.lbl_save = tk.Label(top_inner, text="   "+self.T("save_path"), bg="#dddddd", font=self.default_font)
        self.lbl_save.pack(side="left")
        ttk.Entry(top_inner, textvariable=self.save_path, width=35).pack(side="left", padx=5)
        self.btn_find_save = tk.Button(top_inner, text=self.T("btn_browse"), command=self.browse_save, font=self.default_font)
        self.btn_find_save.pack(side="left")
        
        self.combo_lang = ttk.Combobox(top_inner, textvariable=self.lang_var, state="readonly", width=5)
        available_langs = list(self.lang_db.keys())
        if not available_langs: available_langs = ['kr', 'en']
        self.combo_lang['values'] = available_langs
        self.combo_lang.pack(side="right", padx=5)
        self.combo_lang.bind("<<ComboboxSelected>>", self.on_lang_change)
        
        self.lbl_lang = tk.Label(top_inner, text=self.T("lbl_lang"), bg="#dddddd", font=self.default_font)
        self.lbl_lang.pack(side="right")

        self.chk_safe = tk.Checkbutton(top_inner, text=self.T("chk_safety"), variable=self.no_version_safety, bg="#dddddd", font=self.default_font)
        self.chk_safe.pack(side="right", padx=10)

        main_container = tk.Frame(self.root, bg="#f5f5f5")
        main_container.pack(fill="both", expand=True)

        # 사이드바
        self.sidebar = tk.Frame(main_container, bg="#2b2b2b", width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="DEAD ISLAND 2\nSAVE EDITOR", bg="#2b2b2b", fg="#ffffff", font=self.title_font).pack(pady=(20, 30))

        self.menu_buttons = []
        menus = [('menu_quick', self.show_quick_page), 
                 ('menu_inv', self.show_inventory_page), 
                 ('menu_upgrade', self.show_upgrade_page)]
        
        for key, command in menus:
            btn = tk.Button(self.sidebar, text=self.T(key), command=command, 
                            font=("Malgun Gothic", 11, "bold"),
                            bg="#2b2b2b", fg="#aaaaaa", 
                            activebackground="#4a90e2", activeforeground="white",
                            relief="flat", bd=0, height=2, anchor="w", padx=20)
            btn.pack(fill="x", pady=2)
            self.menu_buttons.append(btn)

        self.content_area = ttk.Frame(main_container, style="TFrame")
        self.content_area.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # 로그창
        self.log_frame = ttk.LabelFrame(self.root, text=" " + self.T("log_title") + " ", padding=5)
        self.log_frame.pack(side="bottom", fill="x", padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(self.log_frame, height=5, state='disabled', font=self.log_font, bg="#fdfdfd")
        self.log_text.pack(fill="both", expand=True)

        self.current_page_idx = 0
        self.show_quick_page()

    def highlight_menu(self, index):
        self.current_page_idx = index
        for i, btn in enumerate(self.menu_buttons):
            if i == index:
                btn.config(bg="#4a90e2", fg="white")
            else:
                btn.config(bg="#2b2b2b", fg="#aaaaaa")

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def init_settings(self):
        loaded_exe = False
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    saved_exe = config.get("exe_path", "")
                    saved_save = config.get("save_path", "")
                    saved_lang = config.get("language", "en")
                    
                    self.lang_var.set(saved_lang)
                    self.update_ui_text()

                    if saved_exe and os.path.exists(saved_exe):
                        self.exe_path.set(saved_exe)
                        self.load_databases(saved_exe)
                        loaded_exe = True
                    if saved_save:
                        self.save_path.set(saved_save)
                    self.log("Settings loaded.")
            except Exception as e: self.log(f"Config Load Error: {e}")

        if not loaded_exe: self.try_auto_detect()

    def save_settings(self):
        data = {
            "exe_path": self.exe_path.get(),
            "save_path": self.save_path.get(),
            "language": self.lang_var.get()
        }
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except: pass

    # ================= PAGE 1: Quick =================
    def show_quick_page(self):
        self.highlight_menu(0)
        self.clear_content()
        ttk.Label(self.content_area, text=self.T('quick_header'), style="Header.TLabel").pack(anchor="w", pady=(0, 20))
        
        frame = ttk.LabelFrame(self.content_area, text=self.T('quick_char_group'), padding=15)
        frame.pack(fill="x", pady=10)
        
        tk.Button(frame, text=self.T('quick_btn_xp'), bg="#4caf50", fg="white", font=("Malgun Gothic", 10, "bold"),
                  relief="flat", pady=5, command=lambda: self.run_command_thread(["quick", "apply", "max-xp"])).pack(fill="x", pady=5)
        ttk.Label(frame, text=self.T('quick_xp_desc')).pack(anchor="w")

        frame2 = ttk.LabelFrame(self.content_area, text=self.T('quick_adv_group'), padding=15)
        frame2.pack(fill="x", pady=10)
        ttk.Label(frame2, text=self.T('quick_cmd_lbl')).pack(anchor="w")
        self.custom_quick = tk.StringVar()
        ttk.Entry(frame2, textvariable=self.custom_quick, font=self.default_font).pack(fill="x", pady=5)
        tk.Button(frame2, text=self.T('btn_run'), bg="#607d8b", fg="white", font=self.default_font, relief="flat", pady=3,
                   command=lambda: self.run_command_thread(["quick", "apply", self.custom_quick.get()])).pack(fill="x")

    # ================= PAGE 2: Inventory =================
    def show_inventory_page(self):
        self.highlight_menu(1)
        self.clear_content()
        ttk.Label(self.content_area, text=self.T('inv_header'), style="Header.TLabel").pack(anchor="w", pady=(0, 10))

        top_panel = ttk.Frame(self.content_area)
        top_panel.pack(fill="x", pady=(0, 10))
        add_pane = tk.PanedWindow(top_panel, orient="horizontal", bg="#f5f5f5", sashwidth=5)
        add_pane.pack(fill="x", expand=True)

        money_frame = ttk.LabelFrame(add_pane, text=self.T('inv_money_group'), padding=10)
        add_pane.add(money_frame, width=300)
        f_money = ttk.Frame(money_frame)
        f_money.pack(fill="x", pady=5)
        ttk.Label(f_money, text=self.T('inv_money_lbl')).pack(side="left")
        self.money_amount = tk.StringVar(value="10000")
        ttk.Entry(f_money, textvariable=self.money_amount, width=12).pack(side="left", padx=5)
        tk.Button(f_money, text=self.T('inv_btn_money'), bg="#ff9800", fg="white", relief="flat", font=self.default_font,
                   command=lambda: self.run_command_thread(["player", "inventory", "add", "--name", "DA_InventoryTypes_Special_CashItem", "--count", self.money_amount.get()])).pack(side="left", padx=5)

        item_frame = ttk.LabelFrame(add_pane, text=self.T('inv_add_group'), padding=10)
        add_pane.add(item_frame)
        f_item = ttk.Frame(item_frame)
        f_item.pack(fill="x", pady=2)
        ttk.Label(f_item, text=self.T('inv_cat_lbl')).pack(side="left")
        self.inv_category = tk.StringVar()
        self.combo_category = ttk.Combobox(f_item, textvariable=self.inv_category, state="readonly", width=15)
        self.combo_category.pack(side="left", padx=5)
        self.combo_category.bind("<<ComboboxSelected>>", self.update_item_list_callback)
        if self.ITEMS_DB: self.combo_category['values'] = list(self.ITEMS_DB.keys()); self.combo_category.current(0)
        
        ttk.Label(f_item, text=self.T('inv_item_lbl')).pack(side="left")
        self.inv_item_label = tk.StringVar()
        self.combo_item = ttk.Combobox(f_item, textvariable=self.inv_item_label, state="normal", width=30)
        self.combo_item.pack(side="left", padx=5)
        self.update_item_list_callback(None)
        
        ttk.Label(f_item, text=self.T('inv_count_lbl')).pack(side="left")
        self.inv_item_count = tk.StringVar(value="1")
        ttk.Entry(f_item, textvariable=self.inv_item_count, width=5).pack(side="left", padx=5)
        tk.Button(f_item, text=self.T('inv_btn_add'), bg="#2196f3", fg="white", relief="flat", font=self.default_font, command=self.add_item_from_list).pack(side="left", padx=5)

        list_frame = ttk.LabelFrame(self.content_area, text=self.T('inv_list_group'), padding=10)
        list_frame.pack(fill="both", expand=True)
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill="x", pady=(0, 5))
        tk.Button(btn_frame, text=self.T('inv_btn_refresh'), bg="#009688", fg="white", relief="flat", font=self.default_font, command=self.load_inventory_list).pack(side="left", padx=5)
        tk.Button(btn_frame, text=self.T('inv_btn_del'), bg="#e91e63", fg="white", relief="flat", font=self.default_font, command=self.delete_selected_inventory_item).pack(side="right", padx=5)

        columns = ("name", "type", "info", "id")
        self.inv_tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        self.inv_tree.heading("name", text=self.T('inv_col_name'))
        self.inv_tree.heading("type", text=self.T('inv_col_type'))
        self.inv_tree.heading("info", text=self.T('inv_col_info'))
        self.inv_tree.heading("id", text=self.T('inv_col_id'))
        self.inv_tree.column("name", width=300)
        self.inv_tree.column("type", width=100)
        self.inv_tree.column("info", width=150)
        self.inv_tree.column("id", width=250)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.inv_tree.yview)
        self.inv_tree.configure(yscroll=scrollbar.set)
        self.inv_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ================= PAGE 3: Upgrades =================
    def show_upgrade_page(self):
        self.highlight_menu(2)
        self.clear_content()
        ttk.Label(self.content_area, text=self.T('upg_header'), style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        paned = tk.PanedWindow(self.content_area, orient="horizontal", bg="#f5f5f5", sashwidth=5)
        paned.pack(fill="both", expand=True)

        left_frame = ttk.LabelFrame(paned, text=self.T('upg_left_group'), padding=10)
        paned.add(left_frame, width=350)
        tk.Button(left_frame, text=self.T('upg_btn_refresh'), bg="#009688", fg="white", relief="flat", pady=5, font=self.default_font, command=self.load_weapons_visual).pack(fill="x", pady=(0, 5))
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        self.weapon_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=self.default_font, selectmode="single", bg="white", bd=1, relief="solid")
        self.weapon_listbox.pack(side="left", fill="both", expand=True)
        self.weapon_listbox.bind("<<ListboxSelect>>", self.on_weapon_select)
        scrollbar.config(command=self.weapon_listbox.yview)

        right_frame = ttk.LabelFrame(paned, text=self.T('upg_right_group'), padding=10)
        paned.add(right_frame)
        self.slots_container = ttk.Frame(right_frame)
        self.slots_container.pack(fill="both", expand=True, anchor="n")
        self.lbl_slot_info = ttk.Label(self.slots_container, text=self.T('upg_slot_info'), anchor="center", justify="center")
        self.lbl_slot_info.pack(pady=50)

    # --- 로직 함수들 ---
    def log(self, message):
        """로그 텍스트 박스에 메시지 출력"""
        # UI 업데이트이므로 메인 스레드에서 실행 보장 필요
        if threading.current_thread() is not threading.main_thread():
            self.root.after(0, lambda: self.log(message))
            return
            
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, ">> " + message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def try_auto_detect(self):
        path1 = os.path.join(self.base_path, "di2save.exe")
        path2 = os.path.join(self.base_path, "bin", "di2save.exe")
        if os.path.exists(path1): self.exe_path.set(path1); self.load_databases(path1)
        elif os.path.exists(path2): self.exe_path.set(path2); self.load_databases(path2)
        else: self.log(self.T('msg_no_exe'))

    def load_databases(self, exe_path):
        base_dir = os.path.dirname(exe_path)
        self.data_dir = os.path.join(base_dir, "data", "inventory")
        cat_file = os.path.join(self.data_dir, "categories.csv")
        items_file = os.path.join(self.data_dir, "items.csv")
        upgrades_file = os.path.join(self.data_dir, "weapon_upgrades.csv")

        self.log(f"Loading data... ({self.data_dir})")
        self.INTERNAL_TO_UI_MAP = {} 
        self.CATEGORIES_MAP = {}
        if os.path.exists(cat_file):
            try:
                with open(cat_file, 'r', encoding='utf-8-sig') as f:
                    for row in csv.DictReader(f): self.CATEGORIES_MAP[row.get('name', '').strip()] = row.get('ui_name', '').strip() or row.get('name', '').strip()
            except: pass

        self.ITEMS_DB = {}
        if os.path.exists(items_file):
            try:
                with open(items_file, 'r', encoding='utf-8-sig') as f:
                    for row in csv.DictReader(f):
                        cat = self.CATEGORIES_MAP.get(row.get('category', '').strip(), row.get('category', '').strip())
                        if cat not in self.ITEMS_DB: self.ITEMS_DB[cat] = []
                        name = row.get('name', '').strip()
                        ui = row.get('ui_name', '').strip() or name
                        if name:
                            self.ITEMS_DB[cat].append((ui, name))
                            self.INTERNAL_TO_UI_MAP[name] = ui
            except: pass

        self.UPGRADES_LIST = []
        if os.path.exists(upgrades_file):
            try:
                with open(upgrades_file, 'r', encoding='utf-8-sig') as f:
                    temp = []
                    for row in csv.DictReader(f):
                        name = row.get('name', '').strip()
                        ui = row.get('ui_name', '').strip() or name
                        rarity = row.get('rarity', 'Common').strip().title()
                        if name:
                            self.INTERNAL_TO_UI_MAP[name] = ui
                            temp.append({'display': f"{ui} ({rarity})", 'code': name, 'rarity': rarity, 'ui': ui})
                    rp = {'Legendary': 0, 'Superior': 1, 'Rare': 2, 'Uncommon': 3, 'Common': 4}
                    temp.sort(key=lambda x: (rp.get(x['rarity'], 99), x['ui']))
                    for t in temp: self.UPGRADES_LIST.append((t['display'], t['code']))
            except: pass
        
        self.log(f"Loaded: Items {sum(len(v) for v in self.ITEMS_DB.values())}, Upgrades {len(self.UPGRADES_LIST)}")
        if hasattr(self, 'combo_category'): self.combo_category['values'] = list(self.ITEMS_DB.keys()); self.combo_category.current(0); self.update_item_list_callback(None)

    def browse_exe(self):
        filename = filedialog.askopenfilename(title=self.T('btn_browse'), filetypes=[("Executable", "*.exe")])
        if filename: self.exe_path.set(filename); self.load_databases(filename); self.save_settings()

    def browse_save(self):
        filename = filedialog.askopenfilename(title=self.T('btn_browse'), filetypes=[("Save files", "*.sav")])
        if filename: self.save_path.set(filename); self.save_settings()

    def run_command_thread(self, args, callback=None): 
        threading.Thread(target=self.run_command, args=(args, callback)).start()

    def run_command(self, args, callback=None):
        exe, save = self.exe_path.get(), self.save_path.get()
        if not exe or not os.path.exists(exe): self.log(self.T('msg_no_exe')); return
        if not save and "--help" not in args: self.log(self.T('msg_no_exe')); return
        
        cmd = [exe] + args
        if save and "help" not in args: cmd.extend(["--file", save])
        if self.no_version_safety.get() and "help" not in args: cmd.append("--no-version-safety")
        
        self.log(f"{self.T('msg_cmd_run')} {' '.join(cmd)}")
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, startupinfo=startupinfo, encoding='utf-8', errors='replace')
            out, err = proc.communicate()
            
            if out: self.log(f"{self.T('msg_success')}\n{out}")
            if err: self.log(f"{self.T('msg_error')}\n{err}")
            
            # [중요 수정] 콜백은 메인 UI 스레드에서 실행되어야 안전함
            if callback: 
                self.root.after(0, lambda: callback(out))
            return out
        except Exception as e: 
            self.log(f"{self.T('msg_error')} {str(e)}")

    def update_item_list_callback(self, event):
        if not hasattr(self, 'combo_item'): return
        cat = self.inv_category.get()
        if cat in self.ITEMS_DB: self.combo_item['values'] = [x[0] for x in self.ITEMS_DB[cat]]; self.combo_item.current(0)

    def add_item_from_list(self):
        cat = self.inv_category.get(); lbl = self.inv_item_label.get(); code = None
        if cat in self.ITEMS_DB:
            for l, c in self.ITEMS_DB[cat]:
                if l == lbl: code = c; break
        if not code: messagebox.showerror("Error", "Code not found"); return
        if code.startswith("DA_Recipe") or code.startswith("DA_Skill"): self.check_and_add_recipe(code, self.inv_item_count.get())
        else: self.run_command_thread(["player", "inventory", "add", "--name", code, "--count", self.inv_item_count.get()])

    def check_and_add_recipe(self, code, count):
        def _process():
            self.log(f"{self.T('msg_dup_check')} ({code})")
            cmd = [self.exe_path.get(), "player", "inventory", "ls", "--file", self.save_path.get()]
            if self.no_version_safety.get(): cmd.append("--no-version-safety")
            startupinfo = subprocess.STARTUPINFO(); startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            try:
                out = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, startupinfo=startupinfo, encoding='utf-8', errors='replace').communicate()[0]
                
                # UI 상호작용은 메인 스레드로 전달
                def _ui_result(output_text):
                    if code in output_text:
                        self.log(self.T('msg_dup_found'))
                        messagebox.showinfo("Info", self.T('alert_dup'))
                    else:
                        self.log(self.T('msg_dup_pass'))
                        self.run_command_thread(["player", "inventory", "add", "--name", code, "--count", count])
                
                self.root.after(0, lambda: _ui_result(out))
            except: pass
        threading.Thread(target=_process).start()

    def load_inventory_list(self):
        for item in self.inv_tree.get_children(): self.inv_tree.delete(item)
        def _parse(output):
            lines = output.split('\n')
            current_section = None
            item_block = {}
            parsed_items = []
            for line in lines:
                line = line.strip()
                if not line: continue
                if "Instanced items:" in line: current_section = "Instanced"; continue
                elif "Archetype items:" in line: current_section = "Archetype"; continue
                id_match = re.search(r"Entry ID:\s*([a-f0-9]+)", line, re.IGNORECASE)
                if id_match:
                    if item_block: parsed_items.append(item_block)
                    item_block = {'id': id_match.group(1), 'type': current_section, 'name': 'Unknown', 'info': ''}
                    continue
                if item_block:
                    if "Archetype:" in line:
                        name_match = re.search(r"Archetype:.*[/\.](DA_[^\.]+)", line, re.IGNORECASE)
                        if not name_match: name_match = re.search(r"Archetype:.*[/\\]([^/\\]+)$", line, re.IGNORECASE)
                        if name_match:
                            internal_name = name_match.group(1)
                            ui_name = self.INTERNAL_TO_UI_MAP.get(internal_name, internal_name)
                            item_block['name'] = ui_name
                    if "Count:" in line: cnt = line.split("Count:")[-1].strip(); item_block['info'] = f"x{cnt}"
                    if "Required rarity:" in line: rarity = line.split("::")[-1].strip(); item_block['info'] = rarity
            if item_block: parsed_items.append(item_block)
            for p in parsed_items: self.inv_tree.insert("", "end", values=(p['name'], p['type'], p['info'], p['id']))
            self.log(f"Inventory loaded: {len(parsed_items)} items")
        self.run_command_thread(["player", "inventory", "ls"], callback=_parse)

    def delete_selected_inventory_item(self):
        selected = self.inv_tree.selection()
        if not selected: messagebox.showwarning("Info", "Select an item."); return
        item_values = self.inv_tree.item(selected[0], 'values')
        if messagebox.askyesno("Confirm", self.T('alert_del_confirm') + f"\n{item_values[0]}"):
            self.run_command_thread(["player", "inventory", "rm", item_values[3]], callback=lambda _: self.load_inventory_list())

    def load_weapons_visual(self):
        def parse_and_fill(output):
            self.weapon_list_map = {} 
            self.weapon_listbox.delete(0, tk.END)
            lines = output.split('\n')
            temp_weapons = [] 
            item_block = {}
            new_upgrades_found = False
            for line in lines:
                line = line.strip()
                id_match = re.search(r"Entry ID:\s*([a-f0-9]+)", line, re.IGNORECASE)
                if id_match:
                    if item_block: self.process_weapon_block(item_block, temp_weapons)
                    item_block = {'id': id_match.group(1), 'upgrades': []}
                    continue
                if item_block:
                    if "Archetype:" in line:
                        name_match = re.search(r"Archetype:.*[/\.](DA_[^\.]+)", line, re.IGNORECASE)
                        if not name_match: name_match = re.search(r"Archetype:.*[/\\]([^/\\]+)$", line, re.IGNORECASE)
                        if name_match: item_block['name'] = name_match.group(1)
                    upg_match = re.search(r"UpgradeEntry\d+:\s*(.*)", line, re.IGNORECASE)
                    if upg_match:
                        full_upg = upg_match.group(1)
                        short_upg = full_upg
                        nm = re.search(r"[/\.](DA_[^\.]+)", full_upg)
                        if nm: short_upg = nm.group(1)
                        item_block['upgrades'].append(short_upg)
                        if short_upg not in self.INTERNAL_TO_UI_MAP:
                            self.register_new_upgrade(short_upg, full_upg)
                            new_upgrades_found = True
            if item_block: self.process_weapon_block(item_block, temp_weapons)
            for display, wid, upgrades in temp_weapons:
                self.weapon_listbox.insert(tk.END, display)
                self.weapon_list_map[display] = {'id': wid, 'upgrades': upgrades}
            if new_upgrades_found: self.log(self.T('msg_new_upgrade'))
        self.run_command_thread(["player", "inventory", "ls"], callback=parse_and_fill)

    def register_new_upgrade(self, code, archetype):
        if not self.data_dir: return 
        ui_name = code.replace("DA_ItemUpgradeData_", "").replace("_", " ")
        display = f"{ui_name} (Auto)"
        self.INTERNAL_TO_UI_MAP[code] = display
        self.UPGRADES_LIST.append((display, code))
        cat_key = self.CATEGORIES_MAP.get('DA_InventoryCategory_Recipes', 'Recipes')
        if cat_key not in self.ITEMS_DB: self.ITEMS_DB[cat_key] = []
        self.ITEMS_DB[cat_key].append((f"{ui_name} Recipe (Auto)", code))
        try:
            with open(os.path.join(self.data_dir, "weapon_upgrades.csv"), 'a', newline='', encoding='utf-8-sig') as f:
                csv.writer(f).writerow(["unknown", "any", "Common", code, ui_name, archetype])
        except: pass
        try:
            with open(os.path.join(self.data_dir, "items.csv"), 'a', newline='', encoding='utf-8-sig') as f:
                csv.writer(f).writerow(["DA_InventoryCategory_Recipes", "RecipeArchetype", code, f"{ui_name} Recipe", "0", "0", "1", "0", "0", "0", archetype])
            self.log(self.T('msg_new_upgrade') + f" {ui_name}")
        except: pass

    def process_weapon_block(self, block, target_list):
        if 'name' in block and 'id' in block:
            name = block['name']
            if name.startswith("DA_MeleeWeapon") or name.startswith("DA_RangedWeapon"):
                ui_name = self.INTERNAL_TO_UI_MAP.get(name, name)
                target_list.append((ui_name, block['id'], block['upgrades']))

    def on_weapon_select(self, event):
        selection = self.weapon_listbox.curselection()
        if not selection: return
        display_name = self.weapon_listbox.get(selection[0])
        weapon_data = self.weapon_list_map.get(display_name)
        if weapon_data:
            self.current_weapon_id = weapon_data['id']
            self.current_weapon_upgrades = weapon_data['upgrades']
            self.draw_upgrade_slots()

    def draw_upgrade_slots(self):
        for widget in self.slots_container.winfo_children(): widget.destroy()
        tk.Label(self.slots_container, text=f"Weapon ID: {self.current_weapon_id}", bg="#f5f5f5", fg="#888", font=("Consolas", 8)).pack(anchor="w", pady=(0, 10))
        for i in range(5):
            is_occupied = i < len(self.current_weapon_upgrades)
            card_bg = "white" if is_occupied else "#e8f5e9"
            label_bg = "#ddd" if is_occupied else "#c8e6c9"
            card = tk.Frame(self.slots_container, bg=card_bg, bd=1, relief="solid")
            card.pack(fill="x", pady=4, padx=2)
            left_col = tk.Frame(card, bg=label_bg, width=60)
            left_col.pack(side="left", fill="y")
            left_col.pack_propagate(False)
            tk.Label(left_col, text=f"Slot {i+1}", bg=label_bg, fg="#333", font=("Malgun Gothic", 9, "bold")).pack(expand=True)
            if is_occupied:
                upg_code = self.current_weapon_upgrades[i]
                ui_name = self.INTERNAL_TO_UI_MAP.get(upg_code, upg_code)
                tk.Label(card, text=ui_name, bg="white", font=("Malgun Gothic", 10, "bold"), anchor="w").pack(side="left", padx=10, fill="x", expand=True)
                del_btn = tk.Button(card, text=self.T('upg_btn_remove'), bg="#ffcdd2", fg="#c62828", relief="flat", bd=0, font=self.default_font, command=lambda c=upg_code: self.remove_upgrade(c))
                del_btn.pack(side="right", padx=5, pady=5)
            else:
                btn_add = tk.Button(card, text=self.T('upg_slot_empty'), bg="#e8f5e9", fg="#2e7d32", font=("Malgun Gothic", 10), relief="flat", anchor="w", command=self.open_add_upgrade_popup)
                btn_add.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    def remove_upgrade(self, upgrade_code):
        if messagebox.askyesno("Confirm", self.T('alert_remove_confirm')):
            self.run_command_thread(["player", "inventory", "upgrade", "rm", "--item", self.current_weapon_id, "--name", upgrade_code], callback=lambda _: self.load_weapons_visual())

    def open_add_upgrade_popup(self):
        if not hasattr(self, 'current_weapon_id'): return
        popup = tk.Toplevel(self.root)
        popup.title(self.T('upg_popup_title'))
        popup.geometry("450x180")
        ttk.Label(popup, text=self.T('upg_popup_lbl'), font=("Malgun Gothic", 10, "bold")).pack(pady=(15, 5))
        combo = ttk.Combobox(popup, width=60, state="readonly", font=("Malgun Gothic", 9))
        if self.UPGRADES_LIST: combo['values'] = [u[0] for u in self.UPGRADES_LIST]
        combo.pack(pady=5)
        def _confirm():
            selection = combo.get()
            if not selection: return
            code = selection
            for l, c in self.UPGRADES_LIST:
                if l == selection: code = c; break
            popup.destroy()
            self.run_command_thread(["player", "inventory", "upgrade", "add", "--item", self.current_weapon_id, "--name", code], callback=lambda _: self.load_weapons_visual())
        tk.Button(popup, text=self.T('upg_popup_confirm'), bg="#4caf50", fg="white", relief="flat", padx=20, pady=5, font=self.default_font, command=_confirm).pack(pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    
    # [수정됨] 아이콘 경로를 절대 경로로 계산하여 적용
    base_path = get_base_path() 
    icon_path = os.path.join(base_path, "di2save_icon.ico")
    
    # 아이콘 파일이 실제로 존재할 때만 적용 (에러 방지)
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(default=icon_path)
        except Exception as e:
            print(f"Icon Load Error: {e}")

    app = DI2SaveEditorGUI(root)
    root.mainloop()