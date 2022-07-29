# %%
import pandas as pd
from ethnicolr import census_ln, pred_census_ln
 
names = [{'name': 'Last Name'}, {'name': 'Brager'}, {'name': 'Kersten'}, {'name': 'Arratia'}, {'name': 'Leonard'}, {'name': 'Soltys'}, {'name': 'Liles'}, {'name': 'Raigoza'}, {'name': 'Sato'}, {'name': 'Ott'}, {'name': 'Sandoval'}, {'name': 'Brinkley'}, {'name': 'Hernes'}, {'name': 'Achmon'}, {'name': 'LeGrand'}, {'name': 'Still'}, {'name': 'Vieira'}, {'name': 'Cid'}, {'name': 'Mukherjea'}, {'name': 'Ingraham'}, {'name': 'Smith'}, {'name': 'Castronovo'}, {'name': 'Helgren'}, {'name': 'Reece'}, {'name': 'Lent'}, {'name': 'Nation'}, {'name': 'Shahrestani'}, {'name': 'Rasche'}, {'name': 'Crawford'}, {'name': 'Soong'}, {'name': 'Johnson'}, {'name': 'Daughrity'}, {'name': 'Weng'}, {'name': 'Gray'}, {'name': 'Cotter'}, {'name': 'Lovato'}, {'name': 'Nourazari'}, {'name': 'Zavala'}, {'name': 'Shaffer'}, {'name': 'Martinez'}, {'name': 'Li'}, {'name': 'Grammer'}, {'name': 'Valenzuela'}, {'name': 'Nicholas'}, {'name': 'Seibt'}, {'name': 'Gipson'}, {'name': 'Goodman-Meza'}, {'name': 'Sammler'}, {'name': 'Shackman'}, {'name': 'DAVILA'}, {'name': 'Berhe'}, {'name': 'Ghezzehei'}, {'name': 'Canner'}, {'name': 'Ho'}, {'name': 'Brundage'}, {'name': 'Palomo'}, {'name': 'Wu'}, {'name': 'Bhandari'}, {'name': 'Dong'}, {'name': 'Ying'}, {'name': 'Woodard'}, {'name': 'Shaheen'}, {'name': 'Coil'}, {'name': 'Sevelius'}, {'name': 'Lam'}, {'name': 'Matharu'}, {'name': 'Peterson'}, {'name': 'Schlemer'}, {'name': 'Becket'}, {'name': 'Kim'}, {'name': 'Hodges'}, {'name': 'Zhang'}, {'name': 'Jones'}, {'name': 'Wiberg'}, {'name': 'Jaffe'}, {'name': 'McNally'}, {'name': 'Streubel'}]
 
df = pd.DataFrame(names)
 
#df
 
#census_ln(df, 'name') #.to_csv("./ethnicolr_results.csv")
#pred = pred_census_ln(df, 'name')
 
#from ethnicolr import pred_wiki_ln, pred_wiki_name
#odf = pred_wiki_ln(df,'last')
 
 
# %%
pred = pred_census_ln(df, 'name')
#pred[['name', 'api_mean', 'black_mean', 'hispanic_mean', 'white_mean', 'race']].to_csv("ethnicolr_predcensus.csv")
 
# %%
pred.to_csv("78_pred_census_ln.csv")
 
# %%
pred = census_ln(df, 'name')
 
# %%
pred.to_csv("ethnicolr_function_census_ln.csv")
 
# %%
from ethnicolr import pred_wiki_ln, pred_wiki_name
 
