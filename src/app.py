import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv


def connect_spotify():
    """Inicializa la conexión a Spotify usando Client Credentials."""
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError("CLIENT_ID o CLIENT_SECRET no están definidos en el archivo .env")

    auth_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    return spotipy.Spotify(auth_manager=auth_manager)


def search_artist_id(sp, artist_name):
    """Busca el ID de un artista en Spotify."""
    results = sp.search(q=artist_name, type="artist", limit=1)
    
    if len(results["artists"]["items"]) == 0:
        print("No se encontró el artista. Intenta otro nombre.")
        return None
    
    return results["artists"]["items"][0]["id"]


def get_top_tracks(sp, artist_id):
    """Obtiene el top 10 de canciones de un artista."""
    data = sp.artist_top_tracks(artist_id)

    tracks = []
    for t in data["tracks"][:10]:
        tracks.append({
            "name": t["name"],
            "popularity": t["popularity"],
            "duration_min": round(t["duration_ms"] / 60000, 2)
        })

    return pd.DataFrame(tracks)


def main():
    print(" === SPOTIFY TOP TRACKS APP === ")

    sp = connect_spotify()

    artist_name = input("Ingrese el nombre del artista: ")

    artist_id = search_artist_id(sp, artist_name)
    if not artist_id:
        return

    print("Obteniendo el top 10 de canciones...")
    df = get_top_tracks(sp, artist_id)

    if df.empty:
        print("No se pudieron obtener canciones.")
        return

    # Mostrar resultado completo
    print("Top 10 canciones:")
    print(df)

    # Top canciones menos populares
    print("Top 3 menos populares:")
    print(df.sort_values("popularity").head(3))

    print("Análisis breve:")
    corr = df["duration_min"].corr(df["popularity"])
    if corr > 0.2:
        print("Canciones más largas tienden a ser más populares.")
    elif corr < -0.2:
        print("Canciones más cortas tienden a ser más populares.")
    else:
        print("No hay relación clara entre duración y popularidad.")
    print(f"Coeficiente de correlación: {corr:.3f}")



if __name__ == "__main__":
    main()
