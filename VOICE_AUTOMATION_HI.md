# Disha voice automation

Disha को खोलें, browser में microphone **Allow** करें, फिर पहले **“Hi Disha”** या **“दिशा”** बोलें। इसके बाद नीचे की commands बोल सकते हैं। ये commands AI API call के बिना current app में तुरंत चलती हैं।

| बोलें | क्या होगा |
| --- | --- |
| “Dashboard kholo” | Dashboard खुलेगा |
| “Products kholo” | Product catalog खुलेगा |
| “Scanner kholo” | QR + Visual Product Scanner page खुलेगा |
| “Alerts dikhao” | Low/out-of-stock alerts खुलेंगे |
| “Reorder list kholo” | Reorder page खुलेगा |
| “Orders kholo” | Order processing page खुलेगा |
| “Bulk stock kholo” | Bulk stock count page खुलेगा |
| “History dikhao” | Stock change history खुलेगी |
| “Aaj ki sales” | आज की dispatched sales report बोलेगी और Dashboard खुलेगा |
| “App status batao” | Live inventory/alert summary बोलेगी |
| “Voice commands batao” | ऊपर वाली command list बोलेगी |

## Stock और order commands

पुरानी Disha commands भी काम करती हैं, जैसे:

- “Blue kurta M size ka stock batao”
- “SKU 123 M size mein 5 add karo”
- “SKU 123 ka stock 12 set karo”
- “Batch 14 dispatch karo”

Stock, product create/edit, delete/restore और order dispatch **पहले confirmation दिखाएँगे**। केवल “हाँ/confirm” बोलने या button दबाने के बाद ही database बदलेगा। यह गलती से voice सुन लेने पर stock/order बदलने से रोकता है।

## Camera limitation

“Scanner kholo” page खोल देता है। Browser security के कारण camera/microphone permission को पहली बार user को browser prompt/address-bar settings में Allow करना पड़ता है; website voice command उसे अपने-आप bypass नहीं कर सकती।
