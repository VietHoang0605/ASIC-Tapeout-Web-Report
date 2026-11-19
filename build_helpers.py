# -*- coding: utf-8 -*-
import os, re, json, glob, html as html_lib, textwrap
import markdown

base_dir = r"D:\Tapeout_chip"
web_dir = r"D:\Tapeout_chip\Web_Report"
output_js = os.path.join(web_dir, "report_data.js")

MD_EXTENSIONS = ['tables', 'fenced_code', 'nl2br', 'sane_lists']

DARK_SVGS = {
    "bon_nhom_duong_timing_paths.svg",
    "cau_truc_flip_flop_setup_time.svg",
    "cay_xung_nhip_cts_clock_tree.svg",
    "counter_gate_level_schematic.svg",
    "counter_schematic.svg",
    "cts_can_bang_clock_tree_truoc_va_sau.svg",
    "floorplan_architecture.svg",
    "hien_tuong_glitch_va_metastability.svg",
    "kien_truc_bo_nhan_mult_lab2.svg",
    "liberty_7_attributes.svg",
    "mo_hinh_thoi_gian_ff_to_ff.svg",
    "phuong_phap_luan_sta_timing_graph.svg",
    "rca_8bit_architecture.svg",
    "so_do_thoi_gian_setup_100mhz_vs_50mhz.svg",
    "yosys_abc_pipeline.svg",
}


def slugify(text):
    clean = re.sub(r'[^\w\s-]', '', text)
    clean = re.sub(r'\s+', '-', clean.strip().lower())
    clean = re.sub(r'-+', '-', clean)
    return clean


def extract_toc(markdown_text, prefix="sec"):
    toc = []
    lines = markdown_text.split("\n")
    slug_counts = {}
    in_fence = False
    for line in lines:
        s = line.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r'^(#{1,4})\s+(.*)$', s)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            clean_title = re.sub(r'[*_`]', '', title).strip()
            clean_title = re.sub(r'<[^>]+>', '', clean_title).strip()
            base_slug = slugify(clean_title)
            if not base_slug:
                base_slug = f"sec-{level}"

            slug_key = f"{prefix}-{base_slug}"
            count = slug_counts.get(slug_key, 0)
            slug_counts[slug_key] = count + 1
            final_id = slug_key if count == 0 else f"{slug_key}-{count}"

            toc.append({
                "level": level,
                "title": clean_title,
                "anchor": final_id
            })
    return toc


def assign_heading_ids(html_text, toc_list):
    toc_iter = iter(toc_list)

    def replacer(match):
        level = int(match.group(1))
        content = match.group(2)
        try:
            item = next(toc_iter)
            anchor = item["anchor"]
        except StopIteration:
            anchor = f"heading-{level}"
        return f'<h{level} id="{anchor}" class="report-heading">{content}</h{level}>'

    return re.sub(r'<h([1-4])>(.*?)</h\1>', replacer, html_text)


def sanitize_latex(text):
    text = re.sub(r'\\text\{\\textbf\{([^}]+)\}\}', r'\\mathbf{\1}', text)

    def fix_mathbf(m):
        inner = m.group(1)
        if r'\text{' in inner:
            return m.group(0)
        inner = inner.replace(r'\_', '_')
        if '_' in inner:
            inner = re.sub(r'_+', lambda sm: f"\\text{{{sm.group(0)}}}", inner)
            return f"\\mathbf{{{inner}}}"
        return m.group(0)

    return re.sub(r'\\mathbf\{([^}]+)\}', fix_mathbf, text)


