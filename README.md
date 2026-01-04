# Dead Island 2 Save Editor GUI

**A user-friendly GUI wrapper for the Dead Island 2 Save Editor.** This tool allows you to easily modify your save files, manage inventory, and customize weapon upgrades without using the command line.

<p align="center">
  <img src="https://private-user-images.githubusercontent.com/10806467/531737844-22402618-3eb8-48f8-8c2e-24ba9187a3eb.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Njc1NDA3OTksIm5iZiI6MTc2NzU0MDQ5OSwicGF0aCI6Ii8xMDgwNjQ2Ny81MzE3Mzc4NDQtMjI0MDI2MTgtM2ViOC00OGY4LThjMmUtMjRiYTkxODdhM2ViLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjAxMDQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwMTA0VDE1MjgxOVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWRmM2IxNWZjZmFkNDc1MWJmNzA4MTU5YWY4YjI2MTMxOGZhY2MxNzliNGYzOWE0NjBmODkxMzU5MjQwNTdmNzUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.4MVCt7U5TPBcZArV_ZGLsx0wrv1bVrcR2SW1C5JzGCY" alt="Dead Island 2 Save Editor GUI Screenshot" width="800">
</p>

<p align="center">
  <img src="https://private-user-images.githubusercontent.com/10806467/531737845-c038d092-28ff-46e3-a64b-f29be1a31028.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Njc1NDA3OTksIm5iZiI6MTc2NzU0MDQ5OSwicGF0aCI6Ii8xMDgwNjQ2Ny81MzE3Mzc4NDUtYzAzOGQwOTItMjhmZi00NmUzLWE2NGItZjI5YmUxYTMxMDI4LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjAxMDQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwMTA0VDE1MjgxOVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWQxNzdhZjc5Y2U3MzE0NTVhNjkzNWU1YmMwYzNjYWJiYzIzOTFjMDAzYmYwNDI4YWMxNjE3NzcxNGJiN2EyMWUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.mznCv0vvMUssHAIH2YCZ4O8riL0lnqHXgm_6_oQc3DU" alt="Dead Island 2 Save Editor GUI Screenshot" width="800">
</p>

<p align="center">
  <img src="https://private-user-images.githubusercontent.com/10806467/531737847-f5276545-7ea5-4c3b-a3b1-562580aa3603.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Njc1NDA3OTksIm5iZiI6MTc2NzU0MDQ5OSwicGF0aCI6Ii8xMDgwNjQ2Ny81MzE3Mzc4NDctZjUyNzY1NDUtN2VhNS00YzNiLWEzYjEtNTYyNTgwYWEzNjAzLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjAxMDQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwMTA0VDE1MjgxOVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTY1NTdmMmNhMmU1MzgzZTY2OTNhNzVmZjdjYWM4M2NlYTc5ZWRhODFhNDkzNDA5Y2YxNzkyMTY1N2Q4NDY5MmImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.GusH52trNBHw7QX-iPHGTOekcrU_27Szyf9nQ4MBSCY" alt="Dead Island 2 Save Editor GUI Screenshot" width="800">
</p>

---

