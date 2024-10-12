import json
import pandas as pd
from web3 import Web3

# Настройки
RPC_URL = 'https://arbitrum.llamarpc.com/'  # Укажите здесь ваш RPC URL
CONTRACT_ADDRESS = '0xeba343f241217eabe4704ec6ae85d2ab8cf4c32a'  # Укажите адрес контракта
MINT_GROUPS = list(range(0, 3))  # Группы для минта, укажите диапазон по вашему усмотрению
OUTPUT_FILE = 'mint_results_eligible.csv'  # Имя выходного файла для экспорта

# Функция для проверки подключения к RPC
def check_rpc_connection(w3):
    try:
        block_number = w3.eth.block_number
        print(f"Соединение с RPC установлено. Текущий блок: {block_number}")
        return True
    except Exception as e:
        print(f"Ошибка подключения к RPC: {e}")
        return False

# Загрузка кошельков из файла wallets.txt
def load_wallets(filename, w3):
    with open(filename, 'r') as f:
        wallets = [line.strip() for line in f if line.strip()]
    checksum_wallets = [w3.to_checksum_address(wallet) for wallet in wallets]
    return checksum_wallets

# Функция для вызова метода mintQuotas
def check_mint_eligibility(w3, contract, group, wallet_address):
    return contract.functions.mintQuotas(group, wallet_address).call()

# Функция для сохранения результатов в файл CSV
def save_results_to_csv(results, filename):
    # Преобразуем результаты в список для pandas DataFrame
    data = []
    for wallet, wallet_results in results.items():
        for group, eligibility in wallet_results.items():
            if eligibility > 0:  # Отображаем только eligible кошельки
                data.append({
                    'Wallet': wallet,
                    'Mint Group': group,
                    'Eligibility': eligibility
                })
    
    # Создаем DataFrame и сохраняем в файл CSV
    if data:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Результаты сохранены в файл {filename}")
    else:
        print("Нет eligible кошельков для записи.")

def main():
    # Подключаемся к RPC узлу
    w3 = Web3(Web3.HTTPProvider(RPC_URL))

    # Проверяем подключение к RPC
    if not check_rpc_connection(w3):
        return

    # ABI контракта
    contract_abi = [{
        "inputs": [
            {"internalType": "uint256", "name": "mintId", "type": "uint256"},
            {"internalType": "address", "name": "", "type": "address"}
        ],
        "name": "mintQuotas",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }]
    
    # Преобразуем адрес контракта в checksum-формат
    contract_address = w3.to_checksum_address(CONTRACT_ADDRESS)

    # Инициализируем контракт
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    # Загрузка кошельков
    wallets = load_wallets('wallets.txt', w3)

    # Проверка возможности минта для каждой группы и кошелька
    results = {}
    for wallet in wallets:
        wallet_results = {}
        for group in MINT_GROUPS:
            try:
                eligibility = check_mint_eligibility(w3, contract, group, wallet)
                wallet_results[group] = eligibility
            except Exception as e:
                print(f"Ошибка для кошелька {wallet} в группе {group}: {str(e)}")
                wallet_results[group] = "Error"
        results[wallet] = wallet_results

    # Экспорт результатов в CSV (только eligible)
    save_results_to_csv(results, OUTPUT_FILE)

if __name__ == '__main__':
    main()
