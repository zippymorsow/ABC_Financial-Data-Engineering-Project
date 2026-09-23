# ABC Financial

This is a tiny project called ABC Financial, used to migrate legacy ledger from source MSSQL into POSTGRES with proper ETL framework. This aims to showcase Data Integrations Engineering technical skills.

## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine.

**File tree**
```
abc_financial
├── config
│   ├── docker.yml
│   └── .env
├── logs
└──sql_scripts
│   └──seed_legacy_ledger.sql
├── config.py
└── README.md
```

### Prerequisites

What things you need to install the software and how to install them.
```bash
node -v
npm -v
```

### Installation

Step-by-step instructions to get a development environment running:

1. Clone the repository:
   ```bash
   git clone https://github.com
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
## Part 1: ETL Pipeline Setup
1. Create folder `abc_financial`,`logs`,`config`,`commons`, according to the file tree above.
2. Copy the whole contents `config`, & `commons` this contains important codes.
3. Update the value in `.env` for your set up.

## Docker Setup
1. Go to the directory of `compose.yml` in docker terminal and run:
```
docker compose -f compose.yml up -d
```


## 💻 Usage

Provide examples of how to use the project. Include helpful code blocks:

```bash
npm start
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
