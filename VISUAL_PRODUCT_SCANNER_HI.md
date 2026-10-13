# Visual Product Scanner — इस्तेमाल करने का तरीका

यह सुविधा product की फोटो से catalog में सबसे मिलते-जुलते designs खोजती है। यह stock **कभी अपने-आप नहीं बदलती**; कर्मचारी को सही design confirm करना होता है।

## बड़े catalog और बहुत users के लिए production setup

2 लाख products या बहुत सारे simultaneous users के लिए SQLite/local-disk mode का उपयोग नहीं करें। इस build में production path भी शामिल है:

1. Railway/Render पर managed **PostgreSQL** लें और उसमें `pgvector` extension enable करें।
2. Managed **Redis** जोड़कर उसका `REDIS_URL` app Variables में रखें। यह repeated scan cache और सभी web instances पर shared rate-limit देता है।
3. Product images को persistent object storage (S3/R2/Cloudinary) या attached persistent volume में रखें—ephemeral Railway disk पर नहीं।
4. Images upload/import होने के बाद अलग worker में `cd backend && python scripts/rebuild_visual_index.py` चलाएँ। यह vector index background में बनाएगा; customers के scan request में कभी 2 लाख photos loop नहीं होंगी।
5. `WEB_CONCURRENCY`, `DB_POOL_SIZE` और `DB_MAX_OVERFLOW` को managed database connection limit के हिसाब से set करें। Load balancer के पीछे multiple identical web instances चलाए जा सकते हैं।

Production में scanner PostgreSQL HNSW nearest-neighbour vector index use करता है, इसलिए lookup indexed रहता है। अगर index empty/unavailable है तो endpoint safe 503 देता है; वह CPU पर पूरा 2 लाख-photo catalog scan नहीं करेगा।

इस code में lightweight `colour-shape-v1` vector default है। Similar embroidery/design के लिए production quality बढ़ाने हेतु dedicated fashion/CLIP embedding worker और multiple photos per design जोड़कर index rebuild करना होगा; केवल environment variable बदलना पर्याप्त नहीं है। हर case में Top matches + human confirmation रखना जरूरी है; कोई image system 100% guarantee नहीं दे सकता।

## रोज़ का workflow

1. **Products** में product बनाते समय SKU, नाम, रंग/category, size-wise stock और साफ़ product photo भरें।
2. **Scan & Recount** खोलें और नीचे **Visual Product Scanner** में `Open Camera` या `Upload Photo` चुनें।
3. एक ही कपड़ा, सीधे सामने से, अच्छे light में दिखाएँ और photo लें/चुनें।
4. App saved catalog photos के साथ तुलना कर के Top 5 closest matches दिखाती है। हर card में SKU, match percentage और प्रत्येक size का live stock दिखता है।
5. सही card पर **This is the correct design** दबाएँ। अब नीचे वही existing stock/recount panel खुलता है। जरूरत हो तभी वहाँ stock update करें।

## अच्छी पहचान के लिए catalog में क्या चाहिए

- हर design और हर colour की **अलग product entry और अलग clean photo** रखें।
- Photo में पूरा garment सामने से हो, plain background हो और बहुत shadow/reflection न हो।
- एक design के लिए ज्यादा angles चाहिए हों तो अभी main/front photo सबसे साफ रखें। भविष्य में multiple reference photos जोड़े जा सकते हैं।
- SKU स्थायी रखें; same design की sizes को उसी product के variants में रखें।

## Accuracy की सही अपेक्षा

यह local matching colour distribution और image shape/detail से compare करता है, इसलिए API key या हर scan का AI खर्च नहीं लगता। लेकिन very similar embroidery, same colour या different lighting में दो designs पास-पास आ सकते हैं। इसलिए app best match को automatic final answer नहीं मानती—Top 5 दिखाती है और manual confirmation जरूरी है।

जब catalog में बहुत सारे similar products हो जाएँ, अगला upgrade real product photos के साथ CLIP/fashion-embedding index और multiple reference photos per design होगा। इस version का catalog workflow उसी upgrade के लिए सही आधार बनाता है।

## Disha microphone

Disha का mic browser permission से चलता है। पहली बार Disha खोलकर mic दबाएँ और address-bar के site controls में **Microphone → Allow** चुनें। अगर headset लगा है तो Windows/phone में उसी headset microphone को input device बनाएं। Permission मिल जाने के बाद Disha continuous Hindi/English speech को server transcription endpoint तक भेजती है।