def wrap_images(text, image_cards=None):
    def repl(m):
        alt = m.group(1).strip()
        url = m.group(2).strip()
        filename = os.path.basename(url)
        web_url = f"images/{filename}"

        tech_badge = "THIẾT KẾ VI MẠCH ASIC"
        lower_alt = alt.lower()
        lower_fn = filename.lower()
        if "roadmap" in lower_alt or "hành trình" in lower_alt or "lộ trình" in lower_alt or "tổng quan" in lower_alt:
            tech_badge = "MASTER ROADMAP ARCHITECTURE"
        elif "gtkwave" in lower_fn or "sóng" in lower_alt or "tap" in lower_alt or "iopath" in lower_alt:
            tech_badge = "GTKWAVE PICOSECOND SIGNOFF"
        elif "tinytdc" in lower_fn:
            tech_badge = "TINYTDC DELAY-LINE ARCHITECTURE"
        elif "timing" in lower_alt or "ff-to-ff" in lower_alt or "setup" in lower_alt or "hold" in lower_alt:
            tech_badge = "STA TIMING MODEL"
        elif "clock" in lower_alt or "cts" in lower_alt:
            tech_badge = "CTS CLOCK TREE"
        elif "pdn" in lower_fn or "vpwr" in lower_fn or "power" in lower_alt:
            tech_badge = "PDN POWER GRID"
        elif "heatmap" in lower_fn or "density" in lower_fn or "stdcells" in lower_fn or "xnor2" in lower_fn or "cell657" in lower_fn or "critical_path_gui" in lower_fn:
            tech_badge = "OPENROAD SILICON INSPECTOR"
        elif "glitch" in lower_alt or "metastability" in lower_alt:
            tech_badge = "SILICON REALITY"
        elif "summary" in lower_alt or "báo cáo" in lower_alt or "rpt" in lower_fn or "report" in lower_alt:
            tech_badge = "OPENROAD STA REPORT"
        elif "dse" in lower_alt or "sweep" in lower_alt or "pareto" in lower_alt or "kịch bản" in lower_alt:
            tech_badge = "DSE PARETO METRICS"
        elif "mult" in lower_alt or "nhân" in lower_alt:
            tech_badge = "REGISTERED MULTIPLIER"
        elif "buffer" in lower_alt:
            tech_badge = "HOLD FIXING BUFFER"
        elif "corner" in lower_alt or "pvt" in lower_alt:
            tech_badge = "PVT CORNERS"
        elif "schematic" in lower_alt:
            tech_badge = "CIRCUIT SCHEMATIC"
        elif "floorplan" in lower_alt:
            tech_badge = "FLOORPLAN ARCHITECTURE"
        elif "render" in lower_alt:
            tech_badge = "3D SILICON RENDER"

        safe_alt_attr = html_lib.escape(alt, quote=True)
        safe_alt_html = html_lib.escape(alt, quote=False)
        wrap_bg = "#0f172a" if filename in DARK_SVGS else "#ffffff"
        card_html = f'''<div class="interactive-diagram-card">
  <div class="diagram-card-header">
    <span class="badge-tech">{tech_badge}</span>
    <span class="badge-status">{safe_alt_html.upper()}</span>
  </div>
  <div class="diagram-img-wrap" style="background: {wrap_bg}; padding: 12px; border-radius: 6px; border: 1px solid #e6e4dd;">
    <img src="{web_url}" alt="{safe_alt_attr}" class="responsive-diagram-img" />
  </div>
  <div class="diagram-card-footer">
    <span><strong>{safe_alt_html}</strong> <em>(Nhấp chuột vào hình để phóng to toàn màn hình)</em></span>
    <span>SkyWater 130nm · OpenROAD Flow</span>
  </div>
</div>'''
        if image_cards is not None:
            idx = len(image_cards)
            image_cards.append(card_html)
            return f'\n\nIMAGECARDPROTECTED{idx}END\n\n'
        return card_html

    return re.sub(r'!\[(.*?)\]\((.*?)\)', repl, text)


def extract_fenced_blocks(text):
    """Extract top-level & list-indented ``` code fences and render them cleanly to HTML."""
    fences = []
    out_lines = []
    in_fence = False
    fence_indent = 0
    fence_lang = ""
    fence_buf = []

    for line in text.split('\n'):
        if not in_fence:
            m = re.match(r'^([ \t]*)```([^\n`]*)$', line)
            if m:
                in_fence = True
                fence_indent = len(m.group(1).expandtabs(4))
                fence_lang = m.group(2).strip().lower()
                fence_buf = []
            else:
                out_lines.append(line)
        else:
            if re.match(r'^[ \t]*```\s*$', line):
                in_fence = False
                code_str = textwrap.dedent('\n'.join(fence_buf)).strip('\n')
                idx = len(fences)
                if fence_lang == 'mermaid':
                    fences.append(f'<pre><code class="language-mermaid">{html_lib.escape(code_str)}</code></pre>')
                else:
                    cls = f' class="language-{html_lib.escape(fence_lang)}"' if fence_lang else ''
                    fences.append(f'<pre><code{cls}>{html_lib.escape(code_str)}</code></pre>')
                out_lines.append('')
                out_lines.append(f'    FENCEBLOCKPROTECTED{idx}END' if fence_indent >= 2 else f'FENCEBLOCKPROTECTED{idx}END')
                out_lines.append('')
            else:
                fence_buf.append(line)

    if in_fence and fence_buf:
        code_str = textwrap.dedent('\n'.join(fence_buf)).strip('\n')
        idx = len(fences)
        fences.append(f'<pre><code>{html_lib.escape(code_str)}</code></pre>')
        out_lines.append(f'FENCEBLOCKPROTECTED{idx}END')

    return '\n'.join(out_lines), fences


