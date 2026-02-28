import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("MONDAY_API_TOKEN")
DEALS_BOARD_ID = int(os.getenv("DEALS_BOARD_ID"))
WORK_BOARD_ID = int(os.getenv("WORK_BOARD_ID"))

API_URL = "https://api.monday.com/v2"


def fetch_board(board_id):

    query = f"""
    query {{
      boards(ids: {board_id}) {{
        items_page {{
          items {{
            name
            column_values {{
              text
              value
              column {{
                title
              }}
            }}
          }}
        }}
      }}
    }}
    """

    headers = {
        "Authorization": API_TOKEN.strip(),
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, json={"query": query}, headers=headers)
    data = response.json()

    if "errors" in data:
        raise Exception(f"Monday API Error: {data['errors']}")

    return data


def fetch_deals_live():
    return fetch_board(DEALS_BOARD_ID)


def fetch_work_live():
    return fetch_board(WORK_BOARD_ID)