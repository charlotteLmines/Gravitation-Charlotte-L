import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, ax = plt.subplots()

ax.axis('equal')
ax.set(xlim=[-1, 100], ylim=[-1,100])

n=10 # Nombre de corps
G= 1 # Constante de gravitation modifiée pour avoir un beau rendu
m=1 # masse des corps en kg
dt=1 #pas de temps en s

# L'objectif est de créer un tableau qui pour chaque corps donne la distance à chaque autre
# corps, ainsi que les projections sur les deux axes

positions = np.random.randint(0,100,(n,2))

# On calcule une matrice carrée symétrique qui donne les vecteurs distances entrechaque corps,avec donc des 0 sur la diagonale
def vecteurdistances (positions):
    A=np.reshape(positions, (n,1,2))
    B=np.reshape(positions,(1,n,2))
    return A-B

# Pour le calcul de la force

def norme (r):
 return np.sqrt(r[:,:,0]**2 + r[:,:,1]**2)

 On calcule les vecteurs forces massiques de chaque corps sur un autre
def forcesm (vecteurdistances):
     distances=norme(vecteurdistances[:,:])
     np.fill_diagonal(distances, np.inf) #pour régler le problème de division par 0
     D=(-G*m*vecteurdistances[:,:])/(distances[:,:,None]**3)
     F=D.sum(axis=1) 
     return F

vites=np.zeros((n,2))

def vitesse (positions):
    F=forcesm(vecteurdistances(positions))
    dvx=F[:,0]*dt
    dvy=F[:,1]*dt
    return vites +np.array([dvx,dvy]).T

# On se sert de l'algorithme d'Euler pour déterminer le déplacement à partir des vecteurs forces précédents

def get_new_position(positions):
    vitesses=vitesse(positions)
    dx=vitesses[:,0]*dt
    dy=vitesses[:,1]*dt
    Xs = positions[:,0]
    Ys = positions[:,1]
    return positions+np.array([dx,dy]).T

scat = ax.scatter(positions[:,0],positions[:,1])

def animate(t):
# une variable globale est une variable utilisée dans une fonction mais dont la modification de la valeur a une portée globale (donc extérieure à la fonction)
    global positions
    global vites
    positions = get_new_position(positions)
    vites=vitesse(positions)

 # update the scatter plot:
 # le np.stack sert ici à mettre les positions dans la bonne shape

    data = np.stack(positions)
    scat.set_offsets(data)
    return scat

ani = animation.FuncAnimation(fig=fig, func=animate, interval=100)
plt.show()