def normalize_markdown_structure(text):
    """Normalize shallow nested lists, paragraph-adjacent lists, indented tables & blockquotes for Python-Markdown."""
    lines = text.split('\n')
    out = []
    sub_indents = []  # Tracks original indent depths for nested list normalization
    active_list_depth = 0
    prev_was_list_context = False

    list_re = re.compile(r'^([ \t]*)(\*|\-|\+|\d+\.)\s+(.*)$')
    table_re = re.compile(r'^[ \t]*(\|.*\|)[ \t]*$')
    bq_re = re.compile(r'^([ \t]*)>(.*)$')
    fence_re = re.compile(r'^[ \t]*(FENCEBLOCKPROTECTED\d+END|CALLOUTPROTECTED\d+END)\s*$')

    for line in lines:
        stripped = line.strip()

        if not stripped:
            out.append('')
            continue

        # 1. Placeholders (fences / callouts) inside or outside lists
        mf = fence_re.match(line)
        if mf:
            if prev_was_list_context and active_list_depth > 0:
                out.append(('    ' * (active_list_depth + 1)) + mf.group(1))
            else:
                out.append(mf.group(1))
            continue

        # 2. Tables: dedent to col 0 and insert blank line if preceded by non-table line
        mt = table_re.match(line)
        if mt:
            if out and out[-1].strip() != '' and not table_re.match(out[-1]):
                out.append('')
            out.append(mt.group(1))
            sub_indents = []
            active_list_depth = 0
            prev_was_list_context = False
            continue

        # 3. Blockquotes: preserve inside lists at multiple-of-4 indent & ensure blank line before blockquote and before lists inside blockquote
        mb = bq_re.match(line)
        if mb:
            ind = len(mb.group(1).expandtabs(4))
            inner = mb.group(2)
            if out and out[-1].strip() != '' and not bq_re.match(out[-1]):
                out.append('')
            norm_ind = ('    ' * max(1, active_list_depth)) if (ind > 0 and prev_was_list_context) else ''
            # If blockquote line starts a list (*, -, +, 1.) right after non-list blockquote text, insert blank '>' line
            if re.match(r'^\s*(\*|\-|\+|\d+\.)\s+', inner) and out:
                prev_bq = bq_re.match(out[-1])
                if prev_bq:
                    prev_inner = prev_bq.group(2).strip()
                    if prev_inner and not re.match(r'^(\*|\-|\+|\d+\.)\s+', prev_inner):
                        out.append(f'{norm_ind}>')
            out.append(f'{norm_ind}>{inner}')
            continue

        # 4. List items (*, -, +, 1.)
        ml = list_re.match(line)
        if ml:
            ind = len(ml.group(1).expandtabs(4))
            marker = ml.group(2)
            body = ml.group(3)
            if out and bq_re.match(out[-1]):
                out.append('')
            if ind == 0:
                sub_indents = []
                active_list_depth = 0
                if out and out[-1].strip() != '':
                    prev_s = out[-1].strip()
                    if not list_re.match(out[-1]) and not prev_s.startswith(('---', '***', '___', 'CALLOUTPROTECTED', 'FENCEBLOCKPROTECTED')):
                        out.append('')
                out.append(f'{marker} {body}')
            else:
                if not prev_was_list_context:
                    sub_indents = [ind]
                else:
                    while sub_indents and sub_indents[-1] > ind:
                        sub_indents.pop()
                    if not sub_indents or ind > sub_indents[-1]:
                        sub_indents.append(ind)
                depth = len(sub_indents)
                active_list_depth = depth
                # Insert blank line when transitioning from a paragraph or heading? No, keep nested continuous unless needed
                norm_ind = '    ' * depth
                out.append(f'{norm_ind}{marker} {body}')
            prev_was_list_context = True
            continue

        # 5. Headings, HRs, block math, or standalone divs break list context
        if stripped.startswith(('#', '---', '<div', '<h', 'MATHBLOCKPROTECTED')):
            if stripped.startswith('MATHBLOCKPROTECTED') and prev_was_list_context and line.startswith(' '):
                out.append(('    ' * (active_list_depth + 1)) + stripped)
                continue
            sub_indents = []
            active_list_depth = 0
            prev_was_list_context = False
            out.append(line)
            continue

        # 6. Normal continuation line vs fresh paragraph
        if prev_was_list_context and line.startswith(' '):
            out.append(('    ' * (active_list_depth + 1)) + stripped)
        else:
            sub_indents = []
            active_list_depth = 0
            prev_was_list_context = False
            out.append(line)

    return '\n'.join(out)