### 🌍 Languages
[English](#english) | [한국어 (Korean)](#한국어-korean) | [Français (French)](#français-french) | [Español (Spanish)](#español-spanish) | [Русский (Russian)](#русский-russian) | [简体中文 (Chinese)](#简体中文-chinese)

---

## English

### ✨ Features
* **Quick Cheats:** Instantly apply Max Level & Max XP to your character.
* **Inventory Management:**
    * Add unlimited Money (Cash).
    * Add Items (Weapons, Consumables, Crafting Materials, Blueprints/Cards).
    * Delete unwanted items easily.
* **Weapon Modification:**
    * Visual Upgrade Editor: View and edit weapon upgrade slots.
    * Add or Remove mods and perks directly.
* **Safety:** Supports automatic version safety checks (can be toggled).

### 🚀 How to Install & Use
1.  Download the latest release.
2.  **Important:** Ensure `di2save.exe` and the `data/` folder are in the same directory as this GUI.
3.  Run `di2save_gui.exe`.
4.  **Configuration:**
    * **Executable Path:** Select the `di2save.exe` file.
    * **Save File Path:** Select your `.sav` file (usually located in `%LOCALAPPDATA%\DeadIsland2\Saved\SaveGames`).
5.  Choose a menu from the sidebar (Quick / Inventory / Upgrade) and apply your changes.

### ⚠️ Disclaimer
* Always **backup your save files** before using this tool.
* Use at your own risk. The author is not responsible for corrupted save files.

### 🏆 Credits & Original Project
* **Core Tool:** This GUI is based on the **[Dead Island 2 Save Editor (CLI)](https://steffenl.com/projects/dead-island-2-save-editor)** by **SteffenL**.
* Please visit the original project page for updates regarding the core logic.

---

## 한국어 (Korean)

### ✨ 주요 기능
* **빠른 치트:** 클릭 한 번으로 만렙(Max Level) 및 최대 경험치 적용.
* **인벤토리 관리:**
    * 돈(Cash) 무제한 추가.
    * 아이템 추가 (무기, 소모품, 재료, 설계도/카드).
    * 불필요한 아이템 삭제 기능.
* **무기 개조 (업그레이드):**
    * 무기 슬롯 시각화: 장착된 업그레이드를 눈으로 확인하고 편집.
    * 특전(Perk) 및 개조 부품(Mod) 자유로운 장착/해제.
* **안전성:** 버전 안전 검사 기능 지원 (옵션에서 토글 가능).

### 🚀 설치 및 사용법
1.  최신 버전을 다운로드하세요.
2.  **중요:** 이 프로그램은 `di2save.exe`와 `data/` 폴더가 같은 위치에 있어야 작동합니다.
3.  `di2save_gui.exe`를 실행하세요.
4.  **설정:**
    * **실행 파일 경로:** `di2save.exe` 파일을 선택합니다.
    * **세이브 파일 경로:** 수정할 `.sav` 파일을 선택합니다 (보통 `%LOCALAPPDATA%\DeadIsland2\Saved\SaveGames` 경로에 있습니다).
5.  왼쪽 메뉴에서 원하는 기능(빠른 설정 / 인벤토리 / 업그레이드)을 선택하여 적용하세요.

### ⚠️ 주의 사항
* 이 도구를 사용하기 전에 반드시 **세이브 파일을 백업**하세요.
* 세이브 파일 손상에 대한 책임은 사용자에게 있습니다.

### 🏆 크레딧 (원본 프로젝트)
* **핵심 도구:** 이 프로그램은 **SteffenL** 님의 **[Dead Island 2 Save Editor (CLI)](https://steffenl.com/projects/dead-island-2-save-editor)** 를 기반으로 제작되었습니다.
* 핵심 로직에 대한 업데이트는 원본 프로젝트 페이지를 참고해 주세요.

---

## Français (French)

### ✨ Fonctionnalités
* **Astuces Rapides (Quick Cheats) :** Appliquez instantanément le Niveau Max et l'XP Max à votre personnage.
* **Gestion de l'Inventaire :**
    * Ajouter de l'Argent (Cash) illimité.
    * Ajouter des Objets (Armes, Consommables, Matériaux, Plans/Cartes).
    * Supprimer facilement les objets indésirables.
* **Modification d'Armes :**
    * Éditeur Visuel : Visualisez et modifiez les emplacements d'amélioration des armes.
    * Ajoutez ou retirez directement des mods et des avantages (perks).
* **Sécurité :** Supporte la vérification automatique de version (peut être activé/désactivé).

### 🚀 Installation et Utilisation
1.  Téléchargez la dernière version (release).
2.  **Important :** Assurez-vous que `di2save.exe` et le dossier `data/` se trouvent dans le même répertoire que cette interface (GUI).
3.  Lancez `di2save_gui.exe`.
4.  **Configuration :**
    * **Chemin de l'exécutable :** Sélectionnez le fichier `di2save.exe`.
    * **Chemin de la sauvegarde :** Sélectionnez votre fichier `.sav` (généralement situé dans `%LOCALAPPDATA%\DeadIsland2\Saved\SaveGames`).
5.  Choisissez un menu dans la barre latérale (Rapide / Inventaire / Amélioration) et appliquez vos changements.

### ⚠️ Avertissement
* **Sauvegardez toujours vos fichiers de sauvegarde** (backup) avant d'utiliser cet outil.
* Utilisation à vos propres risques. L'auteur n'est pas responsable des fichiers de sauvegarde corrompus.

### 🏆 Crédits
* **Outil Principal :** Cette interface est basée sur le **[Dead Island 2 Save Editor (CLI)](https://steffenl.com/projects/dead-island-2-save-editor)** créé par **SteffenL**.
* Veuillez visiter la page du projet original pour les mises à jour concernant la logique centrale.

---

## Español (Spanish)

### ✨ Características
* **Trucos Rápidos:** Aplica Nivel Máximo y XP Máxima al instante.
* **Gestión de Inventario:**
    * Añadir dinero ilimitado.
    * Añadir objetos (Armas, Consumibles, Materiales, Planos).
    * Eliminar objetos no deseados.
* **Modificación de Armas:**
    * Editor Visual: Ver y editar ranuras de mejora de armas.
    * Añadir o quitar mods y ventajas (perks) directamente.
* **Seguridad:** Comprobación automática de seguridad de versión.

### 🚀 Instalación y Uso
1.  Descarga la última versión.
2.  **Importante:** Asegúrate de que `di2save.exe` y la carpeta `data/` estén en el mismo directorio.
3.  Ejecuta `di2save_gui.exe`.
4.  Selecciona la ruta de `di2save.exe` y tu archivo de guardado (`.sav`).
5.  Usa el menú lateral para aplicar los cambios.

### 🏆 Créditos
* **Herramienta Principal:** Esta GUI está basada en **[Dead Island 2 Save Editor (CLI)](https://steffenl.com/projects/dead-island-2-save-editor)** creado por **SteffenL**.

---

## Русский (Russian)

### ✨ Особенности
* **Быстрые читы:** Мгновенное получение максимального уровня и опыта.
* **Управление инвентарем:**
    * Добавление неограниченного количества денег.
    * Добавление предметов (Оружие, Расходники, Материалы, Чертежи).
    * Удаление предметов.
* **Модификация оружия:**
    * Визуальный редактор: Просмотр и изменение слотов улучшения оружия.
    * Добавление и удаление модов и перков.
* **Безопасность:** Поддержка проверки версии сохранения.

### 🚀 Установка и использование
1.  Скачайте последнюю версию.
2.  **Важно:** Убедитесь, что `di2save.exe` и папка `data/` находятся в одной директории.
3.  Запустите `di2save_gui.exe`.
4.  Выберите путь к `di2save.exe` и вашему файлу сохранения (`.sav`).
5.  Используйте меню для внесения изменений.

### 🏆 Кредиты
* **Основной инструмент:** Этот GUI основан на **[Dead Island 2 Save Editor (CLI)](https://steffenl.com/projects/dead-island-2-save-editor)** от **SteffenL**.

---

## 简体中文 (Chinese)

### ✨ 主要功能
* **快速作弊:** 一键修改为满级 (Max Level) 和最大经验值 (Max XP)。
* **库存管理:**
    * 添加无限金钱。
    * 添加物品 (武器, 消耗品, 材料, 蓝图/卡片)。
    * 删除不需要的物品。
* **武器改装:**
    * 可视化编辑器: 查看和编辑武器升级槽。
    * 直接添加或移除模组 (Mods) 和专长 (Perks)。
* **安全性:** 支持版本安全检查功能。

### 🚀 安装与使用
1.  下载最新版本。
2.  **重要:** 请确保 `di2save.exe` 和 `data/` 文件夹与本程序在同一目录下。
3.  运行 `di2save_gui.exe`。
4.  选择 `di2save.exe` 路径和您的存档文件 (`.sav`)。
5.  在左侧菜单选择相应功能进行修改。

### 🏆 致谢
* **核心工具:** 本程序基于 **SteffenL** 开发的 **[Dead Island 2 Save Editor (CLI)](https://steffenl.com/projects/dead-island-2-save-editor)**。