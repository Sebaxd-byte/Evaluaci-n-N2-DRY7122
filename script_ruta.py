import requests
import json


API_KEY = "94db92c6-5fa6-4919-a696-ea8f5fd8cedb"

def obtener_coordenadas(ciudad):
    """Convierte el nombre de una ciudad en coordenadas (lat, lon) usando Geocoding API"""
    url_geocode = f"https://graphhopper.com/api/1/geocode?q={ciudad}&locale=es&key={API_KEY}"
    response = requests.get(url_geocode)
    
    if response.status_code == 200:
        datos = response.json()
        if datos.get("hits"):

            point = datos["hits"][0]["point"]
            return point["lat"], point["lng"]
    return None

def calcular_ruta(orig_name, dest_name, lat1, lon1, lat2, lon2):
    """Calcula la ruta entre dos coordenadas usando Routing API"""
    url_route = f"https://graphhopper.com/api/1/route?point={lat1},{lon1}&point={lat2},{lon2}&vehicle=car&locale=es&instructions=true&key={API_KEY}"
    response = requests.get(url_route)
    
    if response.status_code == 200:
        datos = response.json()
        ruta = datos["paths"][0]
        
        
        distancia_km = ruta["distance"] / 1000
        
        
        tiempo_ms = ruta["time"]
        total_segundos = int(tiempo_ms / 1000)
        horas = total_segundos // 3600
        minutos = (total_segundos % 3600) // 60
        segundos = total_segundos % 60
        
        
        RENDIMIENTO_KM_L = 12.0
        combustible_litros = distancia_km / RENDIMIENTO_KM_L
        
        
        print("\n" + "="*40)
        print(f"RESUMEN DEL VIAJE: {orig_name.upper()} -> {dest_name.upper()}")
        print("="*40)
        print(f"• Distancia: {distancia_km:.2f} km")
        print(f"• Duración: {horas} horas, {minutos} minutos y {segundos} segundos")
        print(f"• Combustible requerido: {combustible_litros:.2f} litros (Rendimiento: {RENDIMIENTO_KM_L} km/L)")
        print("="*40)
        
        
        print("\nNARRATIVA DEL VIAJE (RUTA):")
        print("-" * 40)
        for idx, paso in enumerate(ruta["instructions"], 1):
            texto = paso["text"]
            dist_paso = paso["distance"] / 1000
            print(f"{idx}. {texto} ({dist_paso:.2f} km)")
        print("-" * 40)
        
    else:
        print(f"Error al calcular la ruta. Código de estado: {response.status_code}")

def main():
    print("--- Sistema de Planificación de Rutas (Graphhopper) ---")
    print("Escriba 'q' o 'quit' en cualquier momento para salir del programa.\n")
    
    while True:
        
        origen = input("Ingrese Ciudad de Origen: ").strip()
        if origen.lower() in ['q', 'quit']:
            print("Saliendo del programa... ¡Buen viaje!")
            break
            
        
        destino = input("Ingrese Ciudad de Destino: ").strip()
        if destino.lower() in ['q', 'quit']:
            print("Saliendo del programa... ¡Buen viaje!")
            break
            
        if not origen or not destino:
            print("Error: El origen y el destino no pueden estar vacíos.\n")
            continue
            
        print(f"\nBuscando coordenadas para {origen} y {destino}...")
        coords_origen = obtener_coordenadas(origen)
        coords_destino = obtener_coordenadas(destino)
        
        if coords_origen and coords_destino:
            lat1, lon1 = coords_origen
            lat2, lon2 = coords_destino
          
            calcular_ruta(origen, destino, lat1, lon1, lat2, lon2)
        else:
            print("No se pudieron encontrar las coordenadas de alguna de las ciudades. Intente nuevamente.")
        
        print("\n" + "_"*50 + "\n")

if __name__ == "__main__":
    main()
