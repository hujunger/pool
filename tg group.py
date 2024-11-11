import requests
from telethon import TelegramClient, events, sync
import re

# Telegram API credentials
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
group_username = 'wangcai_8'  # 公共群组的用户名（如 t.me/wangcai_8）

# 测试节点连通性的 URL
TEST_URL = "https://www.gstatic.com/generate_204"
TIMEOUT = 5  # 设置连接超时（秒）

# 登录 Telegram
client = TelegramClient('session_name', api_id, api_hash)

def check_connectivity(ip_or_url):
    """测试节点连通性，返回 True 表示连通，False 表示超时或连接失败"""
    try:
        response = requests.get(TEST_URL, timeout=TIMEOUT)
        return response.status_code == 204  # 检查是否返回204状态码，表示无内容
    except requests.RequestException:
        return False

def save_valid_nodes(file_path, valid_nodes):
    """将有效节点保存到文件中"""
    with open(file_path, 'w') as file:
        for node in valid_nodes:
            file.write(node + "\n")

def main():
    with client:
        # 查找群组的消息
        messages = client.get_messages(group_username, limit=100)  # 获取最近100条消息
        valid_nodes = []

        for message in messages:
            if message.file and message.file.name.endswith('.txt'):
                # 下载 TXT 文件
                file_path = client.download_media(message, file="downloaded_nodes.txt")
                print(f"下载的文件路径: {file_path}")

                # 读取文件内容并测试连通性
                with open(file_path, 'r') as file:
                    nodes = file.read().splitlines()
                    for node in nodes:
                        if check_connectivity(node):
                            valid_nodes.append(node)
                            print(f"节点 {node} 可达")
                        else:
                            print(f"节点 {node} 超时或不可达")

                # 保存有效节点到文件
                save_valid_nodes("valid_nodes.txt", valid_nodes)
                print("测试完成，有效节点已保存到 valid_nodes.txt")
                break
        else:
            print("未找到任何 TXT 文件")

# 启动脚本
if __name__ == "__main__":
    client.start()
    main()