# %%
fullNames = [{'last': 'Li', 'first': 'Yize'}, {'last': 'Lei', 'first': 'Chengwei'}, {'last': 'Zeng', 'first': 'Bilin'}, {'last': 'Fuchs', 'first': 'Alan'}, {'last': 'Gove', 'first': 'David'}, {'last': 'Prasai', 'first': 'Krishna'}, {'last': 'Gehlbach', 'first': 'Hunter'}, {'last': 'Remais', 'first': 'Justin'}, {'last': 'Brager', 'first': 'Gail'}, {'last': 'Lee', 'first': 'Yoonjung'}, {'last': 'Mu', 'first': 'Changhua'}, {'last': 'Eichelmann', 'first': 'Elke'}, {'last': 'Kersten', 'first': 'Ellen'}, {'last': 'Arratia', 'first': 'Miguel'}, {'last': 'Kiran', 'first': 'Mariam'}, {'last': 'Leonard', 'first': 'Kathryn'}, {'last': 'Baker', 'first': 'Dana Lee'}, {'last': 'Soltys', 'first': 'Michael'}, {'last': 'Liles', 'first': 'Garrett'}, {'last': 'Raigoza', 'first': 'Jaime'}, {'last': 'Sato', 'first': 'Noriyuki'}, {'last': 'Ott', 'first': 'Lisa'}, {'last': 'Rosenthal', 'first': 'Jennifer'}, {'last': 'Sandoval', 'first': 'Samuel'}, {'last': 'Brinkley', 'first': 'Catherine'}, {'last': 'Hernes', 'first': 'Peter'}, {'last': 'Qing Ge', 'first': 'Moyar'}, {'last': 'Kumar Jena', 'first': 'Prasant'}, {'last': 'Achmon', 'first': 'Ygal'}, {'last': 'de Lange', 'first': 'Elvira'}, {'last': 'Reynolds', 'first': 'Pamela'}, {'last': 'Kagawa', 'first': 'Rose'}, {'last': 'LeGrand', 'first': 'Karen'}, {'last': 'Still', 'first': 'Patrick'}, {'last': 'Tang', 'first': 'Bin'}, {'last': 'Vieira', 'first': 'Philip'}, {'last': 'Kram', 'first': 'Karin'}, {'last': 'Theiss', 'first': 'Kathryn'}, {'last': 'Lacy', 'first': 'Sarah'}, {'last': 'Cid', 'first': 'Ximena'}, {'last': 'McGlynn', 'first': 'Terry'}, {'last': 'Srinivasan', 'first': 'Chandra'}, {'last': 'Chatterjee', 'first': 'Ayona'}, {'last': 'Khosla', 'first': 'Nidhi'}, {'last': 'Mukherjea', 'first': 'Arnab'}, {'last': 'Ingraham', 'first': 'Natalie'}, {'last': 'Grimm', 'first': 'Kathryn'}, {'last': 'Smith', 'first': 'Ryan'}, {'last': 'Castronovo', 'first': 'Fadi'}, {'last': 'Murray', 'first': 'James'}, {'last': 'Helgren', 'first': 'Erik'}, {'last': 'Ertaul', 'first': 'Levent'}, {'last': 'Chung', 'first': 'Steve'}, {'last': 'Reece', 'first': 'Joshua'}, {'last': 'Cecotti', 'first': 'Hubert'}, {'last': 'Juarez', 'first': 'Chelsey'}, {'last': 'Brooks', 'first': 'Cory'}, {'last': 'Lent', 'first': 'David'}, {'last': 'Ho', 'first': 'Pei-Chun'}, {'last': 'Nation', 'first': 'Austin'}, {'last': 'Lee', 'first': 'Alice'}, {'last': 'Jimenez', 'first': 'Veronica'}, {'last': 'Ramirez', 'first': 'Maria Soledad'}, {'last': 'Shahrestani', 'first': 'Parvin'}, {'last': 'Todorova', 'first': 'Gergana'}, {'last': 'Nikolaidis', 'first': 'Nikolas'}, {'last': 'Rasche', 'first': 'Madeline'}, {'last': 'LEE', 'first': 'CHARLES'}, {'last': 'Rendon', 'first': 'Maria'}, {'last': 'Crawford', 'first': 'Heather'}, {'last': 'Soong', 'first': 'Jennifer'}, {'last': 'Deng', 'first': 'Hang'}, {'last': 'Johnson', 'first': 'Amber'}, {'last': 'Daughrity', 'first': 'Belinda'}, {'last': 'Asvapathanagul', 'first': 'Pitiporn'}, {'last': 'Weng', 'first': 'Suzie'}, {'last': 'Pace', 'first': 'Douglas'}, {'last': 'Gray', 'first': 'Virginia'}, {'last': 'Cotter', 'first': 'Joshua'}, {'last': 'Lovato', 'first': 'Kristina'}, {'last': 'Nourazari', 'first': 'Sara'}, {'last': 'Halim', 'first': 'May Ling'}, {'last': 'Zavala', 'first': 'Arturo'}, {'last': 'Shaffer', 'first': 'Gwen'}, {'last': 'Laris', 'first': 'Paul'}, {'last': 'Martinez', 'first': 'Iveris'}, {'last': 'Li', 'first': 'Jingjing'}, {'last': 'He', 'first': 'Ximin'}, {'last': 'Grammer', 'first': 'Jennie'}, {'last': 'Valenzuela', 'first': 'Nicole'}, {'last': 'Nicholas', 'first': 'Susanne'}, {'last': 'Seibt', 'first': 'Ulrike'}, {'last': 'Wirz', 'first': 'Richard'}, {'last': 'Gipson', 'first': 'Jessica'}, {'last': 'Cusack', 'first': 'Daniela'}, {'last': 'Woo', 'first': 'Shih Lung'}, {'last': 'BAE', 'first': 'SONGYI'}, {'last': 'Halec', 'first': 'Gordana'}, {'last': 'Martin', 'first': 'Raleigh'}, {'last': 'Goodman-Meza', 'first': 'David'}, {'last': 'Sammler', 'first': 'Katherine'}, {'last': 'Shackman', 'first': 'Joshua'}, {'last': 'Alegria', 'first': 'Sharla'}, {'last': 'Pirtle', 'first': 'Whitney'}, {'last': 'Wang', 'first': 'Yue (Jessica)'}, {'last': 'Moran', 'first': 'Emily'}, {'last': 'Magana', 'first': 'Dalia'}, {'last': 'DAVILA', 'first': 'LILIAN'}, {'last': 'McTavish', 'first': 'Emily Jane'}, {'last': 'Berhe', 'first': 'Asmeret Asefaw'}, {'last': 'Ghezzehei', 'first': 'Teamrat'}, {'last': 'Hull', 'first': 'Kathleen'}, {'last': 'Tsoulouhas', 'first': 'Theofanis "Fanis"'}, {'last': 'Leal-Quiros', 'first': 'Edbertho'}, {'last': 'Sandoval', 'first': 'Jesus'}, {'last': 'Chittamuru', 'first': 'Deepti'}, {'last': 'Ruiz', 'first': 'Dannise'}, {'last': 'Grobman', 'first': 'Kevin'}, {'last': 'Canner', 'first': 'Judith'}, {'last': 'Jia', 'first': 'Ruting'}, {'last': 'Banerjee', 'first': 'Meeta'}, {'last': 'Nickols', 'first': 'Kerry'}, {'last': 'Ho', 'first': 'Nhut'}, {'last': 'In Huh', 'first': 'Kyung'}, {'last': 'Olive Li', 'first': 'Yao'}, {'last': 'Brundage', 'first': 'Cord'}, {'last': 'Palomo', 'first': 'Monica'}, {'last': 'Wu', 'first': 'Lin'}, {'last': 'Bhandari', 'first': 'Subodh'}, {'last': 'Dong', 'first': 'Winny'}, {'last': 'Moradi Nargesi', 'first': 'Mahnaz'}, {'last': 'Sasser', 'first': 'Jade'}, {'last': 'Ying', 'first': 'Samantha'}, {'last': 'Li', 'first': 'Chen'}, {'last': 'Bik', 'first': 'Holly'}, {'last': 'Woodard', 'first': 'Sarah'}, {'last': 'Curras-Collazo', 'first': 'Margarita'}, {'last': 'McTernan', 'first': 'Melissa'}, {'last': 'Bahlman', 'first': 'Joseph'}, {'last': 'Markovic', 'first': 'Milica'}, {'last': 'Callori', 'first': 'Sara'}, {'last': 'Goforth', 'first': 'Brett'}, {'last': 'Garcia', 'first': 'Donna'}, {'last': 'Kinoshita', 'first': 'Alicia'}, {'last': 'Xu', 'first': 'Wenwu'}, {'last': 'Liu', 'first': 'Xiaofeng'}, {'last': 'Ghanipoor Machiani', 'first': 'Sahar'}, {'last': 'Forsberg', 'first': 'Erica'}, {'last': 'Maloney', 'first': 'Jillian'}, {'last': 'Schiaffino', 'first': 'Melody K'}, {'last': 'Herrera Villarreal', 'first': 'Felisha'}, {'last': 'Li', 'first': 'Yawen'}, {'last': 'Finlayson', 'first': 'Tracy'}, {'last': 'Oren', 'first': 'Eyal'}, {'last': 'Corliss', 'first': 'Heather'}, {'last': 'Bumah', 'first': 'Violet'}, {'last': 'Klotsko', 'first': 'Shannon Klotsko'}, {'last': 'Ng', 'first': 'Tse Nga Tina'}, {'last': 'Shaheen', 'first': 'Robina'}, {'last': 'Coil', 'first': 'AlisonC'}, {'last': 'Evdokimenko', 'first': 'Ekaterina'}, {'last': 'Johnson', 'first': 'Andrew'}, {'last': 'Sabouri', 'first': 'Somayeh'}, {'last': 'Rogers', 'first': 'Stephanie'}, {'last': 'Torres', 'first': 'Stacy'}, {'last': 'Sevelius', 'first': 'Jae'}, {'last': 'Apollonio', 'first': 'Dorie'}, {'last': 'Lam', 'first': 'Juleen'}, {'last': 'Buckwalter', 'first': 'James'}, {'last': 'Yabut', 'first': 'Odessa'}, {'last': 'Markossian', 'first': 'Sarine'}, {'last': 'Galan', 'first': 'Timothy'}, {'last': 'Matharu', 'first': 'Navneet'}, {'last': 'Bennion', 'first': 'Kelly'}, {'last': 'MAHADEV', 'first': 'STHANU'}, {'last': 'Peterson', 'first': 'Jean'}, {'last': 'Ringer McDonald', 'first': 'Ashley'}, {'last': 'Kang', 'first': 'Ike'}, {'last': 'Schlemer', 'first': 'Lizabeth'}, {'last': 'Niku', 'first': 'Saeed'}, {'last': 'Becket', 'first': 'Elinne'}, {'last': 'Iafe', 'first': 'Robert'}, {'last': 'Tsui', 'first': 'Stephen'}, {'last': 'Eilon', 'first': 'Zachary'}, {'last': 'Lowndes', 'first': 'Julia'}, {'last': 'Kappel', 'first': 'Carrie'}, {'last': 'Nava', 'first': 'Michael'}, {'last': 'Mi', 'first': 'Jane'}, {'last': 'Narayan', 'first': 'Siddharth'}, {'last': 'Kim', 'first': 'Anna'}, {'last': 'Hodges', 'first': 'Heather'}, {'last': 'Mobberley', 'first': 'Jennifer'}, {'last': 'Zhang', 'first': 'Yu'}, {'last': 'Zimmer', 'first': 'Margaret'}, {'last': 'Jones', 'first': 'Kevin'}, {'last': 'Kay', 'first': 'Kathleen'}, {'last': 'Sanfelice', 'first': 'Ricardo'}, {'last': 'Wiberg', 'first': 'Donald'}, {'last': 'Garcia-Luna-Aceves', 'first': 'JJ'}, {'last': 'Viola Eitzel Solera', 'first': 'Melissa'}, {'last': 'Jaffe', 'first': 'Karin'}, {'last': 'DIAZ-GARAYUA', 'first': 'JOSE'}, {'last': 'To', 'first': 'Wing'}, {'last': 'McNally', 'first': 'Alison'}, {'last': 'Ruiz', 'first': 'Iris'}, {'last': 'Kohler', 'first': 'Christian'}, {'last': 'Wainwright', 'first': 'Haruko'}, {'last': 'Feldman', 'first': 'Daniel'}, {'last': 'Karaoz', 'first': 'Ulas'}, {'last': 'Streubel', 'first': 'Robert'}, {'last': 'Tas Baas', 'first': 'Neslihan'}, {'last': 'Mortimer', 'first': 'Jenny'}, {'last': 'Bolshakova', 'first': 'Virginia'}, ]
df1 = pd.DataFrame(fullNames)
 
