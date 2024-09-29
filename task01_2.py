import re
from collections import defaultdict, Counter
from math import gcd
from functools import reduce

# Приклад шифротексту
ciphertext = "VYC PKHOJT XZ RJV AGXOZFR DM ZGRSIBTAC TWPLIJ. RD KSBVAA HPV RLS VCTTEPS RJV YGMWYK IH HPV'J YXF. HNV CGPRKT GH AS CYO RHL VIYCLZGKE XURQ RLDMVKI MPULGI MG T BKN MPACTZYA AWY ZMEYCUJGDG CL SEPBRKWSA MVOEGH. AFG YGVASYK, AH AFG CMLXGZ, WOGT MH TPXMWIZSB PQ C DMSX CL RUIVZKFEGTDNP. TWVQG NFD YWTU UVSW OVYCBBMJ IC ICCLRXYIR KHXUEU RPT VCXIUEA UKKFDNH HVICN AJRPBBBM. KHXZ GU R DPNZZ. KHDZC YYM UBBJ SEPBRKWSA FSGEICNQ KE ZTTIZZFJS RJZLVL OXV TWL AWCRXOOZVD. UVP VYCHX HNVRT PQ JFNT. MVKP AGL RJV CAXQZ KO LOMO SCPNHOWUA AFKEEH FSGE OCSW DVYJMM. ZYEGL GU EM HNQN KHXUE CJ Y BHFGC OG HL KDKDKOR SODR. ZQFIH TFK NEAS UTZRIXB, UI BPKJA NPXMHKE. TWHR KJ YAE. HNV NXUCVVCCMV-IVNIBPA UGHEWQV OU YCCCGHF WY KHT YYIV MU VORZBPU QGVGCZ VOJ OLU DCTC XG O MCAHZ. RJV LXGSZVECAF-EVLINFE UIHSGMV MU KCSRNIPAKJK XL HNV RPNC QW APEWHRN CVR UVCXGU NZS DDL HRAT BB G XLPZQ. VYC BHFGC LXMC QW KPG TUIMH WYTK MU MVK JUQQCEK KPMHKI OU AFG RPIBGZ, SUI AFG DMGTZOKY DM YTK ADGGOJTH PL VYC EXFLVCI BQG FD PG WSGEGMCEK KTWWAD. ND HPVZQI WSYZRTZ RQ GPDOS GEYIOGPX. CKXB ZYICNQ VYYI TFK KRJL ACE ZT IFUMES. UM CIRXLH NRS TAFKTYA LMSGAIOGGJ. YC XHNZCPS QADNPMVE ZN PU YTKGHM WY RN JUNCIBDGOHCE BHLPVPXLA UW SIFJG. EM PKHOJT XZ CXVP BHFHZD. IOC CIRXLH IRN TENTVQH XJKIYIOGPX. RWHIMYT PUB NRLVNOMV AGL RQ KFT TFZZSI PLUKPJFSTKS DM YP RPI. OWIV ACK TKIRJX OXV TD AFG RPIBGZ DAILPKRJH YCX RN PYR. HIMB MVK GOXUR QW TXXK UW FDYK, VYC IRDK FF PSJ VYC PKHY ZS IOC CIR DY HNV MJZGEZYC. YFUD TWL NQZLI HT BZEL VD HVCABBM, KHT HAVFP'H VFGWT XZ RJV RNIS. GCL PYR KJ YI HBIV SJYDCTC PGR YPMQVJ. VYMHX KNF GD ICPVYIA HNV SJYDCTC SH GU RT IOCKI NTKWR. KHDZC YYM GXOJ KHT ZWOSMA WC YF AI AFGZP EXFOC. II PQ VYC HISIKAIVP, CEB CHH RZFT, AFCK YGM FKRLAF KKIPDKG. JZVTYQKKW DY CVZNXVL CSMJM O CFRZ VD CIR HACCJ TWHR VYC LHFQ ZS CLU, EFKEESD, MIIHJ. YYCC VFOKIRZ BKJYVKSK KHT HPVZQI BG OE ARJMTU UXMV NZMHLJH. NC RTB LFRVPTG R KPG TUI MPRGPX Y JLSLLL IOGPX YH ECTX AH OC FFCH GCZ RDBPPG ZR. IAS UELN LVELQT YCX DAZPLI R SHXZKJS IOGPX GH MVGK OCL YFDGGXG OK ICACPJCAR. ORC AGA GU HSXMS AJEALQU"

