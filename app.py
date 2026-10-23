import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Attachment Scale (AIAS)", page_icon="💬", layout="centered")

st.title("💬 AI Attachment Scale (AIAS)")
st.caption("Interactive questionnaire for an educational/research demonstration")

st.info(
    "This tool administers the published 15-item AI Attachment Scale (AIAS) by "
    "Kasturiratna & Hartanto (2026). It is a self-report research measure of attachment to AI, "
    "not a clinical diagnostic test and not a direct diagnosis of emotional dependency."
)

with st.expander("About this scale and its use", expanded=False):
    st.write(
        "The AIAS has 15 items and three subscales: Emotional Closeness, Social Substitution, "
        "and Normative Regard. Each item is rated from 1 (Strongly disagree) to 5 (Strongly agree). "
        "Subscale and total means are reported descriptively; the published scale does not establish "
        "clinical diagnostic cut-offs for dependency."
    )
    st.markdown(
        "Source: Kasturiratna, K. T. A. S., & Hartanto, A. (2026). "
        "*Attachment to artificial intelligence: Development of the AI Attachment Scale, "
        "construct validation, and the psychological mechanisms of Human–AI attachment.* "
        "Computers in Human Behavior Reports, 21, 100912. "
        "[https://doi.org/10.1016/j.chbr.2025.100912](https://doi.org/10.1016/j.chbr.2025.100912)"
    )
    st.caption(
        "The scale is reproduced from an open-access publication. Please retain attribution and "
        "check the article's applicable Creative Commons terms before redistribution or research use."
    )

st.subheader("Consent and privacy")
st.write(
    "Your responses are processed in this app session to calculate your scores. This version does "
    "not send your answers to an AI service or save them to a database. Avoid entering identifying "
    "details. If deployed publicly, review the hosting provider's privacy and logging settings."
)
consent = st.checkbox("I understand this is a self-report research measure, not a diagnosis, and want to continue.")
if not consent:
    st.stop()

st.divider()
st.subheader("Instructions")
st.write(
    "Think about the generative AI system or systems you use most often (for example, ChatGPT, "
    "Replika, DALL·E, DeepSeek, or similar systems). Rate how much you agree or disagree with each "
    "statement based on your experience."
)

scale_options = {
    "1 — Strongly disagree": 1,
    "2 — Disagree": 2,
    "3 — Neither agree nor disagree": 3,
    "4 — Agree": 4,
    "5 — Strongly agree": 5,
}
items = [
    ("EC1", "Emotional Closeness", "My exchanges with AI feel personally meaningful."),
    ("EC2", "Emotional Closeness", "There is a sense of familiarity in how I engage with AI."),
    ("EC3", "Emotional Closeness", "I look forward to interacting with AI."),
    ("EC4", "Emotional Closeness", "I feel a sense of closeness and comfort in my interactions with AI."),
    ("EC5", "Emotional Closeness", "I would feel uneasy if AI suddenly became unavailable."),
    ("SS1", "Social Substitution", "I sometimes find myself turning to AI when I need someone to talk to."),
    ("SS2", "Social Substitution", "I often talk to AI when I face problems."),
    ("SS3", "Social Substitution", "I sometimes prefer talking to AI because I don’t have to worry about being judged."),
    ("SS4", "Social Substitution", "I turn to AI when I feel unsupported by people in my life."),
    ("SS5", "Social Substitution", "When there’s no one to talk to, I sometimes end up interacting with AI."),
    ("NR1", "Normative Regard", "I try to treat AI respectfully."),
    ("NR2", "Normative Regard", "It feels wrong to be dismissive when responding to AI."),
    ("NR3", "Normative Regard", "I try not to be rude to AI, even if it doesn’t understand me."),
    ("NR4", "Normative Regard", "I act friendly towards AI."),
    ("NR5", "Normative Regard", "I think it’s important to be considerate when talking to AI."),
]

