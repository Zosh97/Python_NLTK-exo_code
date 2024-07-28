import time
import instaloader
import re
from wordcloud import STOPWORDS, WordCloud
import matplotlib.pyplot as plt


#créer une instance d'Instaloader
L = instaloader.Instaloader()

#connexion à Instagram : il faudra bien remplacer les hashtags avec votre identifiant Instagram et votre mot de passe.
L.login('####', '####')
print("Connexion réussie")

#pour charger le profil de Marine Le Pen
profile = instaloader.Profile.from_username(L.context, 'marine_lepen')

#avoir le dernier poste
posts = profile.get_posts()
latest_post = next(posts)

#Récupérer les commentaires du dernier post
comments = ['']
for comment in latest_post.get_comments():
    comments.append(comment.text)

# récupérer les commentaires du dernier post avec des tentatives limitées
comments = []
attempts = 0
attempts = 5
succes = False

while attempts < max_attempts and not succes:
    try:
        for comment in latest_post.get_comments():
            comments.append(comment.text)
        succes = True
    except instaloader.exceptions.ConnectionException as e:
        print(f"Erreur lors de la récupéraion des commentaires : {e}")
        attempts += 1
        time.sleep(60)
if not succes:
    print("Impossible de récupérer les commentaires après plusieurs tentatives.")
    exit()


#afficher quelques commentaires pour vérifier
print(comments[:5])

#fonction pour nettoyer le texte: 1. mettre en minuscule 2.enlever les urls, mentions, hashtags et caractère spéciaux
def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+|@\S+|#\S+|[^a-zA-Z\s]', '', text, flags=re.MULTILINE)
    return text

#nettoyer les commentaires
cleaned_comments = [clean_text(comment) for comment in comments]

#afficher quelques commentaires nettoyés en un seul texte
print("Commentaires nettoyés", cleaned_comments[:5])


#concaténer tous les commentaires en un seul texte
text = ' '.join(cleaned_comments)

#définir les stops words en français
stopwords_fr = set(STOPWORDS)
stopwords_fr.update(["je", "tu", "il", "elle", "nous", "vous", "ils", "elles",
                     "le", "la", "les", "un", "une", "des", "et", "en", "à",
                     "de", "du", "que", "qui", "qu'", "au", "aux", "d'", "s'",
                     "l'", "y", "mais", "ou", "donc", "or", "ni", "car", "ce",
                     "cet", "cette", "ces", "mon", "ton", "son", "ma", "ta",
                     "sa", "mes", "tes", "ses", "notre", "votre", "leur", "nos",
                     "vos", "leurs", "ceci", "cela", "celui", "celle", "ceux",
                     "celles", "ici", "là", "où", "quand", "comme", "comment",
                     "être", "avoir", "faire", "pouvoir", "vouloir", "savoir",
                     "devoir", "falloir", "venir", "aller", "aussi", "si", "ainsi",
                     "plus", "moins", "très", "trop", "bien", "mal", "se", "ses",
                     "même", "c'", "s'", "n'", "t'", "d'", "qu'", "j'", "l'"])


#créer le nuage de mots
wordcloud = WordCloud(
    stopwords = stopwords_fr,
    background_color='white',
    width=800,
    height=400
).generate(text)

#afficher le nuage de mots
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()