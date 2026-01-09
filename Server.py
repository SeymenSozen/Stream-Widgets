import requests

def Get_Api_Key():
    try:
        with open("api.key", "r") as file:
            api_key = file.read().strip()
            print('Key okundu: ', api_key)
            return api_key
    except FileNotFoundError:
        print("API key dosyası bulunamadı lütfen api.key adında bir dosya oluştur ve keyini buraya yapıştır.")
        return None
    except Exception as e:
        print(f"API key dosyası okunurken bir hata oluştu: {e}")
        return None
Api_Key = Get_Api_Key()




def Fetch_Donates():
    p = 1
    donates = []
    if Api_Key is not None:
        try:
            while True:
                api = f"https://api.bynogame.com/streamer/donatelist/{Api_Key}?filters=status:1&sort=date:-1&limit=100&page={p}"
                p += 1
                response = requests.get(api)
                response.raise_for_status()  # HTTP hatalarını kontrol et
                data = response.json()
                try:
                    current_donates = data["data"]["data"]
                    donates.extend(current_donates)
                except KeyError: break
                except TypeError: break

                print(f"Toplam bağış sayısı: {len(donates)}")
        except requests.exceptions.RequestException as e:
            print(f"API isteği sırasında bir hata oluştu: {e}")
        except ValueError:
            print("API yanıtı JSON formatında değil.")
        print(donates)
        return donates
if __name__ == "__main__":
    Fetch_Donates()