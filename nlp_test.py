from konlpy.tag import Kkma
from konlpy.tag import Komoran
from konlpy.tag import Hannanum
from konlpy.tag import Okt 

punct = set(u''':!),.:;?.]}¢'"、。〉》」』〕〗〞︰︱︳﹐､﹒
﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､￠
々‖•·ˇˉ―′’”([{£¥'"‵〈《「『〔〖（［｛￡￥〝︵︷︹︻
︽︿﹁﹃﹙﹛﹝（｛“‘_…/''')

okt = Okt()
Komoran = Komoran()
Kkma = Kkma()
Hannanum = Hannanum()
text = """
정의당은 11일 문재인 대통령과 여권 인사들이 안희정 전 충남도지사의 부친상에 근조화환을 보낸 것을 두고 "아직도 반성이 없다"고 비판했다.

강민진 청년정의당 대표는 11일 자신의 페이스북에서 "안 전 지사 부친상에 문재인 대통령 명의의 근조화환이 놓였다. 여러 청와대와 민주당 인사들의 화환과 함께였다. 이런 행태를 보면 현 정부와 민주당은 아직도 반성이 없다. 권력형 성범죄로 징역을 사는 가해자를 여전히 '전 도지사'이자 같은 당 식구로 예우해주는 행위"라고 꼬집었다.

이어 "개인적인 조의를 표하고 싶었다면 사적인 방식으로 위로를 전했으면 될 일이다. 국민을 대표하는 대통령이라는 칭호를 활용해 공식적인 예우를 표해서는 안 된다"고 지적했다. 그러면서 "'안희정은 여전히 민주당의 동지'라는 인상을 주는 것, 그것이 민주당 지지자들에 의한 2차 가해 불씨이자 신호탄이 된다는 사실을 문재인 대통령과 민주당이 모를 리가 없다"고 설명했다.

그러면서 "민주당은 해당 사건 2차 가해자들을 영전시키고 청와대로 보내고 캠프에 직을 줬다. 그리고 이제 몇 달 뒤면 안희정 씨가 출소한다. 지금도 2차 가해에 고통받는 피해자를 위해, 지연된 정의일지언정 민주당이 이제라도 제대로 조치를 취하기를 촉구한다"고 했다.
"""
for i in punct:
    text.replace(i,"")

x = okt.nouns(text)
print("okt")
data= []
for i in x:
    if len(i)==1: continue
    data.append(i)
print(data)


# for i in x:
#     if len(i)==1: continue
#     data.append(i)
# print(data)

# x = Hannanum.nouns(text)
# print("Hannanum")
# data= []

# for i in x:
#     if len(i)==1: continue
#     data.append(i)
# print(data)

# x = Kkma.nouns(text)
# print("Kkma")
# data= []

# for i in x:
#     if len(i)==1: continue
#     data.append(i)
# print(data)