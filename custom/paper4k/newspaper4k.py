import newspaper

# # URL статьи
# url = 'https://www.protothema.gr/greece/article/1541490/thessaloniki-sti-fulaki-50hronos-me-adunamia-sta-smartwatches-eklepse-duo-fores-apo-to-idio-katastima/'

# # Создаем объект статьи
# article = newspaper.Article(url)

# # Загружаем и парсим статью
# article.download()
# article.parse()

# # Выводим заголовок и текст статьи
# print("Заголовок:", article.title)
# print("Текст статьи:", article.text)


url = "https://www.documentonews.gr/article/gallia-perase-apo-tin-ethnosyneleysi-i-protasi-momfis-kata-toy-makron"
article = newspaper.Article(url)
article.download()
article.parse()
print("Заголовок 1:", article.title)
print("Текст статьи:", article.text)
print("----------------------------------")


url = "https://www.kathimerini.gr/politics/amyna/563224714/ti-einai-ta-periferomena-pyromachika-poy-agorazei-i-ellada-oi-dynatotites-poy-xekleidonoyn/"
article = newspaper.Article(url)
article.download()
article.parse()
print("Заголовок 2:", article.title)
print("Текст статьи:", article.text)
print("----------------------------------")

url = "https://www.news247.gr/politiki/siriza-provlimatizei-tin-p-g-to-endexomeno-ekfilismou-tis-proedrikis-eklogis/"
article = newspaper.Article(url)
article.download()
article.parse()
print("Заголовок 3:", article.title)
print("Текст статьи:", article.text)
print("----------------------------------")


url = "https://www.efsyn.gr/kosmos/mesi-anatoli/446744_ekatontades-meli-tis-hezmpolah-traymatistikan-apo-ekrixi-ton-bombiton"
article = newspaper.Article(url)
article.download()
article.parse()
print("Заголовок 4:", article.title)
print("Текст статьи:", article.text)
print("----------------------------------")


url = "https://www.in.gr/2024/09/17/sports/on-field/o-alan-sirer-apotheose-ti-notigxam-tesseris-paiktes-tis-forest-stin-idaniki-entekada-tis-agonistikis-stin-premier/"
article = newspaper.Article(url)
article.download()
article.parse()
print("Заголовок 5:", article.title)
print("Текст статьи:", article.text)
print("----------------------------------")


url = "https://www.capital.gr/diethni/3869169/o-mario-ntragki-sto-ek-i-europi-prepei-na-dialexei-metaxu-dialusis-paralusis-i-oloklirosis/"
article = newspaper.Article(url)
article.download()
article.parse()
print("Заголовок 6:", article.title)
print("Текст статьи:", article.text)
print("----------------------------------")


url = "https://www.iefimerida.gr/kosmos/kataheirokrotithike-zizel-peliko-dikastirio"
article = newspaper.Article(url)
article.download()
article.parse()
print("Заголовок 7:", article.title)
print("Текст статьи:", article.text)
print("----------------------------------")


url = "https://www.lifo.gr/now/greece/fotia-stis-egkatastaseis-tis-motor-oil-ihise-112"
article = newspaper.Article(url)
article.download()
article.parse()
print("Заголовок 8:", article.title)
print("Текст статьи:", article.text)
print("----------------------------------")
