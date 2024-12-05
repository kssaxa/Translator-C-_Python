import requests


def fetch_cpp_codes(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        print(f"ID: {data[len(data)-1]['id']}, Code: {data[len(data)-1]['cpp_code']}")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
    except ValueError:
        print("Ошибка при обработке JSON ответа.")


if __name__ == "__main__":

    # Используем функцию
    api_url = "https://6741de41e4647499008f0f47.mockapi.io/api/v1/code"
    fetch_cpp_codes(api_url)
