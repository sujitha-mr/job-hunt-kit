from hashlib import sha256
import os
from pathlib import Path
import streamlit as st
from resume_builder import parse_profile, select_demo, select_ai, render_resume, coverage, export_docx

ROOT = Path(__file__).parent


def reset_approval():
    st.session_state.approved = False


st.set_page_config(page_title='Evidence • Resume Builder', page_icon='📄', layout='wide')
st.title('Evidence • Resume Builder')
st.caption('Your experience. A focused resume. Every selected fact traceable to its source.')
st.info('Prototype: offline demo works without an API key. AI mode selects evidence; source wording is preserved. No employer ATS score is claimed.')

with st.sidebar:
    st.header('Workspace')
    mode = st.radio('Drafting mode', ['Offline demo', 'AI evidence selection'])
    model = st.text_input('OpenAI model', value=os.getenv('RESUME_MODEL', 'gpt-4.1-mini')) if mode.startswith('AI') else ''
    st.caption('Profiles and drafts stay in this session; the app does not write them to disk. Hosting infrastructure may retain operational metadata. Use a private local instance for real profiles.')
    if mode.startswith('AI'):
        st.warning('Generation sends profile evidence and the JD to OpenAI. API usage is billed separately. Configure RESUME_API_KEY on the server; never paste keys into a profile.')
    if st.button('Clear session'):
        st.session_state.clear()
        st.rerun()

left, right = st.columns(2)
with left:
    st.subheader('1 · Master profile')
    uploaded = st.file_uploader('Upload one person’s Markdown profile', type=['md', 'txt'])
    use_example = st.checkbox('Use fictional example profile', value=True)
    profile_text = (ROOT / 'examples/profile.md').read_text() if use_example else ''
    if uploaded is not None:
        try:
            profile_text = uploaded.getvalue().decode('utf-8-sig')
        except UnicodeDecodeError:
            st.error('Upload a UTF-8 text or Markdown file.')
            profile_text = ''
    profile = None
    if profile_text:
        try:
            profile = parse_profile(profile_text)
            st.success(f'Selected profile: {profile.name} · {len(profile.facts)} source facts')
            st.caption('Source claims are user-provided, not independently verified. Only Career Evidence, Experience, Skills, Education and Certifications sections are included.')
        except ValueError as exc:
            st.error(str(exc))
with right:
    st.subheader('2 · Target role')
    jd = st.text_area('Paste the full job description', value=(ROOT / 'examples/job-description.txt').read_text(), height=270, max_chars=30000)

signature = sha256((profile_text + '\0' + jd + '\0' + mode + '\0' + model).encode()).hexdigest()
if st.session_state.get('signature') != signature:
    for key in ['draft', 'ids', 'approved', 'editor']:
        st.session_state.pop(key, None)

if st.button('Build evidence-based draft', type='primary', disabled=profile is None):
    try:
        with st.spinner('Selecting relevant evidence…'):
            ids = select_demo(profile, jd) if mode == 'Offline demo' else select_ai(profile, jd, os.getenv('RESUME_API_KEY'), model)
            draft = render_resume(profile, ids)
            st.session_state.update(ids=ids, draft=draft, editor=draft, signature=signature, approved=False)
    except ValueError as exc:
        st.error(str(exc))
    except Exception:
        st.error('AI request failed. Check the server API-key configuration, network access, model availability, and API billing. No new draft was accepted.')

if st.session_state.get('draft') and profile:
    st.subheader('3 · Review your draft')
    st.caption('Source order and official role details are retained. Selection may omit useful evidence; review the evidence table before applying.')
    preview, evidence = st.tabs(['Resume editor', 'Evidence & gaps'])
    with preview:
        edited = st.text_area('Edit resume Markdown', key='editor', height=480, on_change=reset_approval)
        if edited != st.session_state.draft:
            st.warning('This draft has manual edits. Source traceability applies to the original selected facts; review all edited claims yourself.')
        with st.expander('Preview'):
            st.markdown(edited)
    with evidence:
        st.dataframe([{'ID': f.id, 'Section': f.section, 'Context': f.context, 'Source text': f.text, 'Selected': f.id in st.session_state.ids} for f in profile.facts], hide_index=True)
        st.markdown('**JD evidence candidates**')
        st.caption('Literal word overlap only. These are review aids, not verified qualification matches. Negation, scope and certification status require human review.')
        st.dataframe(coverage(profile, st.session_state.ids, jd), hide_index=True)
        st.warning('Profile guardrails and exclusions are never exported as qualifications. Consult the original profile for additional constraints. No ATS ranking or interview outcome is guaranteed.')
    approved = st.checkbox('I reviewed this draft for factual accuracy and approve it for download.', key='approved')
    if approved and edited.strip():
        st.download_button('Download Word resume', data=export_docx(edited), file_name='tailored-resume.docx', mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        st.download_button('Download Markdown', data=edited, file_name='tailored-resume.md')
