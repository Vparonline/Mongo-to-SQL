import pymongo
import pymysql

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/içşarabısiarabı") # Mongo Adresiniz
mongodb_database = mongo_client["sectwist"]  # Veri Çekilecek Koleksiyon Adı
mongodb_collection = mongodb_database["userapi"] # Verininin Çekileceği Koleksiyonun İçindeki Şemanın Adı

sql_connection = pymysql.connect(host='localhost', # Aşağıyı MySQL Bilgileriniz İle Doldurun.
                                 user='root',
                                 password='',
                                 database='sectwist',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
sql_cursor = sql_connection.cursor()

belgeler = mongodb_collection.find()

for belge in belgeler:
    if "UserIp" in belge:
# UserIP Mongo verilerinde varsa kayıt ediyor bulamadığı takdirde alt tarafa geçip, sql'de UserIp'ye null atayıp verileri kaydetmeye devam ediyor.
        sql_cursor.execute("INSERT INTO verilerim (UserID, UserInformation, UserCreatedAt, UserGuildID, UserIP) VALUES (%s, %s, %s, %s, %s)",
                            (belge["UserID"], belge["UserInformation"], belge["UserCreatedAt"], belge["UserGuildID"], belge["UserIp"]))
    else:
        sql_cursor.execute("INSERT INTO verilerim (UserID, UserInformation, UserCreatedAt, UserGuildID) VALUES (%s, %s, %s, %s)",
                            (belge["UserID"], belge["UserInformation"], belge["UserCreatedAt"], belge["UserGuildID"]))

    sql_connection.commit()

    print("Yeni veri eklendi:")
    print(belge)

sql_cursor.close()
sql_connection.close()