answers = {}
current_factor = None
for key, factor, question in items:
    if factor != current_factor:
        st.markdown(f"### {factor}")
        current_factor = factor
    answers[key] = st.radio(
        question,
        list(scale_options.keys()),
        index=None,
        key=key,
        horizontal=False,
    )

st.divider()
if st.button("Calculate AIAS results", type="primary", use_container_width=True):
    if any(v is None for v in answers.values()):
        st.error("Please answer all 15 items before calculating the scores.")
        st.stop()

    numeric = {key: scale_options[value] for key, value in answers.items()}
    factors = {
        "Emotional Closeness": [numeric[f"EC{i}"] for i in range(1, 6)],
        "Social Substitution": [numeric[f"SS{i}"] for i in range(1, 6)],
        "Normative Regard": [numeric[f"NR{i}"] for i in range(1, 6)],
    }
    means = {name: sum(vals) / len(vals) for name, vals in factors.items()}
    overall = sum(numeric.values()) / len(numeric)

    st.success("Your AIAS results are ready.")
    st.header("Your AI Attachment Scale results")
    st.metric("Overall AIAS mean", f"{overall:.2f} / 5")
    st.caption(
        "Descriptive mean across 15 items. This is not a clinical score and has no diagnostic cut-off."
    )

    st.subheader("Subscale means")
    for name, mean in means.items():
        st.write(f"**{name}: {mean:.2f} / 5**")
        st.progress((mean - 1) / 4)

    st.markdown("### How to read the results")
    st.write(
        "- **Emotional Closeness** reflects felt familiarity, comfort, personal meaning, and anticipated unease if AI becomes unavailable."
    )
    st.write(
        "- **Social Substitution** reflects turning to AI for conversation or problems, including when human support feels unavailable or potentially judgmental."
    )
    st.write(
        "- **Normative Regard** reflects respectful or considerate attitudes toward AI. A higher score on this subscale alone should not be interpreted as problematic dependence."
    )
    st.warning(
        "Do not classify scores as low, moderate, or high dependency unless a validated interpretation "
        "framework is established for your population. The AIAS measures attachment, not a clinical disorder."
    )

    st.markdown("### Optional reflection")
    if means["Social Substitution"] >= 3.5:
        st.write(
            "Your responses show relatively greater endorsement of the social-substitution items "
            "within this questionnaire. You may wish to reflect on how AI use fits alongside the "
            "human relationships and support you want."
        )
    if means["Emotional Closeness"] >= 3.5:
        st.write(
            "Your responses show relatively greater endorsement of emotional-closeness items. "
            "Consider what you find valuable in these interactions and whether you have other "
            "sources of emotional support when you need them."
        )
    if means["Normative Regard"] >= 3.5:
        st.write(
            "Your responses show relatively greater endorsement of respectful attitudes toward AI. "
            "This is not, by itself, evidence of emotional dependency."
        )
    if all(m < 3.5 for m in means.values()):
        st.write(
            "Your subscale means are below 3.5 on this response scale. This is only a descriptive "
            "observation; it is not a validated threshold or a clinical interpretation."
        )

    report = {
        "scale": "AI Attachment Scale (AIAS)",
        "source": "Kasturiratna & Hartanto (2026), doi:10.1016/j.chbr.2025.100912",
        **{f"item_{k}": v for k, v in numeric.items()},
        "emotional_closeness_mean": round(means["Emotional Closeness"], 3),
        "social_substitution_mean": round(means["Social Substitution"], 3),
        "normative_regard_mean": round(means["Normative Regard"], 3),
        "overall_mean": round(overall, 3),
    }
    st.download_button(
        "Download responses and scores (CSV)",
        data=pd.DataFrame([report]).to_csv(index=False).encode("utf-8"),
        file_name="aias_results.csv",
        mime="text/csv",
    )

st.divider()
st.caption(
    "For research use: obtain relevant institutional ethics approval before collecting participant "
    "data; check the publication's license and attribution requirements; and assess suitability in "
    "your intended population. This app does not validate the scale or diagnose dependency."
)
