import random
import csv
from paho.mqtt import client as mqtt_client


broker = 'test.mosquitto.org'
port = 1883
topic = "IUT/Colmar/SAE24/Maison1"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def traiter_donnee(mac,piece,date,time,temp):
    if mac == "B8A5F3569EFF":
        chaine = f"{mac};{piece};{date};{time};{temp};"
        file = open("capteur1.csv", "a")
        file.write(chaine + "\n")
        file.close()

    if mac == "A72E3F6B79BB":
        chaine = f"{mac};{piece};{date};{time};{temp};"
        file = open("capteur2.csv", "a")
        file.write(chaine + "\n")
        file.close()

    timestamp = date + " , " + time
    global id_donnee
    id_donnee += 1
    global mycursor
    sql = "INSERT INTO data (id,data,timestamp,capteur_id) VALUES (%s, %s, %s, %s)"
    if id == 'A72E3F6B79BB':
        val = (id_donnee,temp,timestamp,2)
    if id == "B8A5F3569EFF":
        val = (id_donnee, temp, timestamp,1)
    mycursor.execute(sql, val)

    mydb.commit()

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        donne = msg.payload.decode()

        data = donne.split(',')
        print(data)
        mac = data[0][3:len(data[0])]
        piece = data[1][6:len(data[1])]
        date = data[2][5:len(data[2])]
        time = data[3][5:len(data[3])]
        temp = data[4][5:len(data[4])]

        datafinal = []
        datafinal.append(mac)
        datafinal.append(piece)
        datafinal.append(date)
        datafinal.append(time)
        datafinal.append(temp)

        with open('read.csv','a+', newline='') as f:
            write = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            write.writerow(datafinal)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()