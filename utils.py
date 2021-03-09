import json
import base64



def text_to_base(texto="NO INGRESASTE NADA"):
    message_bytes=texto.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message
    
def base_to_text(base="Tk8gSU5HUkVTQVNURSBOQURB"):
    message_bytes=base.encode('ascii')
    base64_bytes = base64.b64decode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message
    


if __name__ == "__main__":
    print(text_to_base())
    print(base_to_text())