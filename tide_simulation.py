import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


# Esssayer a mettre par jours le graphique et mettre sur 1 an pour voir les eclipset
# Essayer de mettre des paramettre modifiable : composantes, durée, intervale


# Définir les paramètres des composantes harmoniques avec des valeurs plus réalistes
composantes = {
    'M2': {'amplitude': 120, 'période': 12.42, 'phase': 145},
    'S2': {'amplitude': 40, 'période': 12.00, 'phase': 180},
    'N2': {'amplitude': 22, 'période': 12.66, 'phase': 160},
    'K1': {'amplitude': 10, 'période': 23.93, 'phase': 75},
    'O1': {'amplitude': 14, 'période': 25.82, 'phase': 60},
    'P1': {'amplitude': 8, 'période': 24.07, 'phase': 85},
    'K2': {'amplitude': 5, 'période': 11.97, 'phase': 195}
}

# Définir la durée de la simulation et l'intervalle de temps
durée = 48  # en heures
intervalle = 0.1  # en heures
temps = np.arange(0, durée, intervalle)

# Fonction pour calculer une composante harmonique
def composante_harmonique(amplitude, période, phase, temps):
    return amplitude * np.sin(2 * np.pi * temps / période + np.deg2rad(phase))

# Initialiser le niveau de la marée avec des valeurs nulles
niveau_maree = np.zeros_like(temps)
niveau_maree_sans_lune = np.zeros_like(temps)

# Préparer les couleurs pour chaque composante
couleurs = ['b', 'g', 'r', 'c', 'm', 'y', 'orange']

# Créer la figure et les axes
fig, ax = plt.subplots(figsize=(14, 8))
plt.subplots_adjust(right=0.8, top=0.85, bottom=0.2)

# Dictionnaire pour stocker les lignes tracées
lignes = {}

# Ajouter chaque composante harmonique au niveau de la marée et tracer chaque composante
for (nom, params), couleur in zip(composantes.items(), couleurs):
    y = composante_harmonique(params['amplitude'], params['période'], params['phase'], temps)
    niveau_maree += y
    if nom not in ['M2', 'N2', 'K1', 'O1']:
        niveau_maree_sans_lune += y
    ligne, = ax.plot(temps, y, label=f'{nom} (Amplitude: {params["amplitude"]} cm, Période: {params["période"]} h)', color=couleur, linestyle='--')
    lignes[nom] = ligne

# Tracer la marée totale
lignes['Marée totale'], = ax.plot(temps, niveau_maree, label='Marée totale', color='black', linewidth=2)
lignes['Marée sans Lune'], = ax.plot(temps, niveau_maree_sans_lune, label='Marée sans Lune', color='purple', linewidth=2, linestyle='-.')

# Ajouter les titres et les légendes
ax.set_title('Composantes harmoniques des marées à Biarritz')
ax.set_xlabel('Temps (heures)')
ax.set_ylabel('Niveau de la marée (cm)')
legende = ax.legend(loc='upper right')
ax.grid(True)
ax.set_xticks(np.arange(0, durée + 1, 6))
ax.set_yticks(np.arange(-200, 201, 50))

# Fonction de mise à jour de la visibilité des courbes
def on_pick(event):
    legend_line = event.artist
    is_visible = not legend_line.get_visible()
    legend_line.set_visible(is_visible)
    for line in lignes.values():
        if line.get_label() == legend_line.get_label():
            line.set_visible(is_visible)
    plt.draw()

for leg_line in legende.get_lines():
    leg_line.set_picker(True)
    leg_line.set_pickradius(5)

fig.canvas.mpl_connect('pick_event', on_pick)

# Ajouter un bouton pour cacher/afficher la légende
class LegendButton:
    def __init__(self, ax):
        self.visible = True
        self.button = Button(ax, 'Afficher/Cacher la légende')
        self.button.on_clicked(self.toggle_legend)

    def toggle_legend(self, event):
        self.visible = not self.visible
        legende.set_visible(self.visible)
        plt.draw()

# Ajouter le bouton de la légende en haut à droite
ax_button = plt.axes([0.83, 0.9, 0.15, 0.075])
legend_button = LegendButton(ax_button)

# Ajouter la formule mathématique
plt.text(0.5, 0.1, r'$h(t) = H_0 + \sum_{i} A_i \cdot \cos\left(\frac{2 \pi \cdot t}{période_i} + phase_i\right)$', 
         horizontalalignment='center', verticalalignment='center', transform=fig.transFigure, fontsize=12)

# Afficher le graphique
plt.show()
