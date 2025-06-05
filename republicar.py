from telethon.sync import TelegramClient
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon import events
import asyncio
import time
from datetime import datetime, time as dt_time
import pytz

# Configuración de la cuenta de usuario
API_ID = 25435727  # Tu API_ID
API_HASH = "0076e32ddbbc18e3ec950eb509b9211e"  # Tu API_HASH
PHONE_NUMBER = "+525663862985"  # Tu número de teléfono

# Lista de IDs de los grupos específicos donde enviar las publicaciones
TARGET_GROUP_IDS = [
    -1002546532470,  # ID del grupo 1
    -1234567890000   # ID del grupo 2
]

# Mensaje único para enviar a los grupos
POST = (
    "📞Números Virtuales 🇺🇸 EE.UU.\n"
    "Verifica cualquier tipo de cuenta 🚀\n\n"
    "💸 PayPal Verificado ☑ para 🇨🇺 Cuba. Te creamos la cuenta con tus datos y la verificamos 🧾💳\n"
    "¡Maneja tus dolares USD! 🧻🌎\n\n"
    "🎁 eSIM 🇲🇽 México: ¡1 solo número y creas todas tus cuentas! WhatsApp, Telegram, Instagram, etc.\n\n"
    "🛡VPN Enzona 👍 para navegar con cuenta nacional. También como VPN PREMIUM con IP fija 🎁\n\n"
    "SOY VIP ☑ 👑  👌🙊📖✨"
)

# Intervalo entre publicaciones (en segundos, 2 minutos = 120 segundos)
POST_INTERVAL = 120

