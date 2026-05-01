import pandas as pd
import json
import re

# Dosyaları yükle
df1 = pd.read_csv('/Users/sumeyyegultekin/Desktop/COURSE/CENG 493/Proje/Data prepration/CSV/hukuk_verisi.csv')
df2 = pd.read_csv('/Users/sumeyyegultekin/Desktop/COURSE/CENG 493/Proje/Data prepration/CSV/turkish_law_dataset.csv')

df = pd.concat([df1, df2]).drop_duplicates(subset=['soru', 'cevap'])
df = df.dropna(subset=['soru', 'cevap'])

df['soru'] = df['soru'].str.strip()
df['cevap'] = df['cevap'].str.strip()


def madde_formatla(metin):
    if not isinstance(metin, str):
        return None
        
    pattern = r'Madde\s*(\d+)|(\d+)\s*\.?\s*Madde|madde\s*(\d+)|(\d+)\s*\.?\s*madde'
    matches = re.findall(pattern, metin, flags=re.IGNORECASE)
    
    sonuclar = []
    for m in matches:
        # Hangi grup dolduysa o rakamı al
        rakam = m[0] if m[0] else m[1]
        if rakam: 
            sonuclar.append(f"{rakam}. Madde")
    
    unique_matches = list(set(sonuclar))
    
    try:
        unique_matches.sort(key=lambda x: int(re.search(r'\d+', x).group()))
    except (ValueError, AttributeError):
        unique_matches.sort() # Hata olursa düz string sıralaması yap
        
    return ", ".join(unique_matches) if unique_matches else None

rag_list = []

for index, row in df.iterrows():
    m_soru = madde_formatla(row['soru'])
    m_cevap = madde_formatla(row['cevap'])
    
    set_birlesik = set()
    for kaynak in [m_soru, m_cevap]:
        if kaynak is not None:
            set_birlesik.update([item.strip() for item in kaynak.split(',')])
    
    final_list = list(set_birlesik)
    try:
        final_list.sort(key=lambda x: int(re.search(r'\d+', x).group()))
    except:
        final_list.sort()

    metadata_val = ", ".join(final_list) if final_list else None

    veri_objesi = {
        "index": f"row_{index}",
        "question": row['soru'],
        "answer": row['cevap'],
        "metadata": {
            "madde": metadata_val
        }
    }
    rag_list.append(veri_objesi)

# Kaydet
with open('data.jsonl', 'w', encoding='utf-8') as f:
    json.dump(rag_list, f, ensure_ascii=False, indent=4)