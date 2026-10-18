"""cubo.py - un cubo di Rubik 3x3 in poche righe.

Il cubo e' un DATO: un dizionario (posizione, normale) -> colore.
Le mosse sono FUNZIONI: prendono un cubo e ne restituiscono uno nuovo.
Stesso input, stesso output. Sempre.
"""
import random

# normale della faccia -> nome (e colore) della faccia
FACCE = {(0, 1, 0): "U", (0, -1, 0): "D", (1, 0, 0): "R",
         (-1, 0, 0): "L", (0, 0, 1): "F", (0, 0, -1): "B"}
# faccia -> (asse, verso): x=0, y=1, z=2
ASSE = {"U": (1, 1), "D": (1, -1), "R": (0, 1),
        "L": (0, -1), "F": (2, 1), "B": (2, -1)}


def risolto():
    cubo = {}
    for n, faccia in FACCE.items():
        i = n.index(1) if 1 in n else n.index(-1)
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                p = [a, b]
                p.insert(i, n[i])          # il pezzo sta sulla faccia n
                cubo[(tuple(p), n)] = faccia
    return cubo


def ruota90(v, i):
    """Rotazione di +90 gradi attorno all'asse i (regola della mano destra)."""
    x, y, z = v
    return ((x, -z, y), (z, y, -x), (-y, x, z))[i]


def mossa(cubo, m):
    """Applica una mossa (es. "R", "U'", "F2") e restituisce un nuovo cubo."""
    i, verso = ASSE[m[0]]
    giri = 3 if verso == 1 else 1          # orario visto dalla faccia
    if m.endswith("'"):
        giri = 4 - giri
    elif m.endswith("2"):
        giri = 2
    nuovo = {}
    for (p, n), colore in cubo.items():
        if p[i] == verso:                  # il pezzo e' nello strato che gira
            for _ in range(giri):
                p, n = ruota90(p, i), ruota90(n, i)
        nuovo[(p, n)] = colore
    return nuovo


def esegui(cubo, sequenza):
    for m in sequenza.split():
        cubo = mossa(cubo, m)
    return cubo


def e_risolto(cubo):
    return all(FACCE[n] == colore for (p, n), colore in cubo.items())


def periodo(sequenza):
    """Quante volte ripetere la sequenza prima di tornare al cubo risolto."""
    cubo, volte = esegui(risolto(), sequenza), 1
    while not e_risolto(cubo):
        cubo, volte = esegui(cubo, sequenza), volte + 1
    return volte


def mescola(n=20):
    mosse, ultima = [], ""
    while len(mosse) < n:
        f = random.choice("UDRLFB")
        if f != ultima:
            mosse.append(f + random.choice(["", "'", "2"]))
            ultima = f
    return " ".join(mosse)


if __name__ == "__main__":
    for s in ["R", "R U", "R U R' U'", "R U2"]:
        print(f"{s:10} -> periodo {periodo(s)}")
    m = mescola()
    c = esegui(risolto(), m)
    print("mescolato:", m, "| risolto?", e_risolto(c))