# Palabras clave y respuestas para mensajes privados
KEYWORD_RESPONSES = {
    "numero": "Ofrecemos números virtuales de Estados Unidos🇺🇲 para registrarte en cualquier plataforma, ya sea Whatsapp, Telegram, iCloud, Apple, etc... \nSi deseas conocer los 💰precios, por favor escribe -> precios",
    "numeros": "Ofrecemos números virtuales de Estados Unidos🇺🇲 para registrarte en cualquier plataforma, ya sea Whatsapp, Telegram, iCloud, Apple, etc... \nSi deseas conocer los 💰precios, por favor escribe -> precios",
    "Numero": "Ofrecemos números virtuales de Estados Unidos🇺🇸 para registrarte en cualquier plataforma, ya sea Whatsapp, Telegram, iCloud, Apple, etc... \nSi deseas conocer los 💰precios, por favor escribe -> precios",
    "Numeros": "Ofrecemos números virtuales de Estados Unidos🇺🇲 para registrarte en cualquier plataforma, ya sea Whatsapp, Telegram, iCloud, Apple, etc... \nSi deseas conocer los 💰precios, por favor escribe -> precios",
    "números": "Ofrecemos números virtuales de Estados Unidos🇺🇲 para registrarte en cualquier plataforma, ya sea Whatsapp, Telegram, iCloud, Apple, etc... \nSi deseas conocer los 💰precios, por favor escribe -> precios",
    "Número": "Ofrecemos números virtuales de Estados Unidos🇺🇲 para registrarte en cualquier plataforma, ya sea Whatsapp, Telegram, iCloud, Apple, etc... \nSi deseas conocer los 💰precios, por favor escribe -> precios",
    "Números": "Ofrecemos números virtuales de Estados Unidos🇺🇲 para registrarte en cualquier plataforma, ya sea Whatsapp, Telegram, iCloud, Apple, etc... \nSi deseas conocer los 💰precios, por favor escribe -> precios",
    "#": "Ofrecemos números virtuales de Estados Unidos🇺🇲 para registrarte en cualquier plataforma, ya sea Whatsapp, Telegram, iCloud, Apple, etc... \nSi deseas conocer los 💰precios, por favor escribe -> precios",
    "usa": "Ofrecemos números virtuales de Estados Unidos🇺🇲 para registrarte en cualquier plataforma, ya sea Whatsapp, Telegram, iCloud, Apple, etc... \nSi deseas conocer los 💰precios, por favor escribe -> precios",
    "Usa": "Ofrecemos números virtuales de Estados Unidos🇺🇸 para registrarte en cualquier plataforma, ya sea Whatsapp, Telegram, iCloud, Apple, etc... \nSi deseas conocer los 💰precios, por favor escribe -> precios",
    "USA": "Ofrecemos números virtuales de Estados Unidos🇺🇲 para registrarte en cualquier plataforma, ya sea Whatsapp, Telegram, iCloud, Apple, etc... \nSi deseas conocer los 💰precios, por favor escribe -> precios",
    "canal": "https://youtu.be/OoA-Z1XOPbc",
    "Canal": "https://youtu.be/OoA-Z1XOPbc",
    "CANAL": "https://youtu.be/OoA-Z1XOPbc",
    "Canales": "https://youtu.be/OoA-Z1XOPbc",
    "canales": "https://youtu.be/OoA-Z1XOPbc",
    "CANALES": "https://youtu.be/OoA-Z1XOPbc",
    "Streaming": "https://youtu.be/OoA-Z1XOPbc",
    "streaming": "https://youtu.be/OoA-Z1XOPbc",
    "STREAMING": "https://youtu.be/OoA-Z1XOPbc",
    "virtual": "Ofrecemos números virtuales de Estados Unidos🇺🇸 para registrarte en cualquier plataforma, ya sea Whatsapp, Telegram, iCloud, Apple, etc... \nSi deseas conocer los 💰precios, por favor escribe -> precios",
    "Virtual": "Ofrecemos números virtuales de Estados Unidos🇺🇲 para registrarte en cualquier plataforma, ya sea Whatsapp, Telegram, iCloud, Apple, etc... \nSi deseas conocer los 💰precios, por favor escribe -> precios",
    "virtuales": "Ofrecemos números virtuales de Estados Unidos🇺🇸 para registrarte en cualquier plataforma, ya sea Whatsapp, Telegram, iCloud, Apple, etc... \nSi deseas conocer los 💰precios, por favor escribe -> precios",
    "Virtuales": "Ofrecemos números virtuales de Estados Unidos🇺🇸 para registrarte en cualquier plataforma, ya sea Whatsapp, Telegram, iCloud, Apple, etc... \nSi deseas conocer los 💰precios, por favor escribe -> precios",
    "PayPal": "Creamos y verificamos cuenta Paypal con tus datos, sin importar del pais que seas. Para los usuarios de Cuba🇨🇺 deben usar obligatoriamente un 🔒VPN, si no posees ninguno, yo te lo proporciono sin costo adicional.\nSi estas interesado escribe aqui debajo estos datos:\nNombre y Apellidos\nFecha de Nacimiento\nCorreo electronico. (el correo no puedes haberlo usado anteriormente en ninguna otra cuenta)\nSi te interesa saber el 💰precio por favor escribe -> precio",
    "paypal": "Creamos y verificamos cuenta Paypal con tus datos, sin importar del pais que seas. Para los usuarios de Cuba🇨🇺 deben usar obligatoriamente un 🔒VPN, si no posees ninguno, yo te lo proporciono sin costo adicional.\nSi estas interesado escribe aqui debajo estos datos:\nNombre y Apellidos\nFecha de Nacimiento\nCorreo electronico. (el correo no puedes haberlo usado anteriormente en ninguna otra cuenta)\nSi te interesa saber el 💰precio por favor escribe -> precio",
    "Paypal": "Creamos y verificamos cuenta Paypal con tus datos, sin importar del pais que seas. Para los usuarios de Cuba🇨🇺 deben usar obligatoriamente un 🔒VPN, si no posees ninguno, yo te lo proporciono sin costo adicional.\nSi estas interesado escribe aqui debajo estos datos:\nNombre y Apellidos\nFecha de Nacimiento\nCorreo electronico. (el correo no puedes haberlo usado anteriormente en ninguna otra cuenta)\nSi te interesa saber el 💰precio por favor escribe -> precio",
    "payPal": "Creamos y verificamos cuenta Paypal con tus datos, sin importar del pais que seas. Para los usuarios de Cuba🇨🇺 deben usar obligatoriamente un 🔒VPN, si no posees ninguno, yo te lo proporciono sin costo adicional.\nSi estas interesado escribe aqui debajo estos datos:\nNombre y Apellidos\nFecha de Nacimiento\nCorreo electronico. (el correo no puedes haberlo usado anteriormente en ninguna otra cuenta)\nSi te interesa saber el 💰precio por favor escribe -> precio",
    "PAYPAL": "Creamos y verificamos cuenta Paypal con tus datos, sin importar del pais que seas. Para los usuarios de Cuba🇨🇺 deben usar obligatoriamente un 🔒VPN, si no posees ninguno, yo te lo proporciono sin costo adicional.\nSi estas interesado escribe aqui debajo estos datos:\nNombre y Apellidos\nFecha de Nacimiento\nCorreo electronico. (el correo no puedes haberlo usado anteriormente en ninguna otra cuenta)\nSi te interesa saber el 💰precio por favor escribe -> precio",
    "Pay Pal": "Creamos y verificamos cuenta Paypal con tus datos, sin importar del pais que seas. Para los usuarios de Cuba🇨🇺 deben usar obligatoriamente un 🔒VPN, si no posees ninguno, yo te lo proporciono sin costo adicional.\nSi estas interesado escribe aqui debajo estos datos:\nNombre y Apellidos\nFecha de Nacimiento\nCorreo electronico. (el correo no puedes haberlo usado anteriormente en ninguna otra cuenta)\nSi te interesa saber el 💰precio por favor escribe -> precio",
    "Pay pal": "Creamos y verificamos cuenta Paypal con tus datos, sin importar del pais que seas. Para los usuarios de Cuba🇨🇺 deben usar obligatoriamente un 🔒VPN, si no posees ninguno, yo te lo proporciono sin costo adicional.\nSi estas interesado escribe aqui debajo estos datos:\nNombre y Apellidos\nFecha de Nacimiento\nCorreo electronico. (el correo no puedes haberlo usado anteriormente en ninguna otra cuenta)\nSi te interesa saber el 💰precio por favor escribe -> precio",
    "PAY PAL": "Creamos y verificamos cuenta Paypal con tus datos, sin importar del pais que seas. Para los usuarios de Cuba🇨🇺 deben usar obligatoriamente un 🔒VPN, si no posees ninguno, yo te lo proporciono sin costo adicional.\nSi estas interesado escribe aqui debajo estos datos:\nNombre y Apellidos\nFecha de Nacimiento\nCorreo electronico. (el correo no puedes haberlo usado anteriormente en ninguna otra cuenta)\nSi te interesa saber el 💰precio por favor escribe -> precio",
    "pay pal": "Creamos y verificamos cuenta Paypal con tus datos, sin importar del pais que seas. Para los usuarios de Cuba🇨🇺 deben usar obligatoriamente un 🔲VPN, si no posees uno, yo te lo proporciono sin costo adicional.\nSi estas interesado escribe aqui debajo estos datos:\nNombre y Apellidos\nFecha de Nacimiento\nCorreo electronico. (el correo no puedes haberlo usado anteriormente en ninguna otra cuenta)\nSi te interesa saber el 💰precio por favor escribe -> precio",
    "precios": "🏧Cuenta PayPal verificada -> 1\n\n📲Números Virtuales de 🇺🇸USA -> 2\n\n🔑VPN Nauta ✅ para Enzona -> 3\n\n📡Streaming para Servicio de Canales -> 4\n\nAhora solo escriba el número del cual necesitas información",
    "Precios": "🏧Cuenta PayPal verificada -> 1\n\n📲Números Virtuales de 🇺🇸USA -> 2\n\n🔑VPN Nauta ✅ para Enzona -> 3\n\n📡Servicio Streaming de Canales -> 4\n\nAhora solo escriba el número del cual necesitas información",
    "PRECIOS": "🏧Cuenta PayPal verificada -> 1\n\n📲Números Virtuales de 🇺🇸USA -> 2\n\n🔑VPN Nauta ✅ para Enzona -> 3\n\n📡Streaming para Servicio de Canales -> 4\n\nAhora solo escriba el número del cual necesitas información",
    "precio": "🏧Cuenta PayPal verificada -> 1\n\n📲Números Virtuales de 🇺🇸USA -> 2\n\n🔑VPN Nauta ✅ para Enzona -> 3\n\n📡Streaming para Servicio de Canales -> 4\n\nAhora solo escriba el número del cual necesitas información",
    "Precio": "🏧Cuenta PayPal verificada -> 1\n\n📲Números Virtuales de 🇺🇸USA -> 2\n\n🔑VPN Nauta -> 3\n\n📡Servicio Streaming de Canales -> 4\n\nAhora solo escriba el número del cual necesitas información",
    "PRECIO": "🏧Cuenta PayPal verificada -> 1\n\n📲Números Virtuales de 🇺🇸USA -> 2\n\n🔑VPN Nauta -> 3\n\n📡Servicio Streaming de Canales -> 4\n\nAhora solo escriba el número del cual necesitas información",
    "1": "Precio de PayPal💸\nCUP: $3500 (+ VPN Incluido)\nUSDT: 10 USDT Bep20",
    "2": "📲 Números Virtuales de 🇺🇸 USA (+1)\nOfrecemos métodos de pago: CUP, USDT (Binance u otra wallet cripto), Pix y PayPal. Los precios varían según la plataforma:\n\n✅ WhatsApp\n• 1000 CUP\n• 4 USDT\n• 4.9 USD (PayPal)\n• 26 Reales\n\n✅ Telegram\n• 2100 CUP\n• 5.5 USDT\n• 6.1 USD (PayPal)\n\n✅ Otras plataformas\n• 1000 USD\n• 4 USDT\n• 4.9 USD (PayPal)",
    "3": "VPN NAUTA Y ENZONA👍 -> $1099 CUP/mes",
    "4": "Servicio streaming + de 4mil canales💾 + de 3501 Películas y 6mil Series 🎥 -> $2000 CUP /mes\nNo necesita VPN\nPuedes conectar en 4 dispositivos a la vez"
}

