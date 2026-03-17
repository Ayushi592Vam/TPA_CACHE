"""
ui/topbar.py
Renders the top navigation bar: logo, title, schema badge, settings gear.
Returns True if the settings dialog should be opened.
"""

import streamlit as st
from modules.logo import logo_img_tag


def _navbar_badge_html(active_schema: str | None, schemas: dict) -> str:
    if not active_schema or active_schema not in schemas:
        return ""
    sc = schemas[active_schema]
    return (
        f'<span class="navbar-schema-badge" '
        f'style="border-color:{sc["color"]}44;color:{sc["color"]};background:{sc["color"]}11;'
        f'display:inline-flex;align-items:center;gap:6px;border-radius:6px;padding:4px 12px;'
        f'font-size:12px;font-weight:700;font-family:monospace;border:1px solid;white-space:nowrap;">'
        f'{sc["icon"]} {active_schema} &nbsp;&middot;&nbsp; {sc["version"]}</span>'
    )


def render_topbar(schemas: dict, config_load_status: dict) -> bool:
    """
    Renders the top bar.
    Returns True if the settings gear was clicked (caller should open dialog).
    """
    active_schema = st.session_state.get("active_schema", None)
    _logo         = logo_img_tag(height=34)
    _badge        = _navbar_badge_html(active_schema, schemas)

    col_title, col_gear = st.columns([11, 1])

    with col_title:
        st.markdown(
            '<div style="display:flex;align-items:center;padding:10px 0 6px 0;min-height:52px;">'
            + _logo
            + '<div style="display:inline-flex;flex-direction:column;vertical-align:middle;margin-left:4px;">'
              '<span class="navbar-title">&#128737; TPA Loss Run Parser</span>'
              '<span class="navbar-subtitle">Insurance Loss Run Parsing &amp; Schema Export Platform</span>'
              '</div>'
            + ('&nbsp;&nbsp;' + _badge if _badge else '')
            + '</div>',
            unsafe_allow_html=True,
        )

    with col_gear:
        st.markdown("<div style='padding-top:12px;'>", unsafe_allow_html=True)
        clicked = st.button("⚙", key="open_settings", help="Settings", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<hr style="border:none;border-top:1px solid #2a2a45;margin:4px 0 20px 0;">',
        unsafe_allow_html=True,
    )
    return clicked
