# jenkins_ukol

Domácí úkol dle zadání stahuje informace o jednotlivých Jenkins jobech.

Skript byl napsán pod Ubuntu 18.04 se systémovým Pythonem 3.6:

Skript vyžaduje knihovnu requests. V případě její absence je třeba ji nainstalovat následujícím příkazem:

pip install requests

Skript se spouští jako:

python3 ukol.py

Je možné jej parametrizovat o výstupní adresář. Například:

python3 ukol.py /home/miroslav/jenkins_parser
