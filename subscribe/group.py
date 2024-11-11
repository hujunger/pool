import os
from telethon import TelegramClient
import requests

# 从环境变量中获取 API_ID, API_HASH 和 Bot Token
API_ID = int(os.getenv('TELEGRAM_API_ID'))
API_HASH = os.getenv('TELEGRAM_API_HASH')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_NAME = 'wangcai_8'

# 初始化客户端并使用 Bot Token 启动
client = TelegramClient('bot_session', api_id=API_ID, api_hash=API_HASH).start(bot_token=BOT_TOKEN)

# 下载 TXT 文件
def download_txt_file():
    messages = client.get_messages(CHANNEL_NAME, limit=10)  # 获取最近10条消息
    for message in messages:
        if message.file and message.file.name.endswith('.txt'):
            message.download_media(file='nodes.txt')
            print("TXT 文件下载成功！")
            return 'nodes.txt'
    print("未找到 TXT 文件。")
    return None

# 测试连通性
def test_connectivity(url):
    try:
        response = requests.get(url, timeout=3)
        return response.status_code == 204
    except requests.RequestException:
        return False

# 解析文件并筛选可连通的节点
def filter_nodes(file_path):
    with open(file_path, 'r') as file:
        nodes = file.readlines()

    reachable_nodes = []
    for node in nodes:
        node = node.strip()
        if test_connectivity(node):
            reachable_nodes.append(node)

    with open('reachable_nodes.txt', 'w') as file:
        file.write('\n'.join(reachable_nodes))

    print(f"可连接的节点已保存至 reachable_nodes.txt，共找到 {len(reachable_nodes)} 个节点。")

# 执行流程
file_path = download_txt_file()
if file_path:
    filter_nodes(file_path)

# 断开客户端
client.disconnect()
