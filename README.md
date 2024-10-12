# NFT Mint Eligibility Checker

Этот проект проверяет возможность минта для группы кошельков в смарт-контракте. Результаты сохраняются в CSV-файл, отображая только те кошельки, которые eligible.

## Требования

Для работы скрипта требуются следующие библиотеки Python:

- `web3` для взаимодействия с блокчейном
- `pandas` для экспорта данных в CSV

## Установка

1. Клонируйте репозиторий или скопируйте скрипт на ваш компьютер.
2. Установите зависимости с помощью файла `requirements.txt`:

   ```bash
   pip install -r requirements.txt

3. Убедитесь, что у вас есть файл с кошельками wallets.txt, в котором каждый адрес находится на отдельной строке.


## Настройка
Перед запуском скрипта отредактируйте переменные в начале файла:

RPC_URL: URL RPC сервера для сети, где развернут контракт.
CONTRACT_ADDRESS: адрес смарт-контракта.
MINT_GROUPS: диапазон групп минта, которые нужно проверить.
OUTPUT_FILE: имя файла, в который будет сохранён результат.


## Запуск


Скрипт проверит возможность минта для всех кошельков и групп, указанных в настройках, и сохранит результаты в файл CSV. В файле будут отображены только кошельки, eligible для минта.

Пример файла wallets.txt
Пример содержания файла wallets.txt:
0x1234567890abcdef1234567890abcdef12345678
0xabcdef1234567890abcdef1234567890abcdef12
0x7890abcdef1234567890abcdef1234567890abcd
Каждый адрес должен быть записан в отдельной строке.