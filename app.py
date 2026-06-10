{\rtf1\ansi\ansicpg1252\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
import numpy as np\
import matplotlib.pyplot as plt\
import io\
\
# \uc0\u3605 \u3633 \u3657 \u3591 \u3588 \u3656 \u3634 \u3627 \u3609 \u3657 \u3634 \u3648 \u3623 \u3655 \u3610 \u3650 \u3611 \u3619 \u3649 \u3585 \u3619 \u3617 \
st.set_page_config(page_title="SL-TTS Biomechanical Analyzer", layout="wide")\
\
st.title("\uc0\u55356 \u57283 \u8205 \u9794 \u65039  Single-Leg Time to Stability (SL-TTS) Analyzer")\
st.write("\uc0\u3649 \u3629 \u3611 \u3614 \u3621 \u3636 \u3648 \u3588 \u3594 \u3633 \u3609 \u3623 \u3636 \u3648 \u3588 \u3619 \u3634 \u3632 \u3627 \u3660 \u3648 \u3626 \u3606 \u3637 \u3618 \u3619 \u3616 \u3634 \u3614 \u3649 \u3621 \u3632 \u3614 \u3634 \u3619 \u3634 \u3617 \u3636 \u3648 \u3605 \u3629 \u3619 \u3660 \u3594 \u3637 \u3623 \u3585 \u3621 \u3624 \u3634 \u3626 \u3605 \u3619 \u3660 \u3626 \u3635 \u3627 \u3619 \u3633 \u3610 \u3585 \u3634 \u3619 \u3607 \u3604 \u3626 \u3629 \u3610  Single Leg Deadlift (SLDL)")\
\
# \uc0\u3626 \u3656 \u3623 \u3609 \u3605 \u3636 \u3604 \u3605 \u3656 \u3629 \u3612 \u3641 \u3657 \u3651 \u3594 \u3657  (Sidebar) \u3626 \u3635 \u3627 \u3619 \u3633 \u3610 \u3605 \u3633 \u3657 \u3591 \u3588 \u3656 \u3634 \u3614 \u3634 \u3619 \u3634 \u3617 \u3636 \u3648 \u3605 \u3629 \u3619 \u3660 \
st.sidebar.header("\uc0\u55357 \u57056  \u3585 \u3634 \u3619 \u3605 \u3633 \u3657 \u3591 \u3588 \u3656 \u3634 \u3614 \u3634 \u3619 \u3634 \u3617 \u3636 \u3648 \u3605 \u3629 \u3619 \u3660 ")\
sampling_rate = st.sidebar.number_input("Sampling Rate (Hz)", min_value=1, value=1000, step=100)\
contact_threshold = st.sidebar.number_input("Initial Contact Threshold (N)", min_value=0.0, value=10.0, step=1.0)\
stability_window_sec = st.sidebar.number_input("Stability Window Duration (Seconds)", min_value=0.1, value=1.0, step=0.1)\
\
# \uc0\u3649 \u3611 \u3621 \u3591 \u3648 \u3623 \u3621 \u3634 \u3627 \u3609 \u3657 \u3634 \u3605 \u3656 \u3634 \u3591 \u3651 \u3627 \u3657 \u3648 \u3611 \u3655 \u3609 \u3592 \u3635 \u3609 \u3623 \u3609 \u3592 \u3640 \u3604 \u3586 \u3657 \u3629 \u3617 \u3641 \u3621 \u3605 \u3634 \u3617  Sampling Rate\
window_size = int(stability_window_sec * sampling_rate)\
\
# \uc0\u3626 \u3656 \u3623 \u3609 \u3629 \u3633 \u3611 \u3650 \u3627 \u3621 \u3604 \u3652 \u3615 \u3621 \u3660 \u3604 \u3636 \u3610  (.csv)\
uploaded_file = st.file_uploader("\uc0\u3629 \u3633 \u3611 \u3650 \u3627 \u3621 \u3604 \u3652 \u3615 \u3621 \u3660 \u3586 \u3657 \u3629 \u3617 \u3641 \u3621 \u3604 \u3636 \u3610  (.csv) \u3607 \u3637 \u3656 \u3609 \u3637 \u3656 ", type=["csv"])\
\
if uploaded_file is not None:\
    try:\
        # \uc0\u3629 \u3656 \u3634 \u3609 \u3652 \u3615 \u3621 \u3660 \u3586 \u3657 \u3629 \u3617 \u3641 \u3621 \u3604 \u3657 \u3623 \u3618 \u3605 \u3633 \u3623 \u3588 \u3633 \u3656 \u3609 \u3648 \u3595 \u3617 \u3636 \u3650 \u3588 \u3621 \u3629 \u3609  (;)\
        df = pd.read_csv(uploaded_file, delimiter=';')\
        st.success("\uc0\u3650 \u3627 \u3621 \u3604 \u3652 \u3615 \u3621 \u3660 \u3586 \u3657 \u3629 \u3617 \u3641 \u3621 \u3626 \u3635 \u3648 \u3619 \u3655 \u3592 !")\
        \
        # \uc0\u3605 \u3619 \u3623 \u3592 \u3626 \u3629 \u3610 \u3588 \u3623 \u3634 \u3617 \u3626 \u3617 \u3610 \u3641 \u3619 \u3603 \u3660 \u3586 \u3629 \u3591 \u3650 \u3588 \u3619 \u3591 \u3626 \u3619 \u3657 \u3634 \u3591 \u3588 \u3629 \u3621 \u3633 \u3617 \u3609 \u3660 \
        required_cols = ['timestamp', '2 Newton', '2 sway X', '2 sway Y', '2 velocity']\
        if not all(col in df.columns for col in required_cols):\
            st.error("\uc0\u3650 \u3588 \u3619 \u3591 \u3626 \u3619 \u3657 \u3634 \u3591 \u3652 \u3615 \u3621 \u3660 \u3652 \u3617 \u3656 \u3606 \u3641 \u3585 \u3605 \u3657 \u3629 \u3591  \u3585 \u3619 \u3640 \u3603 \u3634 \u3605 \u3619 \u3623 \u3592 \u3626 \u3629 \u3610 \u3627 \u3633 \u3623 \u3586 \u3657 \u3629 \u3588 \u3629 \u3621 \u3633 \u3617 \u3609 \u3660 \u3604 \u3636 \u3610 ")\
        else:\
            # \uc0\u3626 \u3585 \u3633 \u3604 \u3586 \u3657 \u3629 \u3617 \u3641 \u3621 \u3648 \u3611 \u3655 \u3609  Arrays\
            force = df['2 Newton'].values\
            sway_x = df['2 sway X'].values\
            sway_y = df['2 sway Y'].values\
            velocity = df['2 velocity'].values\
            time_secs = df['timestamp'].values / sampling_rate\
            \
            # ---- 1. \uc0\u3588 \u3635 \u3609 \u3623 \u3603 \u3627 \u3634 \u3614 \u3634 \u3619 \u3634 \u3617 \u3636 \u3648 \u3605 \u3629 \u3619 \u3660 \u3648 \u3594 \u3636 \u3591 \u3594 \u3637 \u3623 \u3585 \u3621 \u3624 \u3634 \u3626 \u3605 \u3619 \u3660  ----\
            peak_force = np.max(force)\
            mean_sway_x = np.mean(sway_x)\
            mean_sway_y = np.mean(sway_y)\
            range_sway_x = np.max(sway_x) - np.min(sway_x)\
            range_sway_y = np.max(sway_y) - np.min(sway_y)\
            peak_velocity = np.max(np.abs(velocity))\
            \
            # ---- 2. \uc0\u3588 \u3635 \u3609 \u3623 \u3603 \u3605 \u3619 \u3619 \u3585 \u3632  SL-TTS ----\
            contact_idx = np.where(force >= contact_threshold)[0]\
            \
            idx_contact = None\
            t_contact_sec = None\
            idx_stability = None\
            t_stability_sec = None\
            sl_tts_sec = None\
            \
            # \uc0\u3605 \u3619 \u3623 \u3592 \u3626 \u3629 \u3610 \u3592 \u3640 \u3604 \u3611 \u3632 \u3607 \u3632 \u3649 \u3619 \u3585 \
            if len(contact_idx) > 0:\
                idx_contact = contact_idx[0]\
                t_contact_sec = time_secs[idx_contact]\
                \
                # \uc0\u3627 \u3634  Body Weight (BW) \u3592 \u3634 \u3585 \u3594 \u3656 \u3623 \u3591 \u3607 \u3657 \u3634 \u3618 \
                bw = np.mean(force[-100:])\
                upper_bound = bw + (0.05 * bw)\
                lower_bound = bw - (0.05 * bw)\
                \
                # \uc0\u3588 \u3657 \u3609 \u3627 \u3634  Onset of Stability \u3605 \u3634 \u3617 \u3585 \u3619 \u3629 \u3610 \u3648 \u3623 \u3621 \u3634 \u3607 \u3637 \u3656 \u3605 \u3633 \u3657 \u3591 \u3652 \u3623 \u3657 \
                for i in range(idx_contact, len(force) - window_size):\
                    window = force[i : i + window_size]\
                    if np.all((window >= lower_bound) & (window <= upper_bound)):\
                        idx_stability = i\
                        break\
                \
                if idx_stability is not None:\
                    t_stability_sec = time_secs[idx_stability]\
                    sl_tts_sec = t_stability_sec - t_contact_sec\
            \
            # ---- 3. \uc0\u3627 \u3609 \u3657 \u3634 \u3592 \u3629 \u3649 \u3626 \u3604 \u3591 \u3612 \u3621 \u3621 \u3633 \u3614 \u3608 \u3660  (UI Layout) ----\
            col1, col2, col3 = st.columns(3)\
            with col1:\
                st.metric(label="Peak Force (\uc0\u3649 \u3619 \u3591 \u3626 \u3641 \u3591 \u3626 \u3640 \u3604 )", value=f"\{peak_force:.2f\} N")\
                if sl_tts_sec is not None:\
                    st.metric(label="SL-TTS (\uc0\u3648 \u3623 \u3621 \u3634 \u3626 \u3641 \u3656 \u3588 \u3623 \u3634 \u3617 \u3648 \u3626 \u3606 \u3637 \u3618 \u3619 )", value=f"\{sl_tts_sec:.3f\} \u3623 \u3636 \u3609 \u3634 \u3607 \u3637 ")\
                else:\
                    st.metric(label="SL-TTS (\uc0\u3648 \u3623 \u3621 \u3634 \u3626 \u3641 \u3656 \u3588 \u3623 \u3634 \u3617 \u3648 \u3626 \u3606 \u3637 \u3618 \u3619 )", value="\u3652 \u3617 \u3656 \u3648 \u3586 \u3657 \u3634 \u3648 \u3585 \u3603 \u3601 \u3660 \u3648 \u3626 \u3606 \u3637 \u3618 \u3619 ")\
            with col2:\
                st.metric(label="Max Range Sway X (\uc0\u3585 \u3634 \u3619 \u3648 \u3595 \u3649 \u3609 \u3623 \u3595 \u3657 \u3634 \u3618 -\u3586 \u3623 \u3634 )", value=f"\{range_sway_x:.2f\}")\
                st.metric(label="Mean Sway X", value=f"\{mean_sway_x:.2f\}")\
            with col3:\
                st.metric(label="Max Range Sway Y (\uc0\u3585 \u3634 \u3619 \u3648 \u3595 \u3649 \u3609 \u3623 \u3627 \u3609 \u3657 \u3634 -\u3627 \u3621 \u3633 \u3591 )", value=f"\{range_sway_y:.2f\}")\
                st.metric(label="Peak Velocity (\uc0\u3588 \u3623 \u3634 \u3617 \u3648 \u3619 \u3655 \u3623 \u3626 \u3641 \u3591 \u3626 \u3640 \u3604 )", value=f"\{peak_velocity:.6f\} m/s")\
                \
            # ---- 4. \uc0\u3626 \u3656 \u3623 \u3609 \u3585 \u3634 \u3619 \u3648 \u3619 \u3609 \u3648 \u3604 \u3629 \u3619 \u3660 \u3585 \u3619 \u3634 \u3615 \u3623 \u3636 \u3648 \u3588 \u3619 \u3634 \u3632 \u3627 \u3660  ----\
            st.subheader("\uc0\u55357 \u56520  Force-Time Curve Analysis")\
            fig, ax = plt.subplots(figsize=(12, 5))\
            ax.plot(time_secs, force, color='#7f7f7f', alpha=0.6, label='Vertical GRF (N)')\
            \
            if idx_contact is not None:\
                ax.axhline(y=bw, color='#2ca02c', linestyle='-', linewidth=2, label=f'Body Weight (\{bw:.1f\} N)')\
                ax.axhline(y=upper_bound, color='#d62728', linestyle='--', alpha=0.8, label='+5% BW boundary')\
                ax.axhline(y=lower_bound, color='#d62728', linestyle='--', alpha=0.8, label='-5% BW boundary')\
                ax.axvline(x=t_contact_sec, color='#ff7f0e', linestyle=':', linewidth=2, label=f'Initial Contact (\{t_contact_sec:.3f\} s)')\
                \
                if t_stability_sec is not None:\
                    ax.axvline(x=t_stability_sec, color='#9467bd', linestyle=':', linewidth=2, label=f'Stability Onset (\{t_stability_sec:.3f\} s)')\
                    ax.axvspan(t_stability_sec, t_stability_sec + stability_window_sec, color='#2ca02c', alpha=0.1, label='Stable Window')\
            \
            ax.set_xlabel("Time (Seconds)")\
            ax.set_ylabel("Force (Newtons)")\
            ax.grid(True, linestyle='--', alpha=0.5)\
            ax.legend(loc='lower right')\
            \
            st.pyplot(fig)\
            \
    except Exception as e:\
        st.error(f"\uc0\u3648 \u3585 \u3636 \u3604 \u3586 \u3657 \u3629 \u3612 \u3636 \u3604 \u3614 \u3621 \u3634 \u3604 \u3651 \u3609 \u3585 \u3634 \u3619 \u3611 \u3619 \u3632 \u3617 \u3623 \u3621 \u3612 \u3621 \u3652 \u3615 \u3621 \u3660 : \{e\}")}