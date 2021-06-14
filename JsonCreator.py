import json

data = {}
data['courant']= []
data['courant'].append({
    'nom': 'courant',
    'front': 'm',
    'poids': 'lien/vers/les/poids', #poids correspond au nom des poids : à display à l'utilisateur
    'exposition': '95',
    'lumiere': '20',
    'langue':'fr',
    'taillecycle':"50"
})
for i in range (1, 50):
    data['program'+str(i)] = []
    data['program'+str(i)].append({
        'nom': 'void',
        'front': 'void',
        'poids': 'void',  # poids correspond au nom des poids : à display à l'utilisateur
        'exposition': 'void',
        'lumiere': 'void'
    })

with open('Site/MyVisionia/siteweb/sauvegarde.json','w') as outfile:
    json.dump(data, outfile)

