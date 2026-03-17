"""
ui/sheet_card.py
Renders the sheet-stats card and the LLM field-map notification banner.
"""

import streamlit as st


def render_sheet_card(
    selected_sheet: str,
    sheet_type: str,
    sh_hash: str,
    n_claims: int,
    total_rows: int,
    total_cols: int,
    n_merged: int,
    totals_data: dict,
    n_title_fields: int,
    from_cache: bool,
    sheet_dup_info: dict,
) -> None:
    sh_hash_short = sh_hash[:18] + "…" if sh_hash else "N/A"
    totals_cls    = "hi" if totals_data else "mid"
    totals_found  = "Found" if totals_data else "None"
    _cache_badge  = (
        "<span style='font-size:9px;color:#34d399;font-family:monospace;margin-left:6px;'>"
        "⚡ from cache</span>"
        if from_cache
        else ""
    )
    _type_cls = "unk" if sheet_type == "UNKNOWN" else ""

    st.markdown(
        f"""
        <div class="sheet-card">
          <div class="sheet-card-hdr">
            <div class="sheet-card-name">
              ⊞ {selected_sheet}
              <span class="sheet-type-tag {_type_cls}">{sheet_type}</span>
              {_cache_badge}
            </div>
            <span style="font-size:10px;color:var(--t3);font-family:var(--mono);">
              SHA-256:
              <span style="color:var(--green);font-size:9px;">{sh_hash_short}</span>
            </span>
          </div>
          <div class="sheet-stats-grid">
            <div class="sh-stat"><div class="sh-stat-lbl">Claim Rows</div><div class="sh-stat-val hi">{n_claims}</div></div>
            <div class="sh-stat"><div class="sh-stat-lbl">Rows</div><div class="sh-stat-val">{total_rows}</div></div>
            <div class="sh-stat"><div class="sh-stat-lbl">Columns</div><div class="sh-stat-val">{total_cols}</div></div>
            <div class="sh-stat"><div class="sh-stat-lbl">Merged Regions</div><div class="sh-stat-val">{n_merged}</div></div>
            <div class="sh-stat"><div class="sh-stat-lbl">Totals Row</div><div class="sh-stat-val {totals_cls}">{totals_found}</div></div>
            <div class="sh-stat"><div class="sh-stat-lbl">Title Fields</div><div class="sh-stat-val">{n_title_fields}</div></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Per-sheet duplicate warning
    _selected_dup = sheet_dup_info.get(selected_sheet)
    if _selected_dup:
        _orig_file  = _selected_dup.get("filename", "unknown file")
        _orig_sheet = _selected_dup.get("sheet_name", selected_sheet)
        _orig_date  = _selected_dup.get("first_seen", "")[:10]
        _same_name  = _orig_sheet == selected_sheet
        _sheet_ref  = f"sheet **{_orig_sheet}**" if not _same_name else "the same sheet name"
        st.warning(
            f"⚠ **This sheet was already processed** — {_sheet_ref} "
            f"in `{_orig_file}` on **{_orig_date}**."
        )


def render_llm_map_banner(llm_map_result: dict, llm_map_count: int) -> None:
    _mapped_cols   = list(llm_map_result.get("mappings", {}).keys())
    _unmapped_cols = llm_map_result.get("_unmapped", [])
    _details_str   = ", ".join(
        f"<b>{s}</b> → {t}"
        for s, t in list(llm_map_result.get("mappings", {}).items())[:5]
    )
    _unmapped_str = (
        f"<span style='color:var(--red);'>&nbsp;·&nbsp;"
        f"{len(_unmapped_cols)} column(s) could not be mapped</span>"
        if _unmapped_cols
        else ""
    )
    st.markdown(
        f"<div class='llm-map-banner'>"
        f"<div style='font-size:var(--sz-xs);font-weight:700;color:var(--yellow);"
        f"font-family:var(--mono);text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;'>"
        f"Unfamiliar columns detected — {llm_map_count} automatically mapped</div>"
        f"<div style='font-size:var(--sz-xs);color:var(--t2);font-family:var(--font);'>"
        f"{_details_str}{_unmapped_str}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
