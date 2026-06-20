# Claude Code CLI Integration

Claude Code adalah *agent* berbasis terminal dari Anthropic yang memiliki akses langsung ke *file system* dan kemampuan untuk menjalankan perintah secara mandiri. Karena sifatnya yang otonom, sangat penting untuk menyuntikkan **Agentfull DNA** ke dalamnya agar tidak melakukan tindakan destruktif.

## Cara Instalasi

1. Pastikan Anda telah menginstal Claude Code secara global:
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```
2. Jalankan `claude` di direktori proyek Anda.
3. Anda bisa mengarahkan Claude Code untuk mengadopsi instruksi Agentfull dengan menggunakan flag `--prompt-file` atau menyimpannya di file `.clauderc`.

### Metode 1: Perintah Langsung (Rekomendasi)
Gunakan perintah ini untuk memulai sesi Claude Code yang dibekali dengan DNA Agentfull:
```bash
claude --prompt-file path/to/agentfull/integrations/claude-code-cli/CLAUDE_PROMPT.md
```

### Metode 2: Konfigurasi Permanen (.clauderc)
Salin seluruh isi `CLAUDE_PROMPT.md` dan tambahkan ke dalam file `.clauderc` di direktori *root* Anda untuk menjadikan aturan ini sebagai standar permanen setiap kali Anda mengetik `claude`.