# %%
pred1 = pred_wiki_name(df1, 'first', 'last')
 
 
# %%
pred1
 
# %%
pred1.to_csv("ethnicolr_function_pred_wiki_name.csv")
 
# %%
pred1 = pred_wiki_ln(df1, 'last')
 
# %%
pred1
 
# %%
pred1.to_csv("ethnicolr_function_pred_wiki_ln.csv")
 
# %%
#pred1.columns
#pred1.to_csv("ethnicolr_wikiname.csv")
pred1[['__name', 'Asian,GreaterEastAsian,EastAsian_mean', 'Asian,GreaterEastAsian,Japanese_mean', 'Asian,IndianSubContinent_mean', 'GreaterAfrican,Africans_mean', 'GreaterAfrican,Muslim_mean', 'GreaterEuropean,British_mean', 'GreaterEuropean,EastEuropean_mean', 'GreaterEuropean,Jewish_mean', 'GreaterEuropean,WestEuropean,French_mean', 'GreaterEuropean,WestEuropean,Germanic_mean', 'GreaterEuropean,WestEuropean,Hispanic_mean', 'GreaterEuropean,WestEuropean,Italian_mean', 'GreaterEuropean,WestEuropean,Nordic_mean', 'race']].to_csv("ethnicolr_wikiname_.csv")
 