def render_markdown_core(raw_text, is_callout=False):
    """Unified markdown -> HTML renderer protecting fences, image cards, double/single inline code & math."""
    fenced_text, fences = extract_fenced_blocks(raw_text)

    image_cards = []
    if not is_callout:
        fenced_text = wrap_images(fenced_text, image_cards)

    # Protect double-backtick spans first (e.g. `` `ifdef FUNCTIONAL ``), then single-backtick spans
    inline_codes = []

    def save_double_code(m):
        inner = m.group(1).strip()
        inline_codes.append(f'<code>{html_lib.escape(inner)}</code>')
        return f'INLINECODEPROTECTED{len(inline_codes)-1}END'

    def save_single_code(m):
        inner = m.group(1)
        inline_codes.append(f'<code>{html_lib.escape(inner)}</code>')
        return f'INLINECODEPROTECTED{len(inline_codes)-1}END'

    protected = re.sub(r'``([^\n]+?)``', save_double_code, fenced_text)
    protected = re.sub(r'`([^`\n]+)`', save_single_code, protected)

    # Protect LaTeX math ($$...$$ and $...$) BEFORE markdown touches underscores/asterisks
    math_blocks = []

    def save_math(m):
        math_blocks.append(m.group(0))
        return f'MATHBLOCKPROTECTED{len(math_blocks)-1}END'

    protected = re.sub(r'\$\$[\s\S]*?\$\$', save_math, protected)
    protected = re.sub(r'\$[^\$\n]+?\$', save_math, protected)

    # Convert callouts at top-level only (match strictly consecutive '>' lines so adjacent list items aren't swallowed!)
    callout_blocks = []
    if not is_callout:
        def save_callout(m):
            leading_ws = m.group(1)
            alert_type = m.group(2).upper()
            content = m.group(3).strip()
            callout_blocks.append(render_callout(alert_type, content))
            tok = f'CALLOUTPROTECTED{len(callout_blocks)-1}END'
            ind = len(leading_ws.expandtabs(4))
            return f'\n\n    {tok}\n\n' if ind >= 2 else f'\n\n{tok}\n\n'

        protected = re.sub(
            r'^([ \t]*)>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]([^\n]*(?:\n[ \t]*>[^\n]*)*)',
            save_callout,
            protected,
            flags=re.MULTILINE
        )

    # Normalize lists, tables, blockquotes
    normalized = normalize_markdown_structure(protected)

    converter = markdown.Markdown(extensions=MD_EXTENSIONS)
    html = converter.convert(normalized)

    # Restore fenced code blocks cleanly (strip wrapping <p>...</p> around fence placeholders)
    for idx, fb in enumerate(fences):
        token = f'FENCEBLOCKPROTECTED{idx}END'
        html = re.sub(rf'<p>\s*{token}\s*</p>', lambda _, v=fb: v, html)
        html = html.replace(token, fb)

    # Restore image cards cleanly (before/outside <p> tags)
    for idx, icard in enumerate(image_cards):
        token = f'IMAGECARDPROTECTED{idx}END'
        html = re.sub(rf'<p>\s*{token}\s*</p>', lambda _, v=icard: v, html)
        html = html.replace(token, icard)

    # Restore callouts cleanly
    for idx, cb in enumerate(callout_blocks):
        token = f'CALLOUTPROTECTED{idx}END'
        html = re.sub(rf'<p>\s*{token}\s*</p>', lambda _, v=cb: v, html)
        html = html.replace(token, cb)

    # Restore inline code & math blocks
    for idx, ic in enumerate(inline_codes):
        html = html.replace(f'INLINECODEPROTECTED{idx}END', ic)

    for idx, mb in enumerate(math_blocks):
        html = html.replace(f'MATHBLOCKPROTECTED{idx}END', mb)

    return html


