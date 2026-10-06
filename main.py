import time
from config import UPDATE_INTERVAL
from monitor import get_network_stats
from security import detect_security_alert
from thingspeak import send_to_thingspeak, send_tel_message



def main():
    msg = ''
    issend = False
    print("=" * 50)
    print("IoT Security Monitoring System")
    print("Raspberry Pi Zero + ThingSpeak")
    print("=" * 50)

    while True:

        try:

            stats = get_network_stats()

            alert, reasons_list = detect_security_alert(stats)

            print("\nNetwork Statistics")
            print("-" * 30)

            print(f"Download : {stats['download']} KB/s")

            print(f"Upload   : {stats['upload']} KB/s")

            print(f"Connections : {stats['connections']}")

            print(f"TCP : {stats['tcp']}")

            print(f"UDP : {stats['udp']}")

            print(f"Interfaces : {stats['interfaces']}")

            print(f"Packets/s : {stats['packets']}")

            print(f"Security Alert : {alert}")

            if reasons_list:

                for reason in reasons_list:
                    msg += f"Reasons: - {reason}\n"
                    print(f"Reasons: - {reason}")

            send_to_thingspeak(
                stats,
                alert
            )
            if msg and not issend:
                time.sleep(1)
                send_tel_message(msg)
                issend = True
            print(f"\nNext update in {UPDATE_INTERVAL} seconds...")

            time.sleep(UPDATE_INTERVAL)

        except KeyboardInterrupt:

            print("\nProgram stopped.")

            break

        except Exception as e:

            print(f"Unexpected error: {e}")

            time.sleep(5)


if __name__ == "__main__":

    main()