# Generar un nombre de sesión único basado en el tiempo actual
SESSION_NAME = f"session_{int(time.time())}"

# Inicializar el cliente de Telegram
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Configuración de zona horaria para México (CDT, UTC-6)
MEXICO_TZ = pytz.timezone('America/Mexico_City')
START_TIME = dt_time(6, 0)  # 6:00 AM
END_TIME = dt_time(22, 0)   # 10:00 PM

async def is_within_time_window():
    """Verifica si la hora actual está dentro del horario de 6:00 AM a 10:00 PM (México)."""
    now = datetime.now(MEXICO_TZ).time()
    return START_TIME <= now <= END_TIME

async def time_until_next_start():
    """Calcula el tiempo en segundos hasta las próximas 6:00 AM (México)."""
    now = datetime.now(MEXICO_TZ)
    tomorrow = now + timedelta(days=1)
    next_start = MEXICO_TZ.localize(
        datetime.combine(tomorrow.date(), START_TIME)
    )
    return (next_start - now).total_seconds()

async def verify_group_access():
    """Verifica que la cuenta está en los grupos especificados."""
    valid_group_ids = []
    for group_id in TARGET_GROUP_IDS:
        try:
            group = await client.get_entity(group_id)
            valid_group_ids.append(group_id)
            print(f"Acceso confirmado al grupo: {group.title} ({group_id})")
        except Exception as e:
            print(f"Error: No se pudo acceder al grupo {group_id}: {e}")
    return valid_group_ids

