import pprint
import re

# ex: '04/01/24, 19:21 - Alessandro:'
pattern = re.compile(r'\d{2}/\d{2}/\d{2}, \d{2}:\d{2} - (.*?): ')

#TODO generare la lista utenti invece di scriverla a mano
MEMBERS = ['Alessandro', 'Costa', 'Gianluca Forte', 'Irene', 'Simone Trentini', 'Solee🥤', 'Pear🍐', 'Alvise Tortato',
           'Daniel Xio', 'Davide Friselle', 'Davide Gobbo', 'Dibe', 'Edo Baldan', 'Erik Nuovo', 'Gabry Trama',
           'Giova Blasi', 'Leonardo Costantini', 'Magua', 'Nico Giusto', 'Nicola Parin', 'Riccardo Brembilla', 'Rudy',
           'Simone Ceolo', 'Simone Crovato', 'Thomas Pavan', 'Tia Maggiolo']

BADWORDS = ["Addio", "l'incendio", "idiota", "studio", "fastidio", "stipendio", "odio", "audio", "radio",
            "radiocomandata", "audiovisivi", "sdioppa", "episodio", "sdioppato", "Gvuardiol", "idioti",
            "misericordioso", "meridio", "presidio", "l'audio", "all'odio", "radio24", "stadio", "radio😂",
            "l’episodio"
            ]


def initialize_leaderboard(memebr_list: list[str]) -> dict[str, dict]:
    members_lead = {}
    for name in memebr_list:
        members_lead.update({name: {'tot': 0, 'blasphemies': {}}})
    return members_lead


def bestemmion_finder(text: str):
    words = text.split()
    results = []

    for i, w in enumerate(words):
        w_lower = w.lower()
        # controllo per i falsi positivi
        if w_lower in BADWORDS:
            continue
        # TODO mettere le parole da matchare in una lista
        if w_lower == 'dio' or w_lower == 'madonna':
            # Se la parola è 'dio', aggiungi 'dio + parola successiva'
            if i + 1 < len(words):
                results.append(w_lower + ' ' + words[i + 1])
        elif 'dio' in w_lower or 'madonna' in w_lower:
            # Se la parola contiene 'dio', aggiungi la parola al risultato
            results.append(w)

    return results


def elaborate_blasph():
    blasphemies_found = bestemmion_finder(''.join(current_data))
    for blasph in blasphemies_found:
        # la prima bestemmia viene inserita nella lista
        if not blasphemies_dict[current_user]['blasphemies']:
            blasphemies_dict[current_user]['blasphemies'].update({blasph: 1})
        else:
            if blasphemies_dict[current_user]['blasphemies'].get(blasph, None):
                blasphemies_dict[current_user]['blasphemies'][blasph] = blasphemies_dict[current_user]['blasphemies'][
                                                                            blasph] + 1
            else:
                blasphemies_dict[current_user]['blasphemies'].update({blasph: 1})


blasphemies_dict = initialize_leaderboard(MEMBERS)

with open('chat.txt', 'r', encoding='utf-8') as file:
    rows_data = []
    current_data = []
    current_user = None
    for line in file:
        match = pattern.match(line)
        # Se trova una corrispondenza con il pattern, inizia un nuovo blocco di dati
        if match:
            # elaboro i dati del blocco precedente prima di iniziare il possimo
            elaborate_blasph()

            current_user = match.group(1)
            if current_user not in MEMBERS:
                current_data = []
                continue

            # Questo if ha senso solo per il primo giro
            if current_data:
                rows_data.append(''.join(current_data))
                current_data = []

        # Aggiungi la riga corrente al blocco corrente eliminando il prefisso con data, ora e utente
        current_data.append(re.sub(pattern, '', line))

    # Aggiungi l'ultimo blocco alla lista (se presente)
    if current_data:
        elaborate_blasph()
        rows_data.append(''.join(current_data))

# ricavo il totale per membro
for user in blasphemies_dict:
    tot = 0
    for user_balsph in blasphemies_dict[user]['blasphemies']:
        tot = tot + blasphemies_dict[user]['blasphemies'][user_balsph]
    blasphemies_dict[user]['tot'] = tot

leaderboard = {}
sorted_user = sorted(blasphemies_dict, key=lambda x: blasphemies_dict[x]['tot'], reverse=True)
for user in sorted_user:
    leaderboard[user] = blasphemies_dict[user]['tot']

pprint.pprint(leaderboard, sort_dicts=False)
pprint.pprint(blasphemies_dict)
