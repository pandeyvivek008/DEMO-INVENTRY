# 2 लाख products और high traffic deployment

यह document उस production setup के लिए है जिसमें बहुत users एक समय पर app इस्तेमाल करें। केवल ZIP को Railway पर deploy कर देना पर्याप्त नहीं है: database, image storage, Redis और index worker भी लगाना होगा।

## Required services

| काम | Production service |
| --- | --- |
| Inventory, users, catalog | PostgreSQL |
| 2 लाख product image matching | PostgreSQL `pgvector` HNSW index |
| Shared scan cache / rate limit | Redis |
| Original product photos | S3, Cloudflare R2, Cloudinary, या persistent volume |
| API traffic | 2+ web instances behind Railway/Render/load balancer |
| Heavy index creation | अलग one-off/background worker |

## Deploy order

1. Managed PostgreSQL और Redis बनाइए। PostgreSQL user को `CREATE EXTENSION vector` की permission होनी चाहिए।
2. App service Variables में `DATABASE_URL`, `REDIS_URL`, `WEB_CONCURRENCY=2`, `DB_POOL_SIZE=10`, `DB_MAX_OVERFLOW=10` रखें। Database plan छोटा हो तो workers × (pool + overflow) database max connections से कम रखें।
3. Product images के लिए persistent storage लगाइए। Local `backend/static/product_images` only demo/single-instance mode है।
4. App deploy करें। पहले bulk catalog/data import करें और photos upload करें।
5. एक worker/job में चलाएँ: `cd backend && python scripts/rebuild_visual_index.py`। यह हर photo को vector में बदलकर HNSW index में रखता है। इसे web request में न चलाएँ।
6. `/api/products/visual-match` से sample scans चलाकर top results verify करें। फिर second web instance scale करें। Redis cache और PostgreSQL index दोनों instances share करेंगे।

## Safety and load controls included

- Scan endpoint per client per minute rate-limited है (`VISUAL_SEARCH_RPM`, default 30)। Redis होने पर limit every web instance में shared रहती है।
- Same photo का result 60 seconds Redis cache में रहता है; stock details हर response में database से fresh आती हैं।
- PostgreSQL connection pool bounded और pre-pinged है, इसलिए traffic spike में uncontrolled connections नहीं खुलते।
- Production search HNSW vector query करती है; entire catalog image files read नहीं करती। Index missing हो तो request fail-safe तरीके से return होती है।
- Scan read-only है; correct design confirmation और stock adjustment का existing audit flow अलग रहता है।

## Accuracy

Current vector colour + visual shape based है और clean catalog photos के लिए economical baseline देता है। Similar patterns/colours को “perfect” तरीके से अलग करने के लिए next stage में fashion-tuned CLIP embeddings, multiple photos per colour/design, and real warehouse scan photos चाहिए। 200k products पर production rollout से पहले 500–1000 labelled scans पर Top-1 / Top-5 accuracy measure करें और human confirmation रखें।