async def send_automatic_post():
    """Envía el mensaje a los grupos dentro del horario establecido."""
    while True:
        try:
            # Verificar si está dentro del horario permitido
            if await is_within_time_window():
                group_ids = await verify_group_access()
                if not group_ids:
                    print("No hay grupos válidos para enviar mensajes.")
                    await asyncio.sleep(POST_INTERVAL)
                    continue
                try:
                    # Enviar el mensaje a Saved Messages
                    saved_message = await client.send_message('me', POST)
                    for chat_id in group_ids:
                        try:
                            # Reenviar el mensaje a cada grupo
                            await client(ForwardMessagesRequest(
                                from_peer='me',
                                id=[saved_message.id],
                                to_peer=chat_id
                            ))
                            print(f"Mensaje reenviado a {chat_id}: {POST[:50]}...")
                        except Exception as e:
                            print(f"Error al reenviar a {chat_id}: {e}")
                    # Esperar 2 minutos antes del próximo envío
                    await asyncio.sleep(POST_INTERVAL)
                except Exception as e:
                    print(f"Error al enviar mensaje a Saved Messages: {e}")
                    await asyncio.sleep(POST_INTERVAL)
            else:
                # Si está fuera del horario, esperar hasta las próximas 6:00 AM
                wait_time = await time_until_next_start()
                print(f"Fuera de horario. Esperando hasta las 6:00 AM (México) en {wait_time:.0f} segundos.")
                await asyncio.sleep(wait_time)
        except Exception as e:
            print(f"Error en send_automatic_post: {e}")
            await asyncio.sleep(60)  # Esperar 1 minuto antes de reintentar en caso de error

async def handle_private_message(event):
    """Maneja mensajes privados verificando si la respuesta ya fue enviada en todo el historial."""
    if event.is_private and event.sender_id != (await client.get_me()).id:
        message_text = event.message.text.lower()
        user_id = event.sender_id
        for keyword, response in KEYWORD_RESPONSES.items():
            if keyword in message_text:
                try:
                    # Revisar todo el historial de mensajes enviados por la cuenta en el chat
                    async for msg in client.iter_messages(user_id, from_user='me', limit=None):
                        if msg.text == response:
                            print(f"Respuesta ya enviada a {user_id} para la palabra clave '{keyword}'")
                            return  # No enviar si la respuesta ya está en el historial
                    # Enviar la respuesta si no se encontró en el historial
                    await event.respond(response)
                    print(f"Respondido a {user_id} con: {response}")
                except Exception as e:
                    print(f"Error al procesar mensaje de {user_id}: {e}")
                break

async def main():
    print("Bot iniciado...")
    try:
        # Iniciar el cliente de Telegram
        await client.start(phone=PHONE_NUMBER)
        
        # Registrar el manejador de mensajes privados
        client.on(events.NewMessage)(handle_private_message)
        
        # Ejecutar el envío de publicaciones automáticas
        await send_automatic_post()
    except Exception as e:
        print(f"Error en main: {e}")
    finally:
        await client.disconnect()
        print("Cliente desconectado.")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot detenido manualmente.")
    except Exception as e:
        print(f"Error fatal: {e}")
    finally:
        # Asegurarse de que el cliente se desconecte correctamente
        if client.is_connected():
            asyncio.run(client.disconnect())
        print("Programa finalizado.")