def render_callout(alert_type, content):
    label_map = {
        "NOTE": ("callout-intuition", "TRỰC GIÁC & BẢN CHẤT VẬT LÝ"),
        "TIP": ("callout-breakthrough", "ĐỘT PHÁ TƯ DUY & KỸ THUẬT THỰC CHIẾN"),
        "IMPORTANT": ("callout-mechanism", "CƠ CHẾ VI MẠCH & MẮT XÍCH CỐT TỬ"),
        "WARNING": ("callout-warning", "CẠM BẪY KỸ THUẬT & LỖI NGUY HIỂM"),
        "CAUTION": ("callout-defense", "GHI CHÚ KIẾN TRÚC SƯ TRƯỞNG"),
    }
    css_class, label = label_map.get(alert_type, ("callout-intuition", "TRỰC GIÁC & BẢN CHẤT VẬT LÝ"))

    clean_lines = []
    subheadings = []
    inline_md = markdown.Markdown(extensions=['nl2br'])

    for line in content.split('\n'):
        l = re.sub(r'^\s*>\s?', '', line)
        mh = re.match(r'^(#{1,6})\s+(.*)$', l.strip())
        if mh:
            # Convert inline markdown (backticks, **bold**, *italic*) inside callout subheadings cleanly!
            heading_raw = mh.group(2).strip()
            heading_inline = re.sub(r'``([^\n]+?)``', lambda m: f'<code>{html_lib.escape(m.group(1).strip())}</code>', heading_raw)
            heading_inline = re.sub(r'`([^`\n]+)`', lambda m: f'<code>{html_lib.escape(m.group(1))}</code>', heading_inline)
            inline_md.reset()
            h_html = inline_md.convert(heading_inline)
            h_html = re.sub(r'^<p>(.*)</p>$', r'\1', h_html, flags=re.DOTALL)
            idx = len(subheadings)
            subheadings.append(f'<div class="callout-subheading" style="font-size:1.04rem;font-weight:700;margin:10px 0 4px 0;color:#111827;">{h_html}</div>')
            clean_lines.append('')
            clean_lines.append(f'CALLOUTSUBHEADING{idx}END')
            clean_lines.append('')
        else:
            clean_lines.append(l)

    body_html = render_markdown_core('\n'.join(clean_lines), is_callout=True)
    for idx, sh in enumerate(subheadings):
        token = f'CALLOUTSUBHEADING{idx}END'
        body_html = re.sub(rf'<p>\s*{token}\s*</p>', lambda _, v=sh: v, body_html)
        body_html = body_html.replace(token, sh)

    return f'<div class="callout-box {css_class}"><div class="callout-title">{label}</div><div class="callout-body">{body_html}</div></div>'


