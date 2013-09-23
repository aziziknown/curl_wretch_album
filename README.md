#curl wretch album (無名相簿備份)


這是一個備份無名相簿的小工具.

由於官方提供的備份僅有相簿名稱,照片網址,單張相片的名稱跟描述都沒有備份~~~~
當初打那些描述花了很多時間QQ~ 現在竟然不給備份QQ
網上找到的都是只有備份圖片而已的程式~~
所以決定自己弄一個~~
把相簿的style,相簿文字,相簿照片等等全部存下來的簡單小程式~
以網頁檔形式儲存方便觀看回味~~

介面頗陽春~

用法如下: 

### Usage: 

```python curl_wretch_album.py your_wretch_id [path_to_put_your_backup]```

or

```./curl_wretch_album.py your_wretch_id [path_to_put_your_backup]```


```your_wretch_id```--> 你在無名的帳號

```path_to_put_your_backup```--> 請自行換成你想要放備份的地方,若沒有填寫,則會存到跟python檔同一層的位置下wretch資料夾

程式會將你所有的相簿都下載到你指定的位置~~
下載完成後~ 請到你指定存放的位置~ 用瀏覽器打開開index.htm就可以觀看相簿了

### 其他資料
程式也會在跟python檔同層的地方,存下執行時抓下的一些文字資料~你可以自己決定是否要留下他們

### 已知問題
1. <script> </script>會變成<script/> 造成排版怪怪的
2. 最後一張相片的連結會錯
3. 第一頁 最後頁的連結可能會錯