# Шаг 1: Метод Касіскі для знаходження довжини ключа
def kasiski_test(ciphertext, min_sequence_length=3):
    """
    Метод Касіскі для оцінки довжини ключа на основі повторюваних послідовностей.
    """
    ciphertext = ''.join([char for char in ciphertext.upper() if char.isalpha()])
    sequences = defaultdict(list)

    # Знаходимо всі повторювані послідовності довжиною не менше min_sequence_length
    for i in range(len(ciphertext) - min_sequence_length + 1):
        seq = ciphertext[i:i + min_sequence_length]
        for j in range(i + min_sequence_length, len(ciphertext) - min_sequence_length + 1):
            if ciphertext[j:j + min_sequence_length] == seq:
                sequences[seq].append(j - i)

    # Збираємо всі відстані між повторюваними фрагментами
    distances = []
    for seq, positions in sequences.items():
        if len(positions) > 1:
            for i in range(len(positions) - 1):
                distances.append(positions[i + 1])

    # Використовуємо НСД для визначення ймовірної довжини ключа
    if len(distances) > 0:
        key_length = reduce(gcd, distances)
        return key_length
    else:
        return None

# Шаг 2: Частотний аналіз для визначення ключа
def frequency_analysis(segment):
    """
    Частотний аналіз для кожного стовпця з метою знаходження найбільш імовірного зсуву (літери ключа).
    """
    frequency_order = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'  # Частотний порядок літер англійської мови
    segment_frequencies = Counter(segment)
    most_common_letter = segment_frequencies.most_common(1)[0][0]
    
    # Знаходимо зсув між найбільш часто вживаною літерою у сегменті та 'E'
    shift = (ord(most_common_letter) - ord('E')) % 26
    return chr(shift + ord('A'))

# Шаг 3: Розбиття шифротексту на стовпці
def split_text_into_columns(ciphertext, key_length):
    """
    Розбиває текст на кілька стовпців на основі довжини ключа.
    """
    columns = ['' for _ in range(key_length)]
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            columns[i % key_length] += char
    return columns

# Шаг 4: Відновлення ключа
def find_key(ciphertext, key_length):
    """
    Відновлює ключ на основі частотного аналізу для кожного стовпця.
    """
    columns = split_text_into_columns(ciphertext, key_length)
    key = ''
    for column in columns:
        key += frequency_analysis(column)
    return key

# Шаг 5: Дешифрування тексту
def vigenere_decrypt(ciphertext, key):
    """
    Дешифрує текст за допомогою шифру Віженера на основі знайденого ключа.
    """
    key = key.upper()
    decrypted_text = []
    key_length = len(key)
    key_index = 0
    
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % key_length]) - ord('A')
            decrypted_char = chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A'))
            decrypted_text.append(decrypted_char)
            key_index += 1
        else:
            decrypted_text.append(char)  # Залишаємо неалфавітні символи без змін
    
    return ''.join(decrypted_text)


# Шаг 1: Застосовуємо метод Касіскі для визначення довжини ключа
key_length = kasiski_test(ciphertext)
print(f"Оцінена довжина ключа: {key_length}")

# Шаг 2: Знаходимо ключ за допомогою частотного аналізу
if key_length:
    key = find_key(ciphertext, key_length)
    print(f"Відновлений ключ: {key}")

    # Шаг 3: Дешифруємо шифротекст
    decrypted_text = vigenere_decrypt(ciphertext, key)
    print(f"Розшифрований текст: {decrypted_text}")
else:
    print("Не вдалося визначити довжину ключа.")