# %%
from ethnicolr import pred_fl_reg_ln_five_cat, pred_fl_reg_name
 
# %%
pred2 = pred_fl_reg_name(df1, 'first', 'last')
#pred2.to_csv("ethnicolr_fl.csv")
 
 
# %%
pred2.to_csv("ethnicolr_function_pred_fl_reg_name.csv")
 
# %%
norm_names = [{'first': 'Yize', 'last': 'Li'}, {'first': 'Chengwei', 'last': 'Lei'}, {'first': 'Bilin', 'last': 'Zeng'}, {'first': 'Alan', 'last': 'Fuchs'}, {'first': 'David', 'last': 'Gove'}, {'first': 'Krishna', 'last': 'Prasai'}, {'first': 'Hunter', 'last': 'Gehlbach'}, {'first': 'Justin', 'last': 'Remais'}, {'first': 'Gail', 'last': 'Brager'}, {'first': 'Yoonjung', 'last': 'Lee'}, {'first': 'Changhua', 'last': 'Mu'}, {'first': 'Elke', 'last': 'Eichelmann'}, {'first': 'Ellen', 'last': 'Kersten'}, {'first': 'Miguel', 'last': 'Arratia'}, {'first': 'Mariam', 'last': 'Kiran'}, {'first': 'Kathryn', 'last': 'Leonard'}, {'first': 'Dana Lee', 'last': 'Baker'}, {'first': 'Michael', 'last': 'Soltys'}, {'first': 'Garrett', 'last': 'Liles'}, {'first': 'Jaime', 'last': 'Raigoza'}, {'first': 'Noriyuki', 'last': 'Sato'}, {'first': 'Lisa', 'last': 'Ott'}, {'first': 'Jennifer', 'last': 'Rosenthal'}, {'first': 'Samuel', 'last': 'Sandoval'}, {'first': 'Catherine', 'last': 'Brinkley'}, {'first': 'Peter', 'last': 'Hernes'}, {'first': 'Moyar', 'last': 'Qing Ge'}, {'first': 'Prasant', 'last': 'Kumar Jena'}, {'first': 'Ygal', 'last': 'Achmon'}, {'first': 'Elvira', 'last': 'de Lange'}, {'first': 'Pamela', 'last': 'Reynolds'}, {'first': 'Rose', 'last': 'Kagawa'}, {'first': 'Karen', 'last': 'LeGrand'}, {'first': 'Patrick', 'last': 'Still'}, {'first': 'Bin', 'last': 'Tang'}, {'first': 'Philip', 'last': 'Vieira'}, {'first': 'Karin', 'last': 'Kram'}, {'first': 'Kathryn', 'last': 'Theiss'}, {'first': 'Sarah', 'last': 'Lacy'}, {'first': 'Ximena', 'last': 'Cid'}, {'first': 'Terry', 'last': 'McGlynn'}, {'first': 'Chandra', 'last': 'Srinivasan'}, {'first': 'Ayona', 'last': 'Chatterjee'}, {'first': 'Nidhi', 'last': 'Khosla'}, {'first': 'Arnab', 'last': 'Mukherjea'}, {'first': 'Natalie', 'last': 'Ingraham'}, {'first': 'Kathryn', 'last': 'Grimm'}, {'first': 'Ryan', 'last': 'Smith'}, {'first': 'Fadi', 'last': 'Castronovo'}, {'first': 'James', 'last': 'Murray'}, {'first': 'Erik', 'last': 'Helgren'}, {'first': 'Levent', 'last': 'Ertaul'}, {'first': 'Steve', 'last': 'Chung'}, {'first': 'Joshua', 'last': 'Reece'}, {'first': 'Hubert', 'last': 'Cecotti'}, {'first': 'Chelsey', 'last': 'Juarez'}, {'first': 'Cory', 'last': 'Brooks'}, {'first': 'David', 'last': 'Lent'}, {'first': 'Pei-Chun', 'last': 'Ho'}, {'first': 'Austin', 'last': 'Nation'}, {'first': 'Alice', 'last': 'Lee'}, {'first': 'Veronica', 'last': 'Jimenez'}, {'first': 'Maria Soledad', 'last': 'Ramirez'}, {'first': 'Parvin', 'last': 'Shahrestani'}, {'first': 'Gergana', 'last': 'Todorova'}, {'first': 'Nikolas', 'last': 'Nikolaidis'}, {'first': 'Madeline', 'last': 'Rasche'}, {'first': 'CHARLES', 'last': 'LEE'}, {'first': 'Maria', 'last': 'Rendon'}, {'first': 'Heather', 'last': 'Crawford'}, {'first': 'Jennifer', 'last': 'Soong'}, {'first': 'Hang', 'last': 'Deng'}, {'first': 'Amber', 'last': 'Johnson'}, {'first': 'Belinda', 'last': 'Daughrity'}, {'first': 'Pitiporn', 'last': 'Asvapathanagul'}, {'first': 'Suzie', 'last': 'Weng'}, {'first': 'Douglas', 'last': 'Pace'}, {'first': 'Virginia', 'last': 'Gray'}, {'first': 'Joshua', 'last': 'Cotter'}, {'first': 'Kristina', 'last': 'Lovato'}, {'first': 'Sara', 'last': 'Nourazari'}, {'first': 'May Ling', 'last': 'Halim'}, {'first': 'Arturo', 'last': 'Zavala'}, {'first': 'Gwen', 'last': 'Shaffer'}, {'first': 'Paul', 'last': 'Laris'}, {'first': 'Iveris', 'last': 'Martinez'}, {'first': 'Jingjing', 'last': 'Li'}, {'first': 'Ximin', 'last': 'He'}, {'first': 'Jennie', 'last': 'Grammer'}, {'first': 'Nicole', 'last': 'Valenzuela'}, {'first': 'Susanne', 'last': 'Nicholas'}, {'first': 'Ulrike', 'last': 'Seibt'}, {'first': 'Richard', 'last': 'Wirz'}, {'first': 'Jessica', 'last': 'Gipson'}, {'first': 'Daniela', 'last': 'Cusack'}, {'first': 'Shih Lung', 'last': 'Woo'}, {'first': 'SONGYI', 'last': 'BAE'}, {'first': 'Gordana', 'last': 'Halec'}, {'first': 'Raleigh', 'last': 'Martin'}, {'first': 'David', 'last': 'Goodman-Meza'}, {'first': 'Katherine', 'last': 'Sammler'}, {'first': 'Joshua', 'last': 'Shackman'}, {'first': 'Sharla', 'last': 'Alegria'}, {'first': 'Whitney', 'last': 'Pirtle'}, {'first': 'Yue (Jessica)', 'last': 'Wang'}, {'first': 'Emily', 'last': 'Moran'}, {'first': 'Dalia', 'last': 'Magana'}, {'first': 'LILIAN', 'last': 'DAVILA'}, {'first': 'Emily Jane', 'last': 'McTavish'}, {'first': 'Asmeret Asefaw', 'last': 'Berhe'}, {'first': 'Teamrat', 'last': 'Ghezzehei'}, {'first': 'Kathleen', 'last': 'Hull'}, {'first': 'Theofanis "Fanis"', 'last': 'Tsoulouhas'}, {'first': 'Edbertho', 'last': 'Leal-Quiros'}, {'first': 'Jesus', 'last': 'Sandoval'}, {'first': 'Deepti', 'last': 'Chittamuru'}, {'first': 'Dannise', 'last': 'Ruiz'}, {'first': 'Kevin', 'last': 'Grobman'}, {'first': 'Judith', 'last': 'Canner'}, {'first': 'Ruting', 'last': 'Jia'}, {'first': 'Meeta', 'last': 'Banerjee'}, {'first': 'Kerry', 'last': 'Nickols'}, {'first': 'Nhut', 'last': 'Ho'}, {'first': 'Kyung', 'last': 'In Huh'}, {'first': 'Yao', 'last': 'Olive Li'}, {'first': 'Cord', 'last': 'Brundage'}, {'first': 'Monica', 'last': 'Palomo'}, {'first': 'Lin', 'last': 'Wu'}, {'first': 'Subodh', 'last': 'Bhandari'}, {'first': 'Winny', 'last': 'Dong'}, {'first': 'Mahnaz', 'last': 'Moradi Nargesi'}, {'first': 'Jade', 'last': 'Sasser'}, {'first': 'Samantha', 'last': 'Ying'}, {'first': 'Chen', 'last': 'Li'}, {'first': 'Holly', 'last': 'Bik'}, {'first': 'Sarah', 'last': 'Woodard'}, {'first': 'Margarita', 'last': 'Curras-Collazo'}, {'first': 'Melissa', 'last': 'McTernan'}, {'first': 'Joseph', 'last': 'Bahlman'}, {'first': 'Milica', 'last': 'Markovic'}, {'first': 'Sara', 'last': 'Callori'}, {'first': 'Brett', 'last': 'Goforth'}, {'first': 'Donna', 'last': 'Garcia'}, {'first': 'Alicia', 'last': 'Kinoshita'}, {'first': 'Wenwu', 'last': 'Xu'}, {'first': 'Xiaofeng', 'last': 'Liu'}, {'first': 'Sahar', 'last': 'Ghanipoor Machiani'}, {'first': 'Erica', 'last': 'Forsberg'}, {'first': 'Jillian', 'last': 'Maloney'}, {'first': 'Melody K', 'last': 'Schiaffino'}, {'first': 'Felisha', 'last': 'Herrera Villarreal'}, {'first': 'Yawen', 'last': 'Li'}, {'first': 'Tracy', 'last': 'Finlayson'}, {'first': 'Eyal', 'last': 'Oren'}, {'first': 'Heather', 'last': 'Corliss'}, {'first': 'Violet', 'last': 'Bumah'}, {'first': 'Shannon Klotsko', 'last': 'Klotsko'}, {'first': 'Tse Nga Tina', 'last': 'Ng'}, {'first': 'Robina', 'last': 'Shaheen'}, {'first': 'AlisonC', 'last': 'Coil'}, {'first': 'Ekaterina', 'last': 'Evdokimenko'}, {'first': 'Andrew', 'last': 'Johnson'}, {'first': 'Somayeh', 'last': 'Sabouri'}, {'first': 'Stephanie', 'last': 'Rogers'}, {'first': 'Stacy', 'last': 'Torres'}, {'first': 'Jae', 'last': 'Sevelius'}, {'first': 'Dorie', 'last': 'Apollonio'}, {'first': 'Juleen', 'last': 'Lam'}, {'first': 'James', 'last': 'Buckwalter'}, {'first': 'Odessa', 'last': 'Yabut'}, {'first': 'Sarine', 'last': 'Markossian'}, {'first': 'Timothy', 'last': 'Galan'}, {'first': 'Navneet', 'last': 'Matharu'}, {'first': 'Kelly', 'last': 'Bennion'}, {'first': 'STHANU', 'last': 'MAHADEV'}, {'first': 'Jean', 'last': 'Peterson'}, {'first': 'Ashley', 'last': 'Ringer McDonald'}, {'first': 'Ike', 'last': 'Kang'}, {'first': 'Lizabeth', 'last': 'Schlemer'}, {'first': 'Saeed', 'last': 'Niku'}, {'first': 'Elinne', 'last': 'Becket'}, {'first': 'Robert', 'last': 'Iafe'}, {'first': 'Stephen', 'last': 'Tsui'}, {'first': 'Zachary', 'last': 'Eilon'}, {'first': 'Julia', 'last': 'Lowndes'}, {'first': 'Carrie', 'last': 'Kappel'}, {'first': 'Michael', 'last': 'Nava'}, {'first': 'Jane', 'last': 'Mi'}, {'first': 'Siddharth', 'last': 'Narayan'}, {'first': 'Anna', 'last': 'Kim'}, {'first': 'Heather', 'last': 'Hodges'}, {'first': 'Jennifer', 'last': 'Mobberley'}, {'first': 'Yu', 'last': 'Zhang'}, {'first': 'Margaret', 'last': 'Zimmer'}, {'first': 'Kevin', 'last': 'Jones'}, {'first': 'Kathleen', 'last': 'Kay'}, {'first': 'Ricardo', 'last': 'Sanfelice'}, {'first': 'Donald', 'last': 'Wiberg'}, {'first': 'JJ', 'last': 'Garcia-Luna-Aceves'}, {'first': 'Melissa', 'last': 'Viola Eitzel Solera'}, {'first': 'Karin', 'last': 'Jaffe'}, {'first': 'JOSE', 'last': 'DIAZ-GARAYUA'}, {'first': 'Wing', 'last': 'To'}, {'first': 'Alison', 'last': 'McNally'}, {'first': 'Iris', 'last': 'Ruiz'}, {'first': 'Christian', 'last': 'Kohler'}, {'first': 'Haruko', 'last': 'Wainwright'}, {'first': 'Daniel', 'last': 'Feldman'}, {'first': 'Ulas', 'last': 'Karaoz'}, {'first': 'Robert', 'last': 'Streubel'}, {'first': 'Neslihan', 'last': 'Tas Baas'}, {'first': 'Jenny', 'last': 'Mortimer'}, {'first': 'Virginia', 'last': 'Bolshakova'}]
df_norm = pd.DataFrame(norm_names)
 
# %%
pred_norm = pred_fl_reg_name(df_norm, 'first', 'last')
#pred_norm
 
# %%
pred_norm
 
# %%
pred_norm.to_csv("ethnicolr_function_pred_fl_reg_name.csv")
 
# %%
from ethnicolr import pred_fl_reg_ln_five_cat, pred_fl_reg_name_five_cat
 
# %%
pred_cat = pred_fl_reg_ln_five_cat(df_norm, 'last')
 
# %%
pred_cat.to_csv("ethnicolr_function_pred_fl_reg_ln_five_cat.csv")
 
# %%
pred_cat
 
# %%
pred_full_cat = pred_fl_reg_name_five_cat(df_norm, 'first', 'last')
 
# %%
pred_full_cat.to_csv("ethnicolr_function_pred_fl_reg_name_five_cat.csv")
 
 
 