def highlight_terms(text):
    protected = []

    def save_prot(m):
        protected.append(m.group(0))
        return f"___PROT_{len(protected)-1}___"

    text = re.sub(r'<div class="diagram-card-(?:header|footer)">.*?</div>', save_prot, text, flags=re.DOTALL)
    text = re.sub(r'<pre>.*?</pre>', save_prot, text, flags=re.DOTALL)
    text = re.sub(r'<svg.*?</svg>', save_prot, text, flags=re.DOTALL)
    text = re.sub(r'\$\$[\s\S]*?\$\$', save_prot, text)
    text = re.sub(r'\$[^\$\n]+?\$', save_prot, text)
    text = re.sub(r'<code.*?>.*?</code>', save_prot, text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', save_prot, text)

    terms = [
        (r'\b(SkyWater\s*130nm|sky130A|sky130_fd_sc_hd)\b', r'<span class="hl-chip hl-asic">\1</span>'),
        (r'\b(OpenROAD|OpenLane|LibreLane|Yosys|OpenSTA|TritonRoute|Magic|KLayout|CVC64|GTKWave)\b', r'<span class="hl-chip hl-radar">\1</span>'),
        (r'\b(DPL-0036|ResizerTimingPostCTS)\b', r'<span class="hl-chip hl-fpga" style="background:#fef2f2;color:#b91c1c;border-color:#fecaca;">\1</span>'),
        (r'\b(GDSII|DEF|LEF|SDF|Liberty|\.lib|\.odb)\b', r'<span class="hl-chip hl-int8">\1</span>'),
        (r'\b(ABC\s*Engine|AIG|Technology\s*Mapping)\b', r'<span class="hl-chip hl-fpga">\1</span>'),
        (r'\b(Static Timing Analysis|STA|Timing Closure|Physical Design)\b', r'<span class="hl-chip hl-asic">\1</span>'),
        (r'\b(Setup Violation|Hold Violation)\b', r'<span class="hl-chip hl-fpga" style="background:#fef2f2;color:#b91c1c;border-color:#fecaca;">\1</span>'),
        (r'\b(Setup Slack|Hold Slack|Worst Negative Slack|WNS|Total Negative Slack|TNS)\b', r'<span class="hl-metric hl-amber">\1</span>'),
        (r'\b(Data Arrival Time|Data Required Time)\b', r'<span class="hl-chip hl-radar">\1</span>'),
        (r'\b(Clock Skew|Clock Latency|Clock Uncertainty|Slew Rate|Transition Time)\b', r'<span class="hl-chip hl-int8">\1</span>'),
        (r'\b(max_ss_100C_1v60|nom_tt_025C_1v80|min_ff_n40C_1v95|nom_ss_100C_1v60|nom_ff_n40C_1v95)\b', r'<span class="hl-chip hl-fpga">\1</span>'),
        (r'\b(DSE\s*Sweep|Design Space Exploration|RTL Pipelining)\b', r'<span class="hl-chip hl-radar">\1</span>'),
        (r'\b(mult\.v|mult\.sdc|mult_post_pnr\.sdc|config\.json|cpu8bit|TinyTDC)\b', r'<span class="hl-chip hl-int8">\1</span>'),
        (r'\b(15\.0\s*ns|13\.0\s*ns|66\.67\s*MHz|76\.92\s*MHz|100\s*MHz|50\s*MHz|20\s*ns|10\s*ns)\b', r'<span class="hl-metric hl-cyan">\1</span>'),
        (r'\b(-0\.1477\s*ns|-0\.569\s*ns|\+1\.5302\s*ns|\+2\.709\s*ns|\+1\.4523\s*ns|\+7\.489\s*ns)\b', r'<span class="hl-metric hl-emerald">\1</span>'),
        (r'\b(376\.611\s*µm²|376\.611\s*um²|1184\s*µm²|1254\s*µm²|1290\s*µm²|1386\s*µm²)\b', r'<span class="hl-metric hl-amber">\1</span>'),
        (r'\b(31\s*cổng\s*logic|8\s*DFF|23\s*Combinational|16\s*Flip-Flop)\b', r'<span class="hl-metric hl-emerald">\1</span>'),
    ]
    for pat, rep in terms:
        text = re.sub(pat, rep, text)

    for i in range(len(protected) - 1, -1, -1):
        text = text.replace(f"___PROT_{i}___", protected[i])

    return text


def convert_markdown_document(raw_md, doc_id="doc"):
    raw_md = raw_md.replace('\r\n', '\n')
    raw_md = sanitize_latex(raw_md)
    raw_md = re.sub(r'\)\s*(#+\s+)', r')\n\n\1', raw_md)

    toc = extract_toc(raw_md, doc_id)
    html = render_markdown_core(raw_md, is_callout=False)
    html = assign_heading_ids(html, toc)
    html = re.sub(r'(<table>.*?</table>)', r'<div class="table-responsive">\1</div>', html, flags=re.DOTALL)
    html = highlight_terms(html)
    return html, toc


print("Builder helper functions initialized successfully.")
