# Efficiency Improvements for Document Analyzer and Summarizer

## Plan Overview
- Implement caching for OCR results to avoid reprocessing the same PDF (using file hash as key).
- Add parallel processing for OCR on multiple pages using `concurrent.futures`.
- Optimize image preprocessing if possible (e.g., adjust parameters for speed vs. accuracy).
- Ensure models are preloaded and not reloaded per request.
- Review and optimize regex patterns in extraction functions if inefficient.

## Steps to Complete

### 1. Review and Optimize Preprocessing (ai_engine/preprocess.py)
- [x] Read ai_engine/preprocess.py to understand current preprocessing steps.
- [x] Optimize parameters for speed vs. accuracy (e.g., adjust threshold values, reduce iterations if possible).

### 2. Add Caching and Parallel Processing to OCR (ai_engine/ocr.py)
- [x] Implement caching mechanism using file hash as key (e.g., use hashlib to generate hash).
- [x] Add parallel processing for OCR on multiple pages using concurrent.futures.
- [x] Modify extract_text_from_pdf to use caching and parallel OCR.

### 3. Integrate Caching in Engine (ai_engine/engine.py)
- [ ] Modify analyze_document to check cache before calling OCR.
- [ ] Store OCR results in cache after processing.

### 4. Ensure Models are Preloaded (ai_engine/classifier.py)
- [ ] Verify that models are loaded once at import time (already seems to be the case).
- [ ] If needed, add any optimizations to avoid reloading.

### 5. Review Extraction Functions for Optimization
- [ ] Read key extraction files (e.g., extract_deadline.py, extract_penalty.py, etc.) to check regex patterns.
- [ ] Optimize any inefficient regex or logic.

### 6. Testing and Followup
- [ ] Test changes with sample PDFs to measure performance improvement.
- [ ] Monitor for accuracy loss due to optimizations.
- [ ] If needed, consider faster OCR alternatives like EasyOCR.
