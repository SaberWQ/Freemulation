# Freemulation IDE 🚀

<center>

Потужний десктопний IDE-комбайн на Python із підтримкою Cython/C++, гнучким інтерфейсом та повним кастомізатором тем.

**[ 🇺🇦 Українська](#українська-секція) | [ 🇬🇧 English](#english-section)**

</center>

---

<a name="українська-секція"></a>
# 🇺🇦 Українська документація

Потужний, легко налаштовуваний десктопний IDE-комбайн, створений на Python із використанням **CustomTkinter**, **Pillow** та прискоренням критичних операцій за допомогою **C++ (Cython)**. Проєкт поєднує гнучкість сучасних інтерфейсів та високу продуктивність під час роботи з важкими файлами, базами даних та терміналами.

### 🌟 Основні особливості

* 🎨 **Повний кастомізатор тем (Color Picker)**: Унікальна «планшетка» налаштувань дозволяє змінювати абсолютно кожен колір інтерфейсу в реальному часі (акценти, фони редактора, сайдбару, панелей, вкладок) з можливістю миттєвого скидання до заводських налаштувань.
* 💻 **Множинні вкладки терміналів**: Незалежні термінальні сесії з підтримкою закриття кожної вкладки, автотрекінгом поточної робочої директорії (**CWD**) та керуванням процесами.
* ⚡ **Прискорення на C++ / Cython**: Використання нативного компільованого коду для швидкого створення Hex-дампів бінарних файлів та парсингу важких структур даних.
* 📂 **Адаптивний інтерфейс (Full Resizability)**: Повністю динамічні панелі (`PanedWindow`), що дозволяють вільно змінювати розміри робочої області «як у справжньому VS Code» без втрати контенту.
* 🗄 **Мультиформатні аналізатори**:
  * **SQLite Viewer**: Інтерактивний переглядач таблиць баз даних.
  * **Image Viewer**: Динамічний переглядач зображень з автоматичним масштабуванням через **Pillow** при зміні розміру вікна.
  * **Hex Viewer**: Швидкий дамп бінарних файлів.
* ⚠️ **Панель проблем (Problems)**: Зручний блок моніторингу помилок та синтаксису проєкту.

---

### 🛠 Технологічний стек

* **Python 3.10+**
* **CustomTkinter** (Сучасна надбудова над Tkinter)
* **Cython & C++** (Оптимізація обробки даних)
* **Pillow (PIL)** (Динамічна обробка медіафайлів)

---

### 📁 Архітектура проєкту

```text
VSCodePro/
│
├── core/
│   ├── __init__.py
│   ├── config.py          # Глобальні теми, палітри кольорів та шрифти
│   ├── terminal.py        # Сесії терміналів з трекінгом CWD та закриттям
│   └── menus.py           # Верхнє меню та динамічний кастомізатор кольорів
│
├── modules/
│   ├── __init__.py
│   ├── editor.py          # Редактор коду з підсвіткою синтаксису
│   └── analyzer.py        # Переглядачі SQLite, Hex та адаптивних зображень
│
├── fast_core/             # C++ / Cython модуль прискорення
│   ├── fast_analyzer.pyx
│   └── setup.py
│
└── main.py                # Головна точка входу в IDE

```
### ⚙️ Встановлення та запуск

#### Клонування репозиторію:

```bash
git clone https://github.com/SaberWQ/Freemulation.git
cd Freemulation-main
```

#### Встановлення залежностей:

```bash
pip install customtkinter pillow cython
```

#### Компіляція C++ / Cython модулів:

```bash
cd fast_core
python setup.py build_ext --inplace
cd ..
```

#### Запуск програми:

```bash
python manage.py
```

---

<a name="english-section"></a>
# 🇬🇧 English Documentation

A powerful, highly customizable desktop IDE built with Python using **CustomTkinter**, **Pillow**, and accelerated via **C++ (Cython)** for heavy file operations, databases, and terminal sessions.

### 🌟 Key Features

* 🎨 **Advanced Color Customizer**: Change every single UI color in real-time using a dedicated color picker panel, with an instant reset-to-defaults feature.
* 💻 **Multiple Terminal Tabs**: Independent terminal sessions with individual close buttons, active working directory (**CWD**) tracking, and process management.
* ⚡ **C++ / Cython Acceleration**: Native compiled code modules for fast hex dumps and data parsing.
* 📂 **Fully Resizable Layout**: Dynamic split panes allowing smooth resizing without content clipping.
* 🗄 **Multi-format Analyzers**:
    * **SQLite Viewer**: Interactive database table viewer.
    * **Image Viewer**: Dynamic image viewer with Pillow auto-scaling on window resize.
    * **Hex Viewer**: Fast binary file hex dump.
* ⚠️ **Problems Panel**: Dedicated monitoring block for project issues and logs.

---

### 🛠 Tech Stack

* **Python 3.10+**
* **CustomTkinter** (Modern Tkinter wrapper)
* **Cython & C++** (Data processing optimization)
* **Pillow (PIL)** (Dynamic media handling)

---

### ⚙️ Installation & Quick Start

#### Clone the repository:

```bash
git clone https://github.com/SaberWQ/Freemulation.git
cd Freemulation-main
```

#### Install dependencies:

```bash
pip install customtkinter pillow cython
```

#### Build C++ / Cython extensions:

```bash
cd fast_core
python setup.py build_ext --inplace
cd ..
```

#### Run the IDE:

```bash
python manage.py
```

---

### 📄 License

Distributed under the MIT License. See `LICENSE` for more information.