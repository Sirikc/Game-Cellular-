import requests
def request_for_movement_chip(chip_uid, chip_move):
  return requests.post("http://127.0.0.1:5000/api/movement_chip", json={"chip_uid": chip_uid, "chip_move": chip_move}).json()


# print(request_for_movement_chip(1, 2))