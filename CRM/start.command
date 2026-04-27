#!/bin/bash
cd "$(dirname "$0")"
echo ""
echo "══════════════════════════════════════"
echo "  NBB CRM — starter op..."
echo "══════════════════════════════════════"
echo ""

# Tjek Python
if ! command -v python3 &>/dev/null; then
  echo "❌ Python3 er ikke installeret."
  echo "   Hent det fra https://www.python.org og prøv igen."
  read -p "Tryk Enter for at lukke..."
  exit 1
fi

# Installer afhængigheder
echo "📦 Installerer nødvendige pakker..."
pip3 install -r requirements.txt -q

echo "✅ Klar — åbner i browseren..."
echo "   Stop: luk dette vindue eller tryk Ctrl+C"
echo ""

DEMO=true python3 app.py
