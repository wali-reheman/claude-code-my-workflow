---
paths:
  - "master_supporting_docs/**"
  - "Replication/data/raw/**"
---

# Robust PDF Processing Best Practices

## Why PDFs Can Break the Code
Large PDFs (>50 pages or >20MB) can cause:
- Memory overflow errors
- Token limit exceeded errors
- Timeout failures during processing
- Incomplete or corrupted text extraction
- Session crashes requiring restart

## Where PDFs Live

| Location | Typical Content | Who Puts Them There |
|----------|----------------|-------------------|
| `master_supporting_docs/supporting_papers/` | Academic papers for lecture/slide development | User uploads |
| `master_supporting_docs/supporting_slides/` | Existing slide decks to upgrade | User uploads |
| `Replication/data/raw/` | Dataset codebooks, data dictionaries, survey instruments | User downloads from data providers |

**All locations follow the same safe processing protocol below.**

## The Safe Processing Workflow

**Step 1: Receive PDF**
- User places PDF in one of the locations above
- Claude DOES NOT attempt to read it directly

**Step 2: Check PDF Properties**
```bash
pdfinfo paper_name.pdf | grep "Pages:"
ls -lh paper_name.pdf
```

**Step 3: Create Subfolder and Split**
```bash
mkdir -p paper_name/

for i in {0..9}; do
  start=$((i*5 + 1))
  end=$(((i+1)*5))
  gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
     -dFirstPage=$start -dLastPage=$end \
     -sOutputFile="paper_name/paper_name_p$(printf '%03d' $start)-$(printf '%03d' $end).pdf" \
     paper_name.pdf 2>/dev/null
done
```

**Step 4: Process Chunks Intelligently**
- Read chunks ONE AT A TIME using the Read tool
- Extract key information from each chunk
- Build understanding progressively
- Don't try to hold all chunks in working memory

**Step 5: Selective Deep Reading**
- After scanning all chunks, identify the most relevant sections
- Only read those sections in detail for slide development
- Skip appendices, references, or less relevant sections unless needed

## Error Handling Protocol

**If a chunk fails to process:**
1. Note the problematic chunk (e.g., "Chunk p021-025 failed")
2. Try splitting it into even smaller pieces (1-2 pages each)
3. If still failing, skip it and document the gap
4. Continue with other chunks

**If splitting fails:**
1. Check if Ghostscript is installed: `gs --version`
2. Try alternative: `pdftk paper.pdf burst output paper_%03d.pdf`
3. If all else fails, ask user to upload specific page ranges manually

**If memory/token issues persist:**
1. Process only 2-3 chunks per session
2. Use Task tool with Explore agent for large-scale scanning
3. Focus on specific sections user identifies as most important

## Codebook and Data Dictionary PDFs

Dataset codebooks (V-Dem, Polity, Afrobarometer, etc.) are often 100-500+ pages. They require special handling:

**Priority sections to extract:**
1. **Variable definitions** — names, descriptions, coding schemes, value labels
2. **Country/unit coverage** — which countries/years are included
3. **Missing data codes** — what values represent missing, refused, don't know
4. **Sampling methodology** — for survey data (weights, stratification)
5. **Version/changelog** — what changed between data releases

**Strategy:** Don't read the entire codebook. After splitting:
1. Scan the table of contents chunk (usually pages 1-5)
2. Jump directly to the variable definitions section
3. Read only the variables the user needs for their analysis
4. Save extracted variable definitions to `data/codebook.md` as you go

**Common codebook locations to document in `data/codebook.md`:**
```
V-Dem Codebook: Replication/data/raw/vdem_codebook_v14.pdf (pp. 30-180 for variable defs)
Polity5 Manual: Replication/data/raw/polity5_manual.pdf (pp. 14-18 for component vars)
WDI Metadata: accessed via WDI() R package — no PDF needed
```

---

## Performance Optimization

**For very large PDFs (>100 pages):**
- Split into 3-page chunks instead of 5-page
- Process only introduction, conclusion, and key sections initially
- Ask user which sections matter most for slide development

**For slide PDFs:**
- Beamer/LaTeX slides often have 1 idea per page - 10-page chunks acceptable
- PowerPoint exports might be image-heavy - stick to 5-page chunks
- Check file size per chunk, not just page count

**For papers with many figures:**
- Figures increase PDF file size dramatically
- A 5-page chunk might be 15MB if figure-heavy
- Split figure-heavy sections into 2-3 page chunks

## Quick Reference: PDF Processing Commands

```bash
# Check PDF info
pdfinfo filename.pdf

# Count pages
pdfinfo filename.pdf | grep "Pages:" | awk '{print $2}'

# Split with Ghostscript (5-page chunks)
for i in {0..XX}; do
  start=$((i*5 + 1))
  end=$(((i+1)*5))
  gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
     -dFirstPage=$start -dLastPage=$end \
     -sOutputFile="folder/name_p$(printf '%03d' $start)-$(printf '%03d' $end).pdf" \
     filename.pdf
done

# Alternative: pdftk (if available)
pdftk filename.pdf burst output folder/name_p%03d.pdf

# Check chunk file sizes
ls -lh folder/*.pdf
```

## When to Ask User for Help

Claude should ask the user to:
1. **Prioritize sections** - "This is a 200-page PDF. Which sections matter most?"
2. **Provide page ranges** - "Could you identify the key pages covering [topic]?"
3. **Upload subsections** - "If possible, could you export just the relevant chapter?"
4. **Clarify focus** - "Should I focus on the theoretical framework or empirical results?"
