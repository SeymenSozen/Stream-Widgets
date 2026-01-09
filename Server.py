import requests,time,flask,threading
from datetime import datetime
from colorama import Fore as f

def Get_Api_Key():
    try:
        with open("api.key", "r") as file:
            api_key = file.read().strip()
            print('Key okundu: ', api_key)
            return api_key
    except FileNotFoundError:
        print("API key dosyası bulunamadı...")
        return None
    except Exception as e:
        print(f"Hata: {e}")
        return None

app = flask.Flask("server")
Api_Key = Get_Api_Key()
Donate_Que = []
All_Donates = [] 
Last_Donate_Id = None
Per_Mounth = False
###Flask Bağış Bar Ayarları
## Donate Bar Hedef Ayarları
Hedef_Turar = 50000
Hedef_Metin = "İşlemci Sıvı Soğutma"
## Doante Alert Ayarları
Alret_Gif = "https://c.tenor.com/0oH_oZ43RxEAAAAd/tenor.gif"
Alett_Sound = "https://www.myinstants.com/media/sounds/sukaka-blyat.mp3"
Alert_Duration = 7  # saniye cinsinden

def process_donate(donate):
    isim = donate["nickName"]
    # if isim == "ByNoGame": return None
    if isim == "seymendomaltan": isim = "LuffyninHeyrani"
    tutar = donate["amount"]
    mesaj = donate["message"]
    ap_tarih = donate["date"]
    id = donate["_id"]
    dt_obj = datetime.fromisoformat(ap_tarih.replace("Z", "+00:00"))
    tarih = dt_obj.strftime("%d-%m-%Y %H:%M")
    return {"isim": isim, "tutar": tutar, "mesaj": mesaj, "tarih": tarih, "id": id}
def Fetch_Donates():
    global Last_Donate_Id, All_Donates
    p = 1
    if Api_Key is not None:
        try:
            print(f"{f.YELLOW}Geçmiş bağışlar çekiliyor...{f.RESET}")
            while True:
                api = f"https://api.bynogame.com/streamer/donatelist/{Api_Key}?filters=status:1&sort=date:-1&limit=100&page={p}"
                p += 1
                response = requests.get(api)
                response.raise_for_status()
                data = response.json()
                api_donates = data["data"]["data"]
                if not api_donates: break
                for donate in api_donates:
                    processed = process_donate(donate)
                    if processed:
                        All_Donates.append(processed)
                print(f"{f.GREEN} Sayfa {p-1} den çekilen: {len(api_donates)} {f.RESET}")
            if All_Donates:
                Last_Donate_Id = All_Donates[0]["id"]
            print(f"{f.YELLOW}Toplam {len(All_Donates)} bağış çekildi.{f.RESET}")
            return All_Donates
        except Exception as e:
            print(f"Hata oluştu: {e}")
            return []
def Track_Donates():
    global Last_Donate_Id, Donate_Que, All_Donates
    print(f"{f.CYAN}Canlı takip başlatıldı.{f.RESET}")
    while True:
        try:
            api = f"https://api.bynogame.com/streamer/donatelist/{Api_Key}?filters=status:1&sort=date:-1&limit=10&page=1"
            response = requests.get(api)
            data = response.json()
            api_donates = data["data"]["data"]
            new_found_donates = []
            for donate in api_donates:
                if donate["_id"] == Last_Donate_Id:
                    break             
                processed = process_donate(donate)
                if processed:
                    new_found_donates.append(processed)
            if new_found_donates:
                Last_Donate_Id = api_donates[0]["_id"]
                for donate in reversed(new_found_donates):
                    All_Donates.insert(0, donate)
                    Donate_Que.append(donate)
                    print(f"{f.GREEN}YENİ BAĞIŞ: {donate['isim']} {donate['tutar']} TL gönderdi: {donate['mesaj']} diyor. {f.RESET}")
        except KeyboardInterrupt:
            print(f"{f.RED}Takip durduruldu.{f.RESET}")
            break
        except Exception as e:
            print(f"{f.RED}Takip hatası: {e}{f.RESET}")
        time.sleep(15) 
def Get_Current_Month_Donates():
    """Sadece içinde bulunduğumuz aya ait bağışları filtreler"""
    global All_Donates
    simdi = datetime.now()
    bu_ay_listesi = []
    
    for donate in All_Donates:
        tarih = datetime.strptime(donate["tarih"], "%d-%m-%Y %H:%M")
        if tarih.month == simdi.month and tarih.year == simdi.year:
            bu_ay_listesi.append(donate)
    return bu_ay_listesi
def Total_Donates(per_month=Per_Mounth, include_bynogame=False):
    global All_Donates
    if per_month:
        veri_seti = Get_Current_Month_Donates()
        baslik = "--- BU AYIN ÖZETİ ---"
    else:
        veri_seti = All_Donates
        baslik = "--- TÜM ZAMANLARIN ÖZETİ ---"
    toplam = 0
    for d in veri_seti:
        if not include_bynogame and d["isim"] == "ByNoGame":
            continue
        toplam += float(d["tutar"])
    print(f"\n{f.CYAN}{baslik}{f.RESET}")
    print(f"Toplam Bağış Miktarı (ByNoGame Hariç): {round(toplam, 2)} TL")
    return round(toplam, 2)
def Top_5(per_month=Per_Mounth, include_bynogame=False):
    if per_month:
        veri_seti = Get_Current_Month_Donates()
    else:
        veri_seti = All_Donates    
    user_totals = {}
    for d in veri_seti:
        isim = d["isim"]
        if not include_bynogame and isim == "ByNoGame":
            continue        
        tutar = float(d["tutar"])
        user_totals[isim] = user_totals.get(isim, 0) + tutar
    sirali_liderler = sorted(user_totals.items(), key=lambda x: x[1], reverse=True)   
    label = "Aylık" if per_month else "Genel"
    print(f"\n{f.YELLOW}{label} Top 5 Liderlik Tablosu:{f.RESET}")
    ilk_bes = sirali_liderler[:5]
    for i, (isim, toplam_tutar) in enumerate(ilk_bes, 1):
        print(f"{i}. {isim}: {round(toplam_tutar, 2)} TL")
    return ilk_bes

@app.route("/donatebar")
def donate_bar():
    totaldonates = Total_Donates(per_month=Per_Mounth, include_bynogame=True)
    progress = min(int((totaldonates / Hedef_Turar) * 100), 100)
    return flask.render_template("DonateBar.html", total=totaldonates, hedef=Hedef_Turar, hedef_metin=Hedef_Metin, progress=progress)
@app.route("/donatealerts")
def donate_alert():
    global Donate_Que
    if Donate_Que:
        donate = Donate_Que.pop(0)
        return flask.render_template("DonateAlerts.html",isim=donate["isim"], tutar=donate["tutar"], mesaj=donate["mesaj"],gif=Alret_Gif, ses=Alett_Sound, sure=Alert_Duration)
    return flask.render_template("DonateAlerts.html", isim=None)
@app.route("/top5")
def top5():
    return flask.render_template("Top5.html", liderler=Top_5(per_month=False, include_bynogame=False))

if __name__ == "__main__":
    Fetch_Donates()
    Top_5(per_month=False, include_bynogame=False)
    Donate_Tracking = threading.Thread(target=Track_Donates, daemon=True)
    Donate_Tracking.start()
    app.run(host="0.0.0.0", port=33333, debug=False, use_reloader=False)
