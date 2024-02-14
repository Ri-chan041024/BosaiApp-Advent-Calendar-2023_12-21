#パッケージをインポートする
import requests
from bs4 import BeautifulSoup
import xmltodict

#大元のXMLのURLを指定
feed_url = 'https://www.data.jma.go.jp/developer/xml/feed/extra_l.xml'
#リクエスト(データを取得する)
feed_xml = requests.get(feed_url)
feed_soup = str(BeautifulSoup(feed_xml.content, "xml"))
#取得したXMLを、辞書型に変換する
feed_dict = xmltodict.parse(feed_soup)


#気象台と市町村名を指定
kisyodai = '金沢地方気象台'
city = '金沢市'

#XMLの中の'entry'の数だけ繰り返す
for i in range(len(feed_dict["feed"]["entry"])):
    print(f'i = {i}')

    #VPWW53が見つかったら
    if 'VPWW53' in feed_dict["feed"]["entry"][i]["id"]:

        #'金沢地方気象台'が見つかったら
        if  kisyodai == feed_dict["feed"]["entry"][i]["author"]["name"]:
            #リクエスト(データを取得する)
            VPWW53_xml = requests.get(feed_dict["feed"]["entry"][i]["id"])
            VPWW53_soup = str(BeautifulSoup(VPWW53_xml.content, "xml"))
            #取得したXMLを、辞書型に変換する
            VPWW53_dict = xmltodict.parse(VPWW53_soup)


            #市町村数を格納
            VPWW53_city_len = len(VPWW53_dict["jmx:Report"]["Body"]["Warning"][3]["Item"])

            #市町村の数だけ繰り返し
            for j in range(VPWW53_city_len):
                print(f'j = {j}')

                #'金沢市'が見つかったら
                if city == VPWW53_dict["jmx:Report"]["Body"]["Warning"][3]["Item"][j]["Area"]["Name"]:
                    print(city)
                    #金沢市の気象警報・注意報のデータを格納
                    kind = VPWW53_dict["jmx:Report"]["Body"]["Warning"][3]["Item"][j]["Kind"]
                    print(type(kind))
                    print(len(kind))


                    #気象警報・注意報が発表されていないとき
                    if type(kind) == dict and len(kind) == 1:
                        print('dict and len(kind)==1')
                        print('発表警報・注意報はなし')


                    #気象警報・注意報が1つのとき
                    elif type(kind) == dict:
                        print('dict')
                        status = VPWW53_dict["jmx:Report"]["Body"]["Warning"][3]["Item"][j]["Kind"]["Status"]

                        #気象警報・注意報が解除されていないとき
                        if status != '解除':
                            #気象警報・注意報名
                            warning = VPWW53_dict["jmx:Report"]["Body"]["Warning"][3]["Item"][j]["Kind"]["Name"]
                            print(warning)

                        #気象警報・注意報が解除されているとき
                        else:
                            print('dict_else')
                            print('発表警報・注意報はなし')


                    #気象警報・注意報が2つ以上のとき
                    elif type(kind) == list:
                        print('list')
                        warnings = []

                        #気象警報・注意報の数だけ繰り返し
                        for w in range(len(kind)):
                            print(f'w = {w}')
                            status = VPWW53_dict["jmx:Report"]["Body"]["Warning"][3]["Item"][j]["Kind"][w]["Status"]

                            #気象警報・注意報が解除されていないとき
                            if status != '解除':
                                #気象警報・注意報名
                                warning = VPWW53_dict["jmx:Report"]["Body"]["Warning"][3]["Item"][j]["Kind"][w]["Name"]
                                #気象警報・注意報名をリストに追加
                                warnings.append(warning)

                        #気象警報・注意報が1つ以上発表されているとき
                        if len(warnings) != 0:
                            for l in range(len(warnings)):
                                print(f'l = {l}')
                                print(warnings[l])

                        #気象警報・注意報が発表されていないとき
                        else:
                            print('list_else')
                            print('発表警報・注意報はなし')

                    break
            break






#                       #気象警報・注意報が発表されていないときのKindの構造 (dict型)
#                            'Kind': {
#                                'Status': '発表警報・注意報はなし'
#                            }
#
#
#                       #気象警報・注意報が1つのときのKindの構造 (dict型)
#                            'Kind': {
#                                'Name': '強風注意報',
#                                ...中略...
#                            }
#
#
#                       #気象警報・注意報が複数のときのKindの構造 (class型)
#                            'Kind': [
#                                  {
#                                        'Name': '波浪警報',
#                                        ...中略...
#                                  },
#                                  {
#                                        'Name': '雷注意報'
#                                        ...中略...
#                                  },
#                                  {
#                                        'Name': '強風注意報',
#                                        ...中略...
#                                  },
#                                       ...中略...
#                            ]
        


#               '発表', '継続', '解除', '発表警報・注意報はなし'