# RedSweep

🛡️ RedSweep é uma ferramenta de automação de reconhecimento ofensivo desenvolvida em Python, projetada para ajudar analistas de segurança a coletar rapidamente informações sobre alvos web, de forma modular, silenciosa e eficaz.

## 📌 Recursos

- Coleta de subdomínios usando Subfinder, Assetfinder e Amass
- Detecção de hosts ativos com Httpx
- Varredura de portas com Nmap
- Coleta de tecnologias com WhatWeb
- Extração de URLs via WaybackURLs
- Crawler com Hakrawler
- Captura de screenshots com Gowitness (opcional)
- Relatório final em JSON (`report.json`)
- Logs detalhados em `debug.log`
- ASCII art no terminal (porque estilo também importa 😎)

## ⚙️ Pré-requisitos

Você precisa ter os seguintes binários instalados e disponíveis no seu `$PATH`:

- `subfinder`
- `assetfinder`
- `amass`
- `httpx`
- `nmap`
- `whatweb`
- `waybackurls`
- `hakrawler`
- `gowitness` (opcional)

Instale-os via `go install` ou usando repositórios oficiais.

## 🧪 Uso

```bash
python redsweep.py example.com
```

### 🔧 Parâmetros

| Flag             | Descrição                                   |
|------------------|---------------------------------------------|
| `--no-gowitness` | Desativa captura de screenshots com gowitness |

### 📁 Estrutura de saída

```
redsweep_example.com_20250525_153000/
├── whois.txt
├── dns.txt
├── subdomains.txt
├── alive.txt
├── nmap.txt
├── whatweb.txt
├── waybackurls.txt
├── hakrawler.txt
├── gowitness.log (se habilitado)
├── screenshots/ (se habilitado)
├── report.json
├── debug.log
```

## 🛠️ Exemplo real

```bash
python redsweep.py target.com --no-gowitness
```

## 📜 Licença

Este projeto é open-source e está sob a licença MIT.

---

> ⚠️ **Aviso Legal:** Esta ferramenta é apenas para fins educacionais e de auditoria autorizada. O uso indevido pode ser considerado ilegal. Use com responsabilidade.

