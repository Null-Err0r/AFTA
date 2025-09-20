# AFTA: Advanced Forensics Triage Assistant

<div align="left">
  <br><br>
  <a href="https://t.me/NullError_ir" target="_blank">
    <img src="https://img.shields.io/badge/Telegram-black?style=for-the-badge&logo=Telegram" alt="Telegram" />
  </a>
</div>
<br>

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
![https://img.shields.io/badge/Version-1.0-red.svg](https://img.shields.io/badge/Version-1.0-red.svg)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)

یک ابزار قدرتمند، سبک و سریع برای فارنزیک زنده (Live Forensics) در سیستم‌عامل‌های لینوکس است.
is a powerful, lightweight, and fast tool for live forensics on Linux operating systems.

این اسکریپت به تحلیلگران امنیت و تیم‌های پاسخ به حادثه (IR) کمک می‌کند تا در کوتاه‌ترین زمان ممکن، داده‌های فرّار و آرتیفکت‌های حیاتی را از یک سیستم در حال کار جمع‌آوری کرده و برای تحلیل‌های بعدی ذخیره نمایند.
This script helps security analysts and Incident Response (IR) teams to collect volatile data and critical artifacts from a live system as quickly as possible for subsequent analysis.

## هدف پروژه

## Project Goal

در شرایط پاسخ به حادثه، سرعت و دقت در جمع‌آوری شواهد اولیه حرف اول را می‌زند.
In an incident response scenario, speed and accuracy in collecting initial evidence are paramount.

 این ابزار فرآیند را خودکار کرده و با ارائه یک خروجی استاندارد و جامع، ریسک خطای انسانی و از دست رفتن داده‌های حیاتی را به حداقل می‌رساند.
This tool automates this process, minimizing the risk of human error and the loss of critical data by providing a standardized and comprehensive output.

این ابزار به عنوان یک اسکریپت triage عمل کرده و یک تصویر کلی از وضعیت سیستم در لحظه وقوع حادثه ارائه می‌دهد.
This tool acts as a triage script, providing a snapshot of the system's state at the moment of the incident.

-----

## ✨ ویژگی‌های کلیدی

## ✨ Key Features

  * **جمع‌آوری خودکار و سریع:** اجرای تنها یک فایل برای جمع‌آوری ده‌ها آرتیفکت مهم.

  * **Fast & Automated Collection:** Execute a single file to gather dozens of important artifacts.

  * **استخراج حافظه RAM:** دانلود خودکار آخرین نسخه **AVML** (از مایکروسافت) برای ایجاد یک تصویر کامل از حافظه.

  * **RAM Acquisition:** Automatically downloads the latest version of **AVML** (from Microsoft) to create a full memory image.

  * **پیکربندی آسان:** مدیریت کامل ماژول‌های جمع‌آوری از طریق یک فایل `config.yaml` ساده و خوانا.

  * **Easy Configuration:** Full control over collection modules via a simple and readable `config.yaml` file.

  * **نصب خودکار پیش‌نیازها:** اسکریپت به طور خودکار کتابخانه‌های پایتون مورد نیاز را نصب می‌کند.

  * **Automatic Dependency Installation:** The script automatically installs required Python libraries.

  * **خروجی جامع و ساختاریافته:** تمام داده‌ها در یک فایل `report.json` و آرتیفکت‌های فایلی در کنار آن، در نهایت در یک فایل `.zip` فشرده می‌شوند.

  * **Comprehensive & Structured Output:** All data is saved in a `report.json` file, alongside file-based artifacts, and finally compressed into a single `.zip` archive.

  * **لاگ‌گیری کامل:** تمام اقدامات و خطاهای احتمالی در یک فایل لاگ مجزا ثبت می‌شوند تا فرآیند جمع‌آوری قابل بازبینی باشد.

  * **Full Logging:** All actions and potential errors are recorded in a separate log file, making the collection process auditable.

  * **سبک و قابل حمل:** بدون نیاز به نصب پیچیده؛ تنها به پایتون ۳ نیاز دارد.

  * **Lightweight & Portable:** No complex installation required; only Python 3 is needed.

-----

## نصب و راه‌اندازی

## Installation & Setup

راه‌اندازی AFTA بسیار ساده است. تنها به **+ Python 3.6 ** و دسترسی **root** روی سیستم هدف نیاز دارید.
Setting up AFTA is very simple. You only need **Python 3.6+** and **root** access on the target system.

**۱. کلون کردن ریپازیتوری:**
**1. Clone the repository:**

```bash
git clone https://github.com/YourUsername/AFTA.git
```

**۲. ورود به دایرکتوری پروژه:**
**2. Navigate to the project directory:**

```bash
cd AFTA
```

اسکریپت به صورت خودکار پیش‌نیازهای پایتون (`requests` و `PyYAML`) را با استفاده از فایل `requirements.txt` نصب خواهد کرد.
The script will automatically install the Python prerequisites (`requests` and `PyYAML`) using the `requirements.txt` file.

-----

## نحوه استفاده

## Usage

تمام عملیات از طریق فایل اصلی اسکریپت و با دسترسی `root` انجام می‌شود.
All operations are performed via the main script file with `root` access.

```bash
sudo python3 afta.py
```

پس از اجرای دستور بالا، اسکریپت:
After running the command above, the script will:

1.  پیش‌نیازها را بررسی و نصب می‌کند.

2.  Check and install dependencies.

3.  در صورت نیاز، آخرین نسخه AVML را دانلود می‌کند.

4.  Download the latest version of AVML if needed.

5.  بر اساس فایل `config.yaml` شروع به جمع‌آوری داده‌ها می‌کند.

6.  Start collecting data based on the `config.yaml` file.

7.  در پایان، یک فایل فشرده `.zip` با نام `forensics_output_[hostname]_[timestamp].zip` در همان دایرکتوری ایجاد می‌کند.

8.  Finally, create a compressed `.zip` file named `forensics_output_[hostname]_[timestamp].zip` in the same directory.

### پیکربندی (`config.yaml`)

### Configuration (`config.yaml`)

قلب تپنده AFTA فایل `config.yaml` است. شما می‌توانید با ویرایش این فایل، دقیقاً مشخص کنید کدام داده‌ها جمع‌آوری شوند.
The heart of AFTA is the `config.yaml` file. By editing this file, you can specify exactly which data should be collected.

```yaml
collection_toggles:
  system_info: true
  process_info: true
  network_info: true
  memory_dump: true
  filesystem_artifacts: true
  hash_critical_binaries: true
  suid_sgid_files: true
```

برای غیرفعال کردن هر بخش، کافیست مقدار آن را به `false` تغییر دهید.
To disable any section, simply change its value to `false`.

-----

## ساختار خروجی

## Output Structure

پس از اتمام کار، یک فایل `.zip` دریافت خواهید کرد که ساختار داخلی آن به شکل زیر است:
After completion, you will receive a `.zip` file with the following internal structure:

```
forensics_output_hostname_2025-09-20_11-30-00.zip
└── forensics_output_hostname_2025-09-20_11-30-00/
    ├── report.json                 # خروجی اصلی شامل اطلاعات سیستم، شبکه، پردازش‌ها و...
                                    # Main output including system, network, process info, etc.
    ├── forensics_run.log           # لاگ کامل اجرای اسکریپت
                                    # Complete log of the script's execution.
    ├── memory.mem                  # تصویر حافظه RAM (در صورت فعال بودن)
                                    # RAM image (if enabled).
    └── fs_artifacts/               # پوشه حاوی آرتیفکت‌های کپی شده از سیستم
                                    # Directory containing artifacts copied from the system.
        ├── syslog
        ├── auth.log
        ├── root_.bash_history
        ├── user1_.bash_history
        └── ...
```

-----

## داده‌های جمع‌آوری شده

## Collected Data

AFTA طیف وسیعی از داده‌های حیاتی را جمع‌آوری می‌کند:
AFTA collects a wide range of critical data:

  * **اطلاعات سیستم:** نام هاست، مشخصات سیستم‌عامل، معماری، آپ‌تایم، ماژول‌های کرنل بارگذاری شده.

  * **System Info:** Hostname, OS details, architecture, uptime, loaded kernel modules.

  * **اطلاعات پردازش‌ها:** لیست کامل پردازش‌ها با جزئیاتی مانند PID, PPID، مسیر اجرایی، کاربر و زمان ایجاد.

  * **Process Info:** A complete list of processes with details like PID, PPID, executable path, user, and creation time.

  * **اطلاعات شبکه:** اتصالات فعال، پورت‌های در حال شنود، جداول مسیریابی و تنظیمات کارت‌های شبکه.

  * **Network Info:** Active connections, listening ports, routing tables, and network interface configurations.

  * **حافظه RAM:** یک تصویر کامل و خام از حافظه فیزیکی سیستم با استفاده از AVML.

  * **RAM:** A full, raw image of the system's physical memory using AVML.

  * **آرتیفکت‌های فایل سیستم:**

  * **Filesystem Artifacts:**

      * لاگ‌های مهم سیستمی (`/var/log/...`).
      * Important system logs (`/var/log/...`).
      * تاریخچه دستورات Shell برای تمام کاربران (`.bash_history`, `.zsh_history`, ...).
      * Shell history for all users (`.bash_history`, `.zsh_history`, ...).
      * کلیدهای `authorized_keys` کاربران برای بررسی دسترسی‌های SSH.
      * Users' `authorized_keys` files for auditing SSH access.

  * **تحلیل‌های امنیتی:**

  * **Security Analyses:**

      * لیست فایل‌های با بیت SUID/SGID برای شناسایی راه‌های بالقوه افزایش دسترسی.
      * A list of files with SUID/SGID bits set to identify potential privilege escalation paths.
      * هش SHA256 از باینری‌های موجود در مسیرهای سیستمی مهم برای مقایسه با نمونه‌های سالم (Hashing).
      * SHA256 hashes of binaries in critical system paths for comparison against known-good samples (Hashing).

-----

## مشارکت

## Contributing

از مشارکت شما در این پروژه استقبال می‌شود.
Contributions to this project are welcome.

## 📜 لایسنس

## 📜 License

این پروژه تحت لایسنس MIT منتشر شده است. برای اطلاعات بیشتر فایل `LICENSE` را مطالعه کنید.
This project is released under the MIT License. See the `LICENSE` file for more details.

![Repo Badge](https://visitor-badge.laobi.icu/badge?page_id=null-err0r.AFTA) 
