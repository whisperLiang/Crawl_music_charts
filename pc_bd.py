import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # 输入框回车
from selenium.webdriver.common.by import By  # 与下面的2个都是等待时要用到
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException  # 异常处理
from selenium.webdriver.chrome.options import Options
import re
import os
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc("font",family='YouYuan')


class NetEaseCloud(object):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)\
             AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

    def __init__(self):
        # pass
        self.authors_all = []
        # self.download_url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(song_id)

    def get_html(self, request_url):  # 得到页面的html
        try:
            response = requests.get(request_url, headers=NetEaseCloud.headers, timeout=20)
            if response.status_code == 200:
                return response
        except TimeoutError:
            print("请求超时！")
            return None
        except Exception as er:
            print("其他错误：", er)
            return None

    def get_id(self):
        try:
            song_id = wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[2]/div/div[1]/table/tbody/tr[*]/td[2]/div/div/div/span/a')))
            title = wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[2]/div/div[1]/table/tbody/tr[*]/td[2]/div/div/div/span/a/b')))
            author = wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[2]/div/div[1]/table/tbody/tr[*]/td[4]/div/span')))
# /html/body/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/div/a[1]/b
            ids = []
            titles = []
            authors = []
            num = 1
            print("为你找到以下内容".center(30, '*'))
            print("序号\t", "歌名\t\t", "歌手")
            for i in range(0, len(song_id)):
                try:
                    ids.append(song_id[i].get_attribute("href"))   # 这儿是歌曲的id
                    titles.append(title[i].get_attribute('title'))  # 这是歌名
                    authors.append(author[i].get_attribute('title'))  # 这是歌手
                    print(num, "\t", titles[i], "\t\t", authors[i], "    ")
                    num += 1
                except:
                    pass
            # print("没到这儿吗")
            self.authors_all += authors
            is_index = int(input("\n选择下载序号,小于0取消下载>>").strip())
            if is_index < 0:
                print("您已取消该歌曲的下载")
                return None
            song_id = re.compile('htt.*?id\=(\d+)').findall(ids[is_index-1])[0]  # 将歌曲id匹配出来
            song_name = titles[is_index-1]
            # print("正在下载......")
            return song_id, song_name
        except TimeoutException:
            print("网络不佳，请重新下载")
            return None
        except NoSuchElementException:
            print("没有找到相关资源QAQ")
            return None
        except Exception as er:
            print("检测到异常错误，请重新下载： ", er)
            return None

    def download(self, song_id, song_name):
        # song_id, song_name = NetEaseCloud.get_id()
        download_url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(song_id)  # 歌曲下载的接口
        try:
            song_html = self.get_html(download_url)  # 访问下载页
            song_data = song_html.content  # 得到下载页的html.content(即歌曲数据的字节)
        except TimeoutError:
            print("检测到网络异常\n退出网易云音乐下载")
            return
        except:
            print("检测到异常\n退出网易云音乐下载")
            return
        try:
            save_path = 'music/{}.mp3'.format(song_name)
            true_path = os.path.abspath(save_path)  # 绝对路径
            print("下载中......")
            with open(save_path, 'wb') as f:
                try:
                    f.write(song_data)
                    print("{}已保存至{}".format(song_name, true_path))
                except Exception as er:
                    print("写入失败：", er)
        except Exception as err:
            print("文件找不到目录music：", err)

    def test(self, song_name):
        songs_name = []
        remove_str = ['/', '\\']
        for name in song_name:
            if name not in remove_str:
                songs_name.append(name)
            else:
                name = '&'
                songs_name.append(name)
        song_string = ''.join(songs_name)
        return song_string

    def net_ease_cloud_api(self,url):
        print("\n", "{:30}".format("正在使用网易云音乐VIP下载器"))
        try:
            # url = "https://music.163.com/#/discover/toplist"
            driver.get(url)
        except:
            print("网络连接异常！")
            return   # 利用return阻断程序
        try:
            driver.switch_to.frame('g_iframe')
            while True:
                song_id, song_name = self.get_id()  # 此时的song_name可能含有字符/,写文件时会报路径错误，所以要想验证
                if song_id is None or song_name is None:
                    break  # 这个None是用户不想下载时返回的
                else:
                    song_name = self.test(song_name)  # 若含有/或者\则转化为&
                    self.download(song_id, song_name)
        except Exception as er:
            print("检测到异常错误\n退出网易云音乐下载 ", er)
    


if __name__ == '__main__':
    toplists = {
    '飙升榜': 'https://music.163.com/discover/toplist?id=19723756',
    '原创榜': 'https://music.163.com/discover/toplist?id=2884035',
    '新歌榜': 'https://music.163.com/discover/toplist?id=3779629',
    '热歌榜': 'https://music.163.com/discover/toplist?id=3778678'
    }
    net_API = NetEaseCloud()
    print("{:^30}".format("欢迎使用VIP音乐破解"))
    if not os.path.exists("./music"):
        os.mkdir("./music/")
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)
        wait = WebDriverWait(driver, 15)
    except Exception as e:
        print("请先安装最新版Chrome浏览器!", e)

    try:
        for name, url in toplists.items():
            print(f'正在获取{name}的歌曲信息...')
            net_API.net_ease_cloud_api(url)
        driver.quit()
    except:
        print("请检查输入是否符合规范")
    # 假设字符串列表为strings

# 使用Counter模块统计字符串数量
string_counts = Counter(net_API.authors_all)

# 获取前10个最常见的歌手和它们的计数值
top_strings = string_counts.most_common(10)
top_strings_labels = [string for string, count in top_strings]
top_strings_counts = [count for string, count in top_strings]

# 绘制水平条形图
fig, ax = plt.subplots()
ax.barh(top_strings_labels, top_strings_counts)
ax.set_xlabel("数量")
ax.set_ylabel("歌手")
ax.set_title("前10个最受欢迎的歌手")
plt.show()





