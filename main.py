import socketpool
import wifi
import elio
import time
from adafruit_httpserver import Server, Request, FileResponse


speed=100


#démarrage du point d’accès de l’esp32
wifi.radio.start_ap("Eliobot_AP", "Elio1234")
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

#création de la route principale 
@server.route("/")
def home(request: Request):
    """
    Serves the file /www/home.html.
    """

    return FileResponse(request, "home.html", "/www")

#création de la route qui récupère le bouton qui a été cliqué 
@server.route("/api/button-click", methods=['POST'])
def button_click(request: Request):
    try:
        data = request.json()
        button = data.get('button')
        # Faites quelque chose avec la valeur du bouton (button)
        print(f"Bouton cliqué : {button}")
        if button == "top":
            elio.moveForward(speed)
            time.sleep(1)
            elio.motorStop()
        if button == "bottom":
            elio.moveBackward(speed)
            time.sleep(1)
            elio.motorStop()
        if button == "left":
            elio.turnLeft(speed)
            time.sleep(0.475)
            elio.motorStop()
        if button == "right":
            elio.turnRight(speed)
            time.sleep(0.475)
            elio.motorStop()
        return 'OK'
    except Exception as e:
        print(f"Erreur lors de la gestion de la requête : {e}")
        return 'Erreur'



server.serve_forever(str(wifi.radio.ipv4_address_